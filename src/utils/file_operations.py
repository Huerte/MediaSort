import shutil
from utils.settings import *
from yaspin import yaspin
from datetime import datetime, timezone
from utils.user_interface import wait_for_enter


def is_folder_empty(folder):
    return not any(folder.iterdir())

def scan_recursive(folder):
    if folder.is_file():
        return [folder], [], []
    
    files, skipped_files, folders = [], [], []
    for sub_content in folder.iterdir():
        try:
            if sub_content.is_dir():
                folders.append(sub_content)
                file, sub_skipped, sub_folder = scan_recursive(folder=sub_content)
                files.extend(file)
                folders.extend(sub_folder)
                skipped_files.extend(sub_skipped)
            elif sub_content.is_file():
                files.append(sub_content)
            else:
                skipped_files.append({
                    'path': sub_content,
                    'reason': 'Not a regular file'
                })
        except PermissionError:
            skipped_files.append({'path': sub_content, 'reason': 'Permission Denied'})     
        except OSError as e:
            skipped_files.append({'path': sub_content, 'reason': f'OS Error: {e}'})

    return files, skipped_files, folders

def safe_copy(file, path):

    if not path.exists():
        path.mkdir(exist_ok=True)
    
    file_path = path.joinpath(file.name)

    if file_path.exists():
        file_name = file.stem
        file_extension = file.suffix
        counter = 1

        while True:
            new_file_name = f'{file_name}({counter}){file_extension}'
            file_path = path.joinpath(new_file_name)
            if not file_path.exists():
                break
            counter += 1

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": "copy",
        "src": str(file),
        "dst": str(file_path),
        "success": False,
        "reason": None
    }

    try:
        shutil.copy2(file, file_path)
        entry["success"] = True
    except PermissionError:
        entry["reason"] = "Permission denied"
    except OSError as e:
        entry["reason"] = str(e)

    return entry

 
def collect_files(target_path):
    file_paths = []
    skipped_items  = []
    with yaspin('Collecting all files....', color='cyan') as spinner:
        try:
            for content in target_path.iterdir():
                try:
                    if content.is_file():
                        file_paths.append(content)
                    elif content.is_dir():
                        if DEEP_SEARCH:
                            file, sub_skipped, _ = scan_recursive(content)
                            file_paths.extend(file)
                            skipped_items.extend(sub_skipped)
                    else:
                        skipped_items.append({
                        'path': content,
                        'reason': 'Not a regular file'
                    })
                except PermissionError:
                    skipped_items.append({'path': content, 'reason': 'Permission Denied'})     
                except OSError as e:
                    skipped_items.append({'path': content, 'reason': f'OS Error: {e}'})

                spinner.text = f'Collecting all files: {len(file_paths)}'
        except PermissionError:
            spinner.fail('❌')
            spinner.text = f"CRITICAL ERROR: No permission to read folder {target_path}"
        except Exception as e:
            spinner.fail('❌')
            spinner.text = f'Error while collecting files: \n{e}'

        spinner.ok('✅')
        
    return file_paths, skipped_items 

def cleanup_empty_folders(target_path):
    successfully_deleted = 0
    with yaspin('Deleting empty folders...', color='cyan') as spinner:
        try:
            for i, content in enumerate(target_path.iterdir()):
                if content.is_dir():
                    if is_folder_empty(content):
                        shutil.rmtree(content)
                        successfully_deleted += 1
                        spinner.text = f'Deleted empty folders: {successfully_deleted}'
                    else:
                        for folder in scan_recursive(content)[-1][::-1]:
                            if is_folder_empty(folder=folder):
                                shutil.rmtree(folder)
                                successfully_deleted += 1
                            spinner.text = f'Deleted empty folders: {successfully_deleted}'
                        if is_folder_empty(folder=content):
                            shutil.rmtree(content)
                            successfully_deleted += 1
                            spinner.text = f'Deleted empty folders: {successfully_deleted}'

            # Delete the parent folder if empty
            if is_folder_empty(target_path):
                shutil.rmtree(target_path)
                successfully_deleted += 1

        except Exception as e:
            spinner.fail('❌')
            spinner.text = f'Error during folder deletion: \n{e}'

        spinner.text = f'{successfully_deleted} empty folders deleted successfully'
        spinner.ok('✅')

    return successfully_deleted

