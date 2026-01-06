import re


def validate_folder_name(name):

    FORBIDDEN_CHARS = r'<>:"/\|?*\0-\31'

    RESERVED_NAMES = {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10))
    }

    name = name.strip()
    if not name:
        raise ValueError("Folder name cannot be empty")
    
    if name.upper() in RESERVED_NAMES:
        raise ValueError(f"'{name}' is a reserved name")
    
    if any(c in FORBIDDEN_CHARS for c in name):
        raise ValueError("Folder name contains invalid characters")
    
    if name.endswith(" ") or name.endswith("."):
        raise ValueError("Folder name cannot end with a space or dot")
    
    if len(name) > 150:
        raise ValueError("Folder name is too long")
    
    return name


def valid_extension(extension):
    EXT_REGEX = re.compile(r"^\.[a-zA-Z0-9]{1,10}(\.[a-zA-Z0-9]{1,10}){0,2}$")

    if not EXT_REGEX.match(extension):
        return False
    
    return True
