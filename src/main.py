from utils.settings import configure_settings
from utils.file_operations import undo_changes
from utils.user_interface import clear_screen, ask_yes_no
from core.organizer import organized_files


if __name__ == '__main__':
    prompt = ''
    while True:
        clear_screen()
        print(f"""{'=' * 40}
\t\tMediaSort
{'=' * 40}
[1] Start Application
[2] Undo All Changes
[3] Settings
[q] Exit
{'=' * 40}""")
        
        if prompt != '':
           print(prompt)
           print('=' * 40)
        
        user_choice = input(">> ").lower()
        
        if user_choice == '1':
           organized_files()
        elif user_choice == '2':
           clear_screen()
           if not ask_yes_no('Are you sure you want to undo changes? (y/N)'):
              continue
           clear_screen()
           undo_changes()
        elif user_choice == '3':
           configure_settings()
        elif user_choice == 'q':
           clear_screen()
           if not ask_yes_no('Are you sure you want to exit? (y/N)'):
              continue
           clear_screen()
           print(f"\n{'=' * 40}\nPrograms exited successfully\n{'=' * 40}\n")
           break
        else:
           prompt = 'Invalid choice. Choose Between 1-3'
