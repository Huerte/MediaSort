<div align="center">

# MediaSort

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](#)
[![Platform](https://img.shields.io/badge/platform-Windows%20|%20Linux-blueviolet.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#)

**A CLI tool that automatically organizes your files into categorized folders, keeping your directories clean and clutter-free.**

</div>

---

## Features

MediaSort provides a command-line environment designed for automated file organization.
Built to be fast, flexible, and safe.

- **Automated Organization:** Sorts files into predefined categories like Music, Videos, Pictures, Documents, and more based on file extensions.
- **Customizable:** Add or remove file extensions and folder categories via the built-in settings menu.
- **Undo Functionality:** Reverts the last sorting operation if the result is not satisfactory.
- **Deep Search:** Recursively scans and sorts files through subfolders for thorough organization.
- **Safety Controls:** Handles duplicate file names with support for "Safe Mode" (Copy) or "Move" operations.
- **Cross-Platform:** Works on both Windows and Linux.

---

## Installation Guide

Follow these steps to install MediaSort locally.

### Prerequisites

- **Python 3.x**
- **Linux only: `tkinter`** (for folder selection dialogs)

---

### Step 1: Get the Code

```bash
git clone https://github.com/Huerte/MediaSort.git
cd MediaSort
```

---

### Step 2: Install Dependencies

_No external dependencies required for Windows._

For **Linux** users, install `tkinter`:
```bash
sudo apt-get install python3-tk
```

---

### Step 3: Run

```bash
python src/main.py
```

---

## Usage

1. Run the main script with `python src/main.py`.
2. **Start Application** — Select the target folder you want to organize.
3. **Undo All Changes** — Revert the last organization operation.
4. **Settings** — Configure folder mappings, file extensions, and advanced options.
5. The tool will automatically sort files into their respective category folders.

---

## Project Structure

```
MediaSort/
│
├── src/
│   ├── core/           # Core logic for organization
│   ├── utils/          # Helper utilities (file ops, settings, UI)
│   └── main.py         # Entry point
├── config.json         # User configuration (generated on first run)
├── .gitignore
└── README.md
```

---

## Configuration

Edit the generated configuration file:
```bash
config.json
```

Example:
```json
{
  "categories": {
    "Music": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mkv", ".avi"]
  }
}
```

---

## Contributing

1. Fork the Project
2. Create a Feature Branch
3. Commit Changes
4. Push to Branch
5. Open Pull Request

---

## License

Distributed under the MIT License. See `LICENSE` for details.

---

&copy; 2026 [Huerte](https://github.com/Huerte). All Rights Reserved.
