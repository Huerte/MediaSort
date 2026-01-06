from utils.user_interface import clear_screen, ask_yes_no
from utils.validation import valid_extension, validate_folder_name
from pathlib import Path
import json
from sys import stdout


DEFAULT_CONFIG = {
    "folders": {
        "Music":        [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
        "Videos":       [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
        "Pictures":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg", ".heic"],
        "Documents":    [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"],
        "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods", ".json", ".xml"],
        "Presentations":[ ".ppt", ".pptx", ".odp"],
        "Archives":     [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
        "Installers":   [".exe", ".msi", ".apk", ".dmg", ".pkg", ".appimage"],
        "Code":         [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".cs", ".php", ".go", ".rs", ".sh", ".ps1"],
        "Fonts":        [".ttf", ".otf", ".woff", ".woff2"],
        "DiskImages":   [".iso", ".img", ".vhd", ".vmdk"],
        "Temp":         [".log", ".tmp", ".part", ".cache", ".bak"],
    },
    "deep_search": True,
    "extension_folders": True,
    "preserved_files": True,
    "delete_empty_dir": True,
    "within_target_dir": False,
}

APP_DIR = Path().parent.joinpath(Path(".mediasort"))
APP_DIR.mkdir(exist_ok=True)

# Load configuration Structure
CONFIG_PATH = Path('config.json')

if CONFIG_PATH.exists():
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        config = DEFAULT_CONFIG
else:
    config = DEFAULT_CONFIG
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

FOLDERS = config.get('folders') or DEFAULT_CONFIG['folders']
EXTENSION_FOLDER  = config.get('extension_folders', DEFAULT_CONFIG['extension_folders'])
DEEP_SEARCH       = config.get('deep_search', DEFAULT_CONFIG['deep_search'])
PRESERVE_FILE     = config.get('preserved_files', DEFAULT_CONFIG['preserved_files'])
DELETE_EMPTY_DIR  = config.get('delete_empty_dir', DEFAULT_CONFIG['delete_empty_dir'])
WITHIN_TARGET_DIR = config.get('within_target_dir', DEFAULT_CONFIG['within_target_dir'])


EXT_TO_FOLDER = {}
for folder, extensions in FOLDERS.items():
    for ext in extensions:
        if ext.lower() in EXT_TO_FOLDER:
            raise ValueError(f"Duplicate extensions exists {ext.lower()}")
        EXT_TO_FOLDER[ext.lower()] = folder


def display_main_menu():
    clear_screen()
    print(f"""{'=' * 40}
       MediaSort CONFIGURATION TOOL
{'=' * 40}
[1] Folder Mapping
[2] Change Location: [{'Sort In-Place' if WITHIN_TARGET_DIR else 'Create Separate Folder'}]
[3] Advanced Settings
[4] Reset All to Defaults
[5] Save Changes
[q] Back
{'=' * 40}""")


def add_extension(folder):
    global FOLDERS
    prompt = ''
    while True:
        clear_screen()
        print('=' * 40)
        if prompt != '':
            print(prompt)

        print('Type extension to add. Type "q" to exit.')
        print('=' * 40)

        new_extension = input('>> ').lower().strip()
        prompt = ''

        if new_extension == 'q':
            break

        if new_extension[0] != '.':
            new_extension = f'.{new_extension}'
        
        if valid_extension(extension=new_extension):
            FOLDERS[folder].append(new_extension)
            break
        else:
            prompt = f"Invalid extension: '{new_extension}'"

def remove_extension(folder):
    global FOLDERS
    file_extensions = FOLDERS[folder]
    prompt = ''
    user_choice = ''
    clear_screen()
    print(f'Choose Between 1-{len(file_extensions)}. Type "q" to exit')
    while True:
        print('=' * 40)
        print("\n".join([f"[{i + 1}] {extension}" for i, extension in enumerate(file_extensions)]))
        print("\n[q] Back\n")
        print('=' * 40)

        if prompt != '':
            print(prompt)

        user_choice = input('>> ').lower().strip()
        prompt = ''

        if user_choice == 'q':
            break

        if user_choice.isdigit() and int(user_choice) > 0 and int(user_choice) <= len(file_extensions):
            file_extensions.pop(int(user_choice) - 1)
            FOLDERS[folder] = file_extensions
            break
        else:
            prompt = f'Invalid choice. Choose between 1-{len(file_extensions)}'

        clear_screen()

def edit_folder(folder):
    global FOLDERS
    extensions = FOLDERS[folder]
    user_choice = ''
    prompt = ''
    while True:
        clear_screen()
        print(f"""{'=' * 40}\n--- EDITING: {folder} ---\n{'=' * 40}\n
Current Extensions: {', '.join(extensions)}
{prompt if prompt != '' else ''}
[1] Add New Extension
[2] Remove an Extension
[3] Delete this Category (Delete '{folder}' mapping)
[q] Back""")
        
        user_choice = input(">> ").lower()
        prompt = ''

        if user_choice == '1':
            add_extension(folder=folder)
        elif user_choice == '2':
            remove_extension(folder=folder)
        elif user_choice == '3':
            clear_screen()
            if ask_yes_no("Are you sure you want to stop sorting files into 'Music'? (y/n)"):
                del FOLDERS[folder]
                break
            else:
                prompt = 'Deletion of this folder cancelled by the user.'
        elif user_choice == 'q':
            break
        else:
            prompt = 'Invalid choice. Pick between 1-3'

def add_new_folder():
    global FOLDERS
    prompt = ''
    new_folder = ''
    while True:
        clear_screen()
        print('=' * 55)
        if prompt != '':
            print(prompt)

        print('Type the folder name to be added. Type "q" to exit.')
        print('=' * 55)

        new_folder = input('>> ').strip()
        prompt = ''

        if new_folder == 'q':
            break

        try:
            folder_name = validate_folder_name(new_folder)
            FOLDERS[folder_name] = []
            break
        except ValueError as e:
            prompt = f"Invalid folder name: {e}"

def map_folder():
    global FOLDERS
    folders = list(FOLDERS.keys())
    user_choice = ''
    prompt = ''
    while True:
        clear_screen()

        print(f"""{'=' * 40}\n--- FOLDER MAPPING ---\n{'=' * 40}\n
{'\n'.join([f'{i + 1} {folder}' for i, folder in enumerate(folders)])}

[a] Add New Folder Category
[q] Back to Main Menu""")
        
        if prompt != '':
            print(prompt)

        user_choice = input(">> ").lower()
        prompt = ''

        if user_choice.isdigit() and int(user_choice) > 0 and int(user_choice) <= len(folders):
            edit_folder(folder=folders[int(user_choice) - 1])
            folders = list(FOLDERS.keys())
        elif user_choice == 'a':
            add_new_folder()
            folders = list(FOLDERS.keys())
        elif user_choice == 'q':
            break
        else:
            prompt = f'Invalid choice. Pick between 1-{len(folders)} and a or q'

    config['folders'] = FOLDERS


def advance_settings():
    user_choice = ''
    prompt = ''
    while True:
        global DEEP_SEARCH, EXTENSION_FOLDER, PRESERVE_FILE, DELETE_EMPTY_DIR
        clear_screen()
        print(f"""{'=' * 40}\n--- ADVANCED SETTINGS ---\n{'=' * 40}\n
[1] Scan all subfolders?          [{'YES' if DEEP_SEARCH else 'NO'}]
[2] Sub-divide by extension?      [{'YES' if EXTENSION_FOLDER else 'NO'}]
[3] Action:                       [{'COPY' if PRESERVE_FILE else 'MOVE'}]
[4] Remove empty folders?         [{'YES' if DELETE_EMPTY_DIR else 'NO'}]
[q] Back""")
        if prompt != '':
            print(prompt)

        user_choice = input(">> ").lower()
        prompt = ''
        if user_choice == '1':
            DEEP_SEARCH = not DEEP_SEARCH
            config['deep_search'] = DEEP_SEARCH
        elif user_choice == '2':
            EXTENSION_FOLDER = not EXTENSION_FOLDER
            config['extension_folders'] = EXTENSION_FOLDER
        elif user_choice == '3':
            PRESERVE_FILE = not PRESERVE_FILE
            config['preserved_files'] = PRESERVE_FILE
        elif user_choice == '4':
            DELETE_EMPTY_DIR = not DELETE_EMPTY_DIR
            config['delete_empty_dir'] = DELETE_EMPTY_DIR
        elif user_choice == 'q':
            break
        else:
            prompt = 'Invalid choice. Pick between 1-4'


def reset_to_defaults():
    with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
        json.dump(DEFAULT_CONFIG, file, indent=4)


def configure_settings():
    user_choice = ''
    prompt = ''
    while True:
        display_main_menu()

        if prompt != '':
            print(prompt)

        user_choice = input(">> ").lower()
        prompt = ''
        if user_choice == '1':
            map_folder()
        elif user_choice == '2':
            global WITHIN_TARGET_DIR

            WITHIN_TARGET_DIR = not WITHIN_TARGET_DIR
            config['within_target_dir'] = WITHIN_TARGET_DIR
        elif user_choice == '3':
            advance_settings()
        elif user_choice == '4':
            reset_to_defaults()
        elif user_choice == '5':
            with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
                json.dump(config, file, indent=4)
            prompt = 'New settings successfully saved'
        elif user_choice == 'q':
            break
        else:
            prompt = 'Invalid choice. Pick between 1-5'
