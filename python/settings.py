import tkinter as tk
from tkinter import filedialog
import json
import os

def load_json():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as json_file:
            data = json.load(json_file)
            email_entry.insert(0, data.get("email", ""))
            password_entry.insert(0, data.get("password", ""))
            path_entry.insert(0, data.get("Pfad", ""))
    else:
        status_label.config(text="Keine vorhandene JSON-Datei gefunden.")

def save_json():
    data = {
        "email": email_entry.get(),
        "password": password_entry.get(),
        "Pfad": path_entry.get()
    }
    with open('config.json', 'w') as json_file:
        json.dump(data, json_file)
    status_label.config(text="Daten wurden gespeichert!")

def choose_directory():
    path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, path)

# Hauptfenster erstellen
root = tk.Tk()
root.title("Settings")

# Email Label und Entry
email_label = tk.Label(root, text="Email:")
email_label.grid(row=0, column=0, padx=10, pady=5)
email_entry = tk.Entry(root, width=50)
email_entry.grid(row=0, column=1, padx=10, pady=5)

# Passwort Label und Entry
password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, width=50, show='*')
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Pfad Label und Entry
path_label = tk.Label(root, text="Pfad:")
path_label.grid(row=2, column=0, padx=10, pady=5)
path_entry = tk.Entry(root, width=50)
path_entry.grid(row=2, column=1, padx=10, pady=5)

# Pfad auswählen Button
path_button = tk.Button(root, text="Pfad auswählen", command=choose_directory)
path_button.grid(row=2, column=2, padx=10, pady=5)

# Speichern Button
save_button = tk.Button(root, text="Speichern", command=save_json)
save_button.grid(row=3, column=1, pady=20)

# Status Label
status_label = tk.Label(root, text="")
status_label.grid(row=4, column=0, columnspan=3)

# JSON-Datei laden und Felder setzen
load_json()

root.mainloop()
