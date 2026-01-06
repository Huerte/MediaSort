# MediaSort

MediaSort is a CLI-based tool designed to organize your files into categorized folders automatically. It keeps your directories clean by sorting files based on their extensions.

## Features

- **Automated Organization**: Sorts files into predefined categories like Music, Videos, Pictures, Documents, etc.
- **Customizable**: Add or remove file extensions and folder categories via the settings menu.
- **Undo Functionality**: Revert changes if you're not satisfied with the sorting result.
- **Deep Search**: Option to scan and sort files recursively through subfolders.
- **Safety**: Handles duplicate file names and allows for "Safe Mode" (Copy) or "Move" operations.
- **Cross-Platform**: Works on Windows and Linux.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/MediaSort.git
   cd MediaSort
   ```

2. Ensure Python 3 is installed.

3. **Linux Users**: This application requires `tkinter` for folder selection dialogs.
   ```bash
   sudo apt-get install python3-tk
   ```

## Usage

Run the main script to start the application:

```bash
python src/main.py
```

Follow the on-screen menu instructions:
1. **Start Application**: Select the target folder you want to organize.
2. **Undo All Changes**: Revert the last organization operation.
3. **Settings**: Configure folder mappings and advanced options.

## structure

```
MediaSort/
├── src/
│   ├── core/           # Core logic for organization
│   ├── utils/          # Helper utilities (file ops, settings, UI)
│   └── main.py         # Entry point
├── config.json         # User configuration (generated on first run)
├── .gitignore
└── README.md
```

## License

[MIT License](LICENSE)
