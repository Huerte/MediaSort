from utils.user_interface import ask_yes_no, ask_folder, wait_for_enter, clear_screen
from utils.file_operations import organize_files, collect_files, cleanup_empty_folders
from utils.settings import Path, configure_settings
from sys import exit


def view_valid_files(file_paths):
    if not file_paths:
        print('No Files Found')
    else:
        for i in range(len(file_paths)):
            print(f'~ {file_paths[i].name}')
    wait_for_enter()

def view_skipped_files(file_paths):
    if not file_paths:
        print('No Skipped Files Found')
    else:
        for path, reason in file_paths.items():
            print(f'{path} - REASON: {reason}')
    wait_for_enter()

def organized_files():

    TARGET = ask_folder()

    if TARGET.strip() == '':
        print('ERROR: No target folder found')
        wait_for_enter()
        return

    target_path = Path(TARGET)

    # Get all file in all sections
    all_files, skipped_items = collect_files(target_path=target_path)
    prompt = ''
    while True:
        clear_screen()

        print('=' * 40)
        print(f'Valid Files       : {len(all_files)}')
        print(f'Skipped Files     : {len(skipped_items)}')
        print(f'Total Files Found : {len(all_files) + len(skipped_items)}')
        print(f'Source Path      : {target_path}')
        print('=' * 40)

        if prompt != '':
            print(prompt)
            print('=' * 40)

        print("""[1] Organized Files
[2] View valid files
[3] View skipped files
[4] Settings
[q] Exit Program""")
        
        user_choice = input(">> ").lower()
        clear_screen()
        prompt = ''

        if user_choice == '1':
            if not ask_yes_no('Are you sure you want to proceed the process? (y/N)'):
                clear_screen()
                print('User Cancelled Operation')
                wait_for_enter('Press Enter to continue...')
                continue
            break
        elif user_choice == '2':
            view_valid_files(all_files)
        elif user_choice == '3':
            view_skipped_files(skipped_items)
        elif user_choice == '4':
            configure_settings()
        elif user_choice == 'q':
            return
        else:
            prompt = 'Invalid Choice. Please choose between 1-4 (q to exit)'

    clear_screen()
    undo_log, file_counts_per_folder = organize_files(file_paths=all_files, target_path=target_path)

    import json
    from utils.settings import WITHIN_TARGET_DIR, APP_DIR, DELETE_EMPTY_DIR

    UNDO_FILE_PATH = APP_DIR.joinpath(Path(f"undo.json"))
    with open(UNDO_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(undo_log, file, indent=4)
    
    if DELETE_EMPTY_DIR:
        cleanup_empty_folders(target_path=target_path)
    
    wait_for_enter('Progress Success. Enter to proceed to report...')

    max_folder_name = max(list(file_counts_per_folder.keys()), key=len)

    print(f"""{'=' * 40}
MediaSort REPORT
{'=' * 40}

SUCCESSFULL: {len(all_files) - 0}           FAILED: {0}

{'=' * 40}
{'\n'.join([f'{folder}{' ' * abs(len(max_folder_name) - len(folder))} : {file_counts}' for folder, file_counts in file_counts_per_folder.items()])}
{'=' * 40}

FULL DIRECTORY PATH: {target_path if WITHIN_TARGET_DIR else f'{target_path}(Copy)'}
""")
    
    wait_for_enter()