def organize_files(file_paths, target_path):
    file_counts = {}

    undo_log = {
        "target path": str(target_path),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "operations": []
    }

    if not WITHIN_TARGET_DIR:
        CONTAINER_DIR = f'{target_path.name}(Copy)'
        for i in range(0, 10_000):
            candidate_dir = f'{CONTAINER_DIR}({i})' if i > 0 else CONTAINER_DIR
            if not Path(candidate_dir).exists():
                CONTAINER_DIR = candidate_dir
                break
                

    with yaspin('Processing items...', color='cyan') as spinner:
        for i, file in enumerate(file_paths):
            if file.suffix.lower() not in EXT_TO_FOLDER.keys():
                folder = 'Others'
            else:
                folder = EXT_TO_FOLDER[file.suffix.lower()]

            # Create the extension main Folder
            if WITHIN_TARGET_DIR:
                complete_path = target_path.joinpath(Path(folder))
                complete_path.mkdir(exist_ok=True)
            else:
                try:
                    container_dir = target_path.parent.joinpath(Path(CONTAINER_DIR))
                    container_dir.mkdir(exist_ok=True)
                except Exception as e:
                    print(f'Error in container_dir {container_dir}')

                try:
                    complete_path = container_dir.joinpath(Path(folder))
                    complete_path.mkdir(exist_ok=True)
                except Exception as e:
                    print(f'Error in complete_path {complete_path}')

            try:
                if EXTENSION_FOLDER:
                    try:
                        sub_path = complete_path.joinpath(Path(file.suffix.lower()[1:]))
                        sub_path.mkdir(exist_ok=True)
                        undo_log['operations'].append(safe_copy(file, sub_path))
                    except Exception as e:
                        print(f"Error Detected: {file} {sub_path}")
                else:
                    undo_log['operations'].append(safe_copy(file, complete_path))
                
                if not PRESERVE_FILE:
                    Path(file).unlink(missing_ok=True)

                file_counts[folder] = file_counts.get(folder, 0) + 1
                spinner.text = f'Processing items: {i + 1}'

            except Exception as e:
                spinner.fail('❌')
                spinner.text = f'ERROR: {e}'

        spinner.text = f'{len(file_paths)} files are successfully processed'
        spinner.ok('✅')

    return undo_log, file_counts

def load_json_file(file_path):
    if not file_path.exists():
        return {}
    
    import json
    data = {}
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)

    return data


def undo_changes():
    try:
        undo_log = load_json_file(APP_DIR.joinpath(Path('undo.json')))
    except Exception as e:
        print(f'LOAD_JSON_FILE ERROR: \n\t\t{e}')
        wait_for_enter()
    if not undo_log or len(undo_log.get('operations', [])) == 0:
        print(f"Undo Log is empty {undo_log}")
        wait_for_enter()
        return False
    
    # entry = {
    #     "ts": datetime.now(timezone.utc).isoformat(),
    #     "action": "copy",
    #     "src": str(file),
    #     "dst": str(file_path),
    #     "success": False,
    #     "reason": None
    # }

    try:
        with yaspin('Undoing All Moved Files....', color='cyan') as spinner:
            for i, item in enumerate(undo_log['operations']):
                data = {}
                for label, val in list(item.items())[2:-1]:
                    data[label] = val
                
                src_path = data['src']
                safe_copy(Path(data['dst']), Path(src_path.replace(Path(src_path).name, '')))
                spinner.text = f'Undoing All Moved Files: {i}'
            
            spinner.ok('✅')
            spinner.text = 'Successfully Undo Changes'
    except Exception as e:
        wait_for_enter(f'{e} ERROR: ')     
    wait_for_enter()
