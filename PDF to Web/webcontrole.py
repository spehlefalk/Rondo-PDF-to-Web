# Import necessary modules from Selenium and standard libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep

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
    
    # Specify the path to the ChromeDriver executable
    chromedriver_path = os.path.join(current_dir, 'chromedriver.exe')
    
    # Create a Chrome service
    service = Service(chromedriver_path)
    
    # Initialize the Chrome driver with the options
    driver = webdriver.Chrome(service=service, options=options)
    
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
    adress_field.send_keys

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
       # EC.element_to_be_clickable((By.XPATH, '//button[@class="el-button el-button--primary el-button--default"]'))
    #)
    #button.click()

    # Wait for a few seconds to ensure the form submission is processed
    #sleep(5)

