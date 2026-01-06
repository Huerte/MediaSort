from pathlib import Path
import random
import string
import json
from time import time

TOTAL_FILES = 5               
TOTAL_FOLDERS = 3
MAX_NEST_DEPTH = 2
RANDOM_SEED = int(time())
random.seed(RANDOM_SEED)

BASE = Path(f"TestFolder{RANDOM_SEED}")

with open("config.json", "r") as f:
    FILE_MAP = json.load(f)["folders"]

EDGE_CASE_EXTS = [".TXT", ".Mp3", ".Pdf", ".JpEg"]
UNKNOWN_EXTS = [".weird", ".data", ".bin", ".unknown"]
DUPLICATE_NAMES = ["report", "final", "backup", "new", "copy", "copy(1)"]

ALL_EXTS = (
    [e for exts in FILE_MAP.values() for e in exts]
    + EDGE_CASE_EXTS
    + UNKNOWN_EXTS
)

INVALID_CHARS = '<>:"/\\|?*'

def sanitize(name: str) -> str:
    for ch in INVALID_CHARS:
        name = name.replace(ch, "_")
    return name

def rand_name(n=8):
    return "".join(random.choices(string.ascii_lowercase, k=n))

def rand_folder_name():
    garbage = [
        "stuff", "old", "new", "temp", "misc",
        "backup_old", "backup_final_final"
    ]
    return random.choice(garbage + [rand_name(5)])

def make_file(folder: Path, name: str, ext: str):
    path = folder / f"{sanitize(name)}{sanitize(ext)}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"Dummy content for {path.name}")

def random_path(base: Path):
    p = base
    for _ in range(random.randint(0, MAX_NEST_DEPTH)):
        p /= rand_folder_name()
    return p

BASE.mkdir(exist_ok=True)

all_folders = [BASE]
for _ in range(TOTAL_FOLDERS):
    p = random_path(BASE)
    p.mkdir(parents=True, exist_ok=True)
    all_folders.append(p)

print(f"{len(all_folders)} folders created")

files_created = 0

def can_create():
    return files_created < TOTAL_FILES

while can_create():
    folder = random.choice(all_folders)
    make_file(
        folder,
        random.choice(DUPLICATE_NAMES + [rand_name()]),
        random.choice(ALL_EXTS)
    )
    files_created += 1

print(f"{files_created} files created total ✅")
print(f"Test structure at: {BASE.resolve()}")
