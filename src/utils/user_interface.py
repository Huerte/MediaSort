import os
import sys

IS_WINDOWS = os.name == "nt"

def clear_screen():
    os.system("cls" if IS_WINDOWS else "clear")


def ask_folder():
    try:
        from tkinter import Tk, filedialog
    except ImportError:
        raise RuntimeError("tkinter is not installed")

    if IS_WINDOWS:
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass 

    root = Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    root.destroy()
    return path


def ask_yes_no(prompt):
    user_prompt = input(f"\n{prompt}\n>> ").strip().lower()
    if user_prompt != "y":
        clear_screen()
        print("\nUser cancelled the operation\n")
        return False
    return True


def wait_for_enter(prompt='\nEnter any key to exit....'): 
    input(f'\n{prompt}') 
    clear_screen()