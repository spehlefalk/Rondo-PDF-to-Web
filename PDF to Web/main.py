import os
import re
import sqlite3
import pdfplumber
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

def clean_text(text):
    cleaned_text = text.replace("(cid:13)", "").replace("(cid:10)", "")
    cleaned_text = re.sub(r',,{2,}', '', cleaned_text)
    cleaned_text = re.sub(r',+', ',', cleaned_text)
    return cleaned_text

def convert_pdf_to_txt(pdf_path, txt_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
        cleaned_text = clean_text(all_text)
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        return cleaned_text
    except Exception as e:
        print("Error:", str(e))
        return None

def convert_txt_to_csv(txt_path, csv_path):
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        cleaned_lines = [clean_text(line) for line in lines]
        data = [line.strip().split(';') for line in cleaned_lines if line.strip()]
        max_cols = max(len(row) for row in data)
        data = [row + [''] * (max_cols - len(row)) for row in data]
        header = ['Field' + str(i) for i in range(1, max_cols + 1)]
        df = pd.DataFrame(data, columns=header)
        df.to_csv(csv_path, index=False)
        return df
    except Exception as e:
        print("Error:", str(e))
        return None

def extract_and_save_aspects(df, conn):
    fields_to_extract = ['Name', 'Adresse', 'Telefon', 'Mobil', 'E-Mail', 'Auftrags Nr.', 'Lieferadressee']
    extracted_data = df[df['Field1'].isin(fields_to_extract)]
    aspects_dict = pd.Series(extracted_data.Field2.values, index=extracted_data.Field1).to_dict()
    field_values = [
        aspects_dict.get('Name', ''),
        aspects_dict.get('Adresse', ''),
        aspects_dict.get('Telefon', ''),
        aspects_dict.get('Mobil', ''),
        aspects_dict.get('E-Mail', ''),
        aspects_dict.get('Auftrags Nr.', ''),
        aspects_dict.get('Lieferadressee', '')
    ]
    c = conn.cursor()
    c.execute('''
    INSERT INTO extracted_aspects (Name, Adresse, Telefon, Mobil, Email, Auftrags_Nr, Lieferadresse)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', field_values)
    conn.commit()
    return field_values

def process_article_data(txt_path, conn):
    anzahl = []
    artikelnr = []
    bezeichnung = []
    with open(txt_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith('Anzahl Artikelnr. Bezeichnung'):
            continue
        parts = line.split(';')
        if len(parts) == 3:
            anzahl.append(parts[0].strip())
            artikelnr.append(parts[1].strip())
            bezeichnung.append(parts[2].strip())
    articles_df = pd.DataFrame({
        'Anzahl': anzahl,
        'Artikelnr.': artikelnr,
        'Bezeichnung': bezeichnung
    })
    c = conn.cursor()
    for i in range(len(articles_df)):
        c.execute('''
        INSERT INTO articles (Anzahl, Artikelnr, Bezeichnung)
        VALUES (?, ?, ?)
        ''', (articles_df.iloc[i]['Anzahl'], articles_df.iloc[i]['Artikelnr.'], articles_df.iloc[i]['Bezeichnung']))
    conn.commit()
    article_numbers_string = ",".join(artikelnr)
    articles_cleaned_content = articles_df.to_string(index=False)
    return article_numbers_string, articles_cleaned_content

def open_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        base_name = os.path.basename(file_path)
        file_name, _ = os.path.splitext(base_name)
        documents_path = os.path.join(os.path.expanduser("~"), "Documents")
        output_folder = os.path.join(documents_path, 'PDF to Web')
        db_path = os.path.join(output_folder, f'{file_name}.db')
        os.makedirs(output_folder, exist_ok=True)
        os.system(f'attrib +h "{output_folder}"')
        if os.path.exists(db_path):
            os.remove(db_path)
        save_txt_path = os.path.join(output_folder, 'intermediate.txt')
        save_csv_path = os.path.join(output_folder, 'intermediate.csv')
        text = convert_pdf_to_txt(file_path, save_txt_path)
        if text is not None:
            df = convert_txt_to_csv(save_txt_path, save_csv_path)
            if df is not None:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute('''
                CREATE TABLE IF NOT EXISTS extracted_aspects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT,
                    Adresse TEXT,
                    Telefon TEXT,
                    Mobil TEXT,
                    Email TEXT,
                    Auftrags_Nr TEXT,
                    Lieferadresse TEXT
                )
                ''')
                c.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Anzahl TEXT,
                    Artikelnr TEXT,
                    Bezeichnung TEXT
                )
                ''')
                conn.commit()
                field_values = extract_and_save_aspects(df, conn)
                article_numbers_string, articles_cleaned_content = process_article_data(save_txt_path, conn)
                conn.close()
                os.remove(save_txt_path)
                os.remove(save_csv_path)
                return article_numbers_string, field_values, articles_cleaned_content

