import requests
import os
import subprocess
import winreg
import sys
import tempfile
import traceback
import zipfile
import shutil
import json

class NiniteLike:
    def __init__(self):
        self.apps = {}
        self.temp_dir = tempfile.mkdtemp()
        self.portable_dir = os.path.join(os.path.expanduser("~"), "PortableApps")
        if not os.path.exists(self.portable_dir):
            os.makedirs(self.portable_dir)
        self.load_apps_from_github()

    def load_apps_from_github(self):
        github_raw_url = "https://raw.githubusercontent.com/yourusername/yourrepository/main/apps.json"
        try:
            response = requests.get(github_raw_url)
            response.raise_for_status()
            self.apps = json.loads(response.text)
            print("Liste des applications mise à jour avec succès depuis GitHub.")
        except requests.RequestException as e:
            print(f"Erreur lors de la mise à jour de la liste des applications : {e}")
            print("Utilisation de la liste des applications par défaut.")
            # Ici, vous pouvez ajouter une liste par défaut au cas où la connexion échoue
        self.apps = {
            "ccleaner": {
                "name": "CCleaner",
                "url": "https://download.ccleaner.com/ccsetup.exe",
                "filename": "ccsetup.exe",
                "silent_args": "/S",
                "type": "install"
            },
            "7zip": {
                "name": "7-Zip",
                "url": "https://www.7-zip.org/a/7z2201-x64.exe",
                "filename": "7z2201-x64.exe",
                "silent_args": "/S",
                "type": "install"
            },
            "notepadplusplus_portable": {
                "name": "Notepad++ Portable",
                "url": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.5.4/npp.8.5.4.portable.x64.zip",
                "filename": "npp.8.5.4.portable.x64.zip",
                "type": "portable_zip",
                "extract_dir": "Notepad++"
            },
            "adwcleaner_portable": {
                "name": "Adwcleaner",
                "url": "https://adwcleaner.malwarebytes.com/adwcleaner?channel=release",
                "type": "portable_exe",
                "filename": "adwcleaner.exe",
                "extract_dir": "Adwcleaner"
            },
            "malwarebytes": {
                "name": "Malwarebytes",
                "url": "https://downloads.malwarebytes.com/file/mb5_offline",
                "filename": "mb4_offline.exe",
                "silent_args": "/VERYSILENT /NORESTART",
                "type": "install"
            },
            "avast": {
                "name": "Avast Free Antivirus",
                "url": "https://www.avast.com/en-us/download-thank-you.php?product=FAV-AVAST&locale=en-us&direct=1",
                "filename": "avast_free_antivirus_setup_online.exe",
                "silent_args": "/silent",
                "type": "install"
            },
            "bitdefender": {
                "name": "Bitdefender Antivirus Free",
                "url": "https://download.bitdefender.com/windows/installer/en-us/bitdefender_antivirus.exe",
                "filename": "bitdefender_antivirus.exe",
                "silent_args": "/SILENT",
                "type": "install"
            },
            "glasswire": {
                "name": "GlassWire",
                "url": "https://download.glasswire.com/GlassWireSetup.exe",
                "filename": "GlassWireSetup.exe",
                "silent_args": "/S",
                "type": "install"
            },
            "bleachbit": {
                "name": "BleachBit",
                "url": "https://download.bleachbit.org/BleachBit-4.6.0-portable.zip",
                "filename": "BleachBit-4.6.0-portable.zip",
#                "silent_args": "/S",
                "type": "portable_zip",
                "extract_dir": "Bleachbit"
            },
            "windirstat": {
                "name": "WinDirStat",
                "url": "https://windirstat.net/wds_current_setup.exe",
                "filename": "wds_current_setup.exe",
                "silent_args": "/S",
                "type": "install"
            },
            "autoruns_portable": {
                "name": "Autoruns",
                "url": "https://download.sysinternals.com/files/Autoruns.zip",
                "filename": "Autoruns.zip",
                "type": "portable_zip",
                "extract_dir": "Autoruns"
            }
        }

    def download_app(self, app_name):
        app = self.apps.get(app_name)
        if not app:
            print(f"L'application {app_name} n'est pas disponible.")
            return False

        print(f"Téléchargement de {app['name']}...")
        try:
            response = requests.get(app['url'], timeout=30)
            response.raise_for_status()
            file_path = os.path.join(self.temp_dir, app['filename'])
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"{app['name']} téléchargé avec succès.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors du téléchargement de {app['name']}: {e}")
            return False

    def install_app(self, app_name):
        app = self.apps.get(app_name)
        if not app:
            print(f"L'application {app_name} n'est pas disponible.")
            return

        file_path = os.path.join(self.temp_dir, app['filename'])
        if not os.path.exists(file_path):
            print(f"Le fichier pour {app['name']} n'existe pas.")
            return

        if app['type'] == 'install':
            print(f"Installation de {app['name']}...")
            try:
                subprocess.run([file_path, app['silent_args']], check=True, timeout=300)
                print(f"{app['name']} installé avec succès.")
            except subprocess.SubprocessError as e:
                print(f"Erreur lors de l'installation de {app['name']}: {e}")
        elif app['type'] == 'portable_zip':
            print(f"Extraction de {app['name']}...")
            try:
                extract_path = os.path.join(self.portable_dir, app['extract_dir'])
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                print(f"{app['name']} extrait avec succès dans {extract_path}.")
            except zipfile.BadZipFile as e:
                print(f"Erreur lors de l'extraction de {app['name']}: {e}")
        elif app['type'] == 'portable_exe':
            print(f"Copie de {app['name']}...")
            try:
                dest_path = os.path.join(self.portable_dir, app['extract_dir'])
                os.makedirs(dest_path, exist_ok=True)
                shutil.copy2(file_path, os.path.join(dest_path, app['filename']))
                print(f"{app['name']} copié avec succès dans {dest_path}.")
            except shutil.Error as e:
                print(f"Erreur lors de la copie de {app['name']}: {e}")

    def is_app_installed(self, app_name):
        app = self.apps.get(app_name)
        if not app:
            return False

        if app['type'] == 'install':
            try:
                winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app['name']}")
                return True
            except WindowsError:
                return False
        elif app['type'] in ['portable_zip', 'portable_exe']:
            return os.path.exists(os.path.join(self.portable_dir, app['extract_dir'], app['filename']))

    def run(self):
        while True:
            try:
                print("\nBienvenue dans NiniteLike!")
                print("Applications disponibles:")
                app_list = list(self.apps.items())
                for i, (app_key, app_info) in enumerate(app_list, 1):
                    print(f"{i}. {app_info['name']} ({'Portable' if 'portable' in app_info['type'] else 'Installable'})")
                
                print("\nEntrez les numéros des applications à installer/extraire (séparés par des espaces),")
                print("'all' pour toutes les installer, 'update' pour mettre à jour la liste, ou 'q' pour quitter.")
                user_input = input("Votre choix : ").lower()
                
                if user_input == 'q':
                    print("Merci d'avoir utilisé NiniteLike. Au revoir!")
                    break
                elif user_input == 'update':
                    self.load_apps_from_github()
                    continue

                if user_input == 'all':
                    to_install = list(self.apps.keys())
                else:
                    try:
                        selected_numbers = [int(x) for x in user_input.split()]
                        to_install = [app_list[i-1][0] for i in selected_numbers if 1 <= i <= len(app_list)]
                    except ValueError:
                        print("Entrée invalide. Veuillez entrer des numéros, 'all', 'update', ou 'q'.")
                        continue

                for app_name in to_install:
                    if not self.is_app_installed(app_name):
                        if self.download_app(app_name):
                            self.install_app(app_name)
                    else:
                        print(f"{self.apps[app_name]['name']} est déjà installé/extrait.")

                input("Appuyez sur Entrée pour continuer...")

            except Exception as e:
                print(f"Une erreur inattendue s'est produite : {e}")
                print("Détails de l'erreur :")
                traceback.print_exc()
                input("Appuyez sur Entrée pour continuer...")

    def cleanup(self):
        print("Nettoyage des fichiers temporaires...")
        shutil.rmtree(self.temp_dir, ignore_errors=True)

if __name__ == "__main__":
    ninite = NiniteLike()
    try:
        ninite.run()
    finally:
        ninite.cleanup()