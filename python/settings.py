import tkinter as tk
from tkinter import filedialog, messagebox, Text
import json
import os
import shutil
import webbrowser

def load_json():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as json_file:
            data = json.load(json_file)
            email_entry.insert(0, data.get("email", ""))
            password_entry.insert(0, data.get("password", ""))
            path_entry.insert(0, data.get("Pfad", ""))
            autosave_var.set(data.get("autosave", False))
            notes_var.set(data.get("notes", False))
    else:
        status_label.config(text="Keine vorhandene JSON-Datei gefunden.")

def save_json():
    data = {
        "email": email_entry.get(),
        "password": password_entry.get(),
        "Pfad": path_entry.get(),
        "autosave": autosave_var.get(),
        "notes": notes_var.get()
    }
    with open('config.json', 'w') as json_file:
        json.dump(data, json_file)
    status_label.config(text="Daten wurden gespeichert!")
    root.destroy()

def choose_directory():
    path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, path)

def upload_file():
    file_path = filedialog.askopenfilename(title="Wählen Sie die Chromedriver-Datei aus", filetypes=[("Exe-Dateien", "*.exe")])
    if file_path:
        try:
            shutil.copy(file_path, os.path.join(os.getcwd(), "chromedriver.exe"))
            status_label.config(text="Chromedriver wurde erfolgreich hochgeladen!")
        except Exception as e:
            status_label.config(text=f"Fehler beim Hochladen: {e}")
def find_chromedriver():
    # Diese Funktion öffnet die offizielle Webseite für den Chromedriver
    webbrowser.open("https://googlechromelabs.github.io/chrome-for-testing/")

    # Chromedriver finden Button
    find_button = tk.Button(root, text="Chromedriver finden", command=find_chromedriver)


def show_help():
    help_window = tk.Toplevel(root)
    help_window.title("Hilfe")

    help_text = (
        "Anleitung zur Ersteinrichtung des Programms:\n\n"
        "1. E-Mail und Passwort eintragen:\n"
        "   - Geben Sie Ihre E-Mail-Adresse und Ihr Passwort in die entsprechenden Felder ein.\n\n"
        "2. Pfad festlegen:\n"
        "   - Wählen Sie den Ordner aus, in dem Sie Aufträge öffnen möchten. Klicken Sie auf 'Pfad auswählen', um den Ordner festzulegen.\n\n"
        "3. Chromedriver herunterladen und hochladen:\n"
        "   - Klicken Sie auf 'Chromedriver finden', um zur offiziellen Webseite zu gelangen.\n"
        "   - Laden Sie den passenden Chromedriver für Windows 64-Bit herunter.\n"
        "   - Klicken Sie im Programm auf 'Chromedriver hochladen' und wählen Sie die heruntergeladene .exe-Datei aus.\n\n"
        "4. Autosave aktivieren:\n"
        "   - Aktivieren Sie die Option 'Autosave', um den Input, den Sie im Browser vornehmen, automatisch zu speichern.\n\n"
        "5. Anmerkungen hinzufügen (optional):\n"
        "   - Falls erforderlich, können Sie zusätzliche Anmerkungen oder Links im entsprechenden Feld speichern.\n\n"
        "6. Einstellungen speichern:\n"
    "   - Nachdem Sie alle Einstellungen vorgenommen haben, klicken Sie auf 'Speichern', um die Konfigurationen zu sichern.\n\n"
        "Offizielle Webseite für Chromedriver: https://googlechromelabs.github.io/chrome-for-testing/"

    )

    text_widget = Text(help_window, wrap="word", height=25, width=70)
    text_widget.insert(tk.END, help_text)
    text_widget.config(state=tk.DISABLED)
    text_widget.pack(padx=10, pady=10)

def on_closing():
    if autosave_var.get():
        save_json()
    else:
        root.destroy()

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

# Autosave Checkbox
autosave_var = tk.BooleanVar()
autosave_check = tk.Checkbutton(root, text="Autosave", variable=autosave_var)
autosave_check.grid(row=3, column=1, padx=10, pady=5)

# Separate Notizen Checkbox
notes_var = tk.BooleanVar()
notes_check = tk.Checkbutton(root, text="Anmerkung/Link", variable=notes_var)
notes_check.grid(row=4, column=1, padx=10, pady=5)

# Datei hochladen Button
upload_button = tk.Button(root, text="Chromedriver hochladen", command=upload_file)
upload_button.grid(row=5, column=1, padx=10, pady=5)

# Chromedriver finden Button
find_button = tk.Button(root, text="Chromedriver finden", command=find_chromedriver)
find_button.grid(row=5, column=2, padx=10, pady=5)

# Hilfe Button
help_button = tk.Button(root, text="Hilfe", command=show_help)
help_button.grid(row=6, column=0, padx=10, pady=5)

# Speichern Button
save_button = tk.Button(root, text="Speichern", command=save_json)
save_button.grid(row=6, column=1, pady=20)

# Status Label
status_label = tk.Label(root, text="")
status_label.grid(row=7, column=0, columnspan=3)

# JSON-Datei laden und Felder setzen
load_json()

# Set up the auto-save on closing the window
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