def webcontrole(data_array, auftragsNr_stg, textarea_data):
    # Get the current directory path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Specify the relative path to your Chrome user data directory
    user_data_dir = os.path.join(current_dir, 'chrome_user_data')
    
    # Specify the profile you want to use
    profile_dir = 'Profile 1'
    
    # Set up Chrome options
    options = Options()
    options.add_argument(f'user-data-dir={user_data_dir}')
    options.add_argument(f'--profile-directory={profile_dir}')
    options.add_experimental_option("detach", True)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    #chromedriver_path = os.path.join(current_dir, 'chromedriver.exe')  # Update this path
    #service = Service(chromedriver_path)
    #driver = webdriver.Chrome(service=service, options=options)
    
    # Navigate to the target URL
    driver.get('https://app.artesa.de/office/assignment/create')
    
    # Pause to allow the page to load
    sleep(1)
    try:
        # Attempt to log in if login fields are present
        loggin_email_field = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.NAME, "email"))
        )
        loggin_password_field = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.NAME, "password"))
        )
        loggin_email_field.send_keys("stephan.schneider@rondolino.de")
        loggin_password_field.send_keys("SS!rondo924p")
        loggin_password_field.send_keys(Keys.RETURN)
    except:
        # Print a message if login fields are not found
        print("Login fields not found, skipping login step.")
    
    # Fill in the form fields with data from the provided array
    name_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'name'))
    )
    name_field.send_keys(data_array[0])

    adress_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Google Maps"]'))
    )
    adress_field.send_keys(data_array[1])

    telephone_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'telephone'))
    )
    telephone_field.send_keys(data_array[2])

    mobile_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'mobile'))
    )
    mobile_field.send_keys(data_array[3])

    email_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'email'))
    )
    email_field.send_keys(data_array[4])

    lieferadresse_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Google Maps Bauvorhaben"]'))
    )
    lieferadresse_field.send_keys(data_array[6])

    auftragsNr_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Auftrags-Nr."]'))
    )
    auftragsNr_field.send_keys(data_array[5])

    auftragsbez_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Auftragsbez."]'))
    )
    auftragsbez_field.send_keys(auftragsNr_stg)

    # Wait for the textarea field to be visible and fill it
    textarea_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'textarea[placeholder="Anmerkungen"]'))
    )
    textarea_field.send_keys(textarea_data)

    # Wait for a few seconds to ensure the form submission is processed
    sleep(5)

    # Wait for the submit button to be clickable and click it
    #button = WebDriverWait(driver, 20).until(
    #   EC.element_to_be_clickable((By.XPATH, '//button[@class="el-button el-button--primary el-button--default"]//span[contains(text(), "Auftrag erstellen")]'))
    #)
    #button.click()

    # Wait for a few seconds to ensure the form submission is processed
    #sleep(5)

root = tk.Tk()
root.withdraw()
article_numbers_string, field_values, articles_cleaned_content = open_pdf()
words = article_numbers_string.split(',')
cleaned_words = [word for word in words if word]  # Remove empty strings
article_numbers_string = ','.join(cleaned_words)
print("Article Numbers:", article_numbers_string)
print("Field Values:", field_values)
print("Articles Cleaned CSV Content:\n", articles_cleaned_content)

data_array = field_values
auftragsNr_stg = field_values[0] + ": " + article_numbers_string 
textarea_data = articles_cleaned_content

webcontrole(data_array,auftragsNr_stg,textarea_data)