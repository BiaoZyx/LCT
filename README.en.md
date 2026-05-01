# LCT - Line Cipher Translator

**Line Cipher Translator** — convert between plain text and line cipher (LC) code, featuring a **Nano‑style full‑screen interface** and a **command‑line one‑shot mode**.

![Version](https://img.shields.io/badge/version-1.3-blue)
![License](https://img.shields.io/badge/license-GPLv3-green)

---

I invented a curious thing called "Line Cipher".

Its hallmark is: **chaos** — yes!  
With this cipher, most people won't be able to understand a thing.

Here's how it works:

1. `-` : horizontal line
2. `|` : vertical line
3. `/` : forward slash (left-leaning)
4. `\` : backward slash (right-leaning)
5. `_` : an arc (a quarter circle)

By decomposing each character into strokes and combining these symbols, I arrived at the Line Cipher. (Don't ask me how I came up with it...)

The v1.0 version was based on the Python code of _MCT-v1.6_.

---

## Features

- Bidirectional translation: text → LC code, LC code → text
- Nano‑style interactive interface (curses‑based):
  - Fixed top title bar and bottom shortcut bar
  - Scrollable content area with automatic separators between commands
  - Colored output, English / Chinese UI support
- One‑shot command‑line mode (ideal for scripts):
  ```bash
  lct -t "HELLO"                # text → LC
  lct -l "|-| ___ |- |- ---"    # LC → text
  lct --dict                    # show colored dictionary
  lct --version                 # version info
  ```
- Complete dictionary: A‑Z, 0‑9 and common punctuation (dynamically generated from `LC_CODE_DICT`)
- Smart color scheme: separate colors for success, errors, hints, separators
- Language switching: interactive choice in full‑screen mode, auto‑detection in one‑shot mode
- Command history: arrow‑key recall, `/history` to list last 20 commands
- Packable into standalone executable (PyInstaller) — no Python required on the target machine

---

## Requirements

- Python 3.8+
- Dependencies (all available via pip or standard library):
  ```bash
  pip install wcwidth
  # On Windows you also need:
  pip install windows-curses
  ```
  Linux/macOS come with `curses`; only `wcwidth` is required.

---

## Quick Start

### Run from source

```bash
git clone https://github.com/BiaoZyx/LCT
cd LCT
python LCT-v1.3.py
```

### Interactive mode

```bash
python LCT-v1.3.py
# Select a language and enter the full‑screen interface.
```

### One‑shot command‑line usage

```bash
python LCT-v1.3.py -t "HELLO"                    # translate text
python LCT-v1.3.py -l "|-| ___ |- |- ---"       # translate LC code
python LCT-v1.3.py --dict                        # print colored dictionary
python LCT-v1.3.py --version                     # show version
python LCT-v1.3.py --lang zh -t "example"        # force Chinese + translate
```

---

## Interactive Commands

Inside the interface, the bottom shortcut bar shows all available commands:

| Command        | Action                      |
| -------------- | --------------------------- |
| `1`            | Text → LC code              |
| `2`            | LC code → Text              |
| `3`            | Display the full dictionary |
| `/menu`        | Show command menu           |
| `/help`        | Detailed help               |
| `/version`     | Version info                |
| `/clear`       | Clear output area           |
| `/history`     | Last 20 commands            |
| `/exit`        | Exit the program            |
| `/egg <color>` | Easter egg (red, green…)    |

---

## Building a standalone executable

Generate a self-contained binary with PyInstaller (no Python needed on the target machine):

```bash
pip install pyinstaller
pyinstaller --onefile LCT-v1.3.py
```

- The binary will be placed in the `dist/` folder.
- You may copy it to a system path (e.g. `/usr/local/bin/lct`) for convenient use.
- **Cross‑platform note**: On Windows, install `windows-curses` before building; the resulting `.exe` will run directly on Windows.

---

## Example

### Interactive interface (Nano style)

```
+----------------------------------------------+
|        LCT v1.3   |   BiaoZyx   |   /help    | (top bar)
+----------------------------------------------+
| Welcome to LCT v1.3                          |
| Type /help for help.                         |
|                                              |
| -------------------------------------------- | (separator)
| >>> command > 1                              |
| >>> text > HELLO                             |
| Translated LC: |-| ___ |- |- ---             |
| -------------------------------------------- |
| >>> command > _                              | (input line)
+----------------------------------------------+
| [1]Text→LC [2]LC→Text [3]Dict [/menu] ...   | (bottom bar)
+----------------------------------------------+
```

### One‑shot output

```
$ lct -t "HELLO" --lang en
Translated LC: |-| ___ |- |- ---
$ lct --dict
[Letters]
A /\-       B |__'__    C ___
...
```

---

## Version History

### v1.3 (2026-05-01)

- Fully rewritten interactive interface using `curses` – fixed top/bottom bars like Nano
- Improved input prompts, now perfectly supports Chinese characters (display width calculated with `wcwidth`)
- Added command echo and output separators
- In-memory command history (extensible to persistent storage)
- One‑shot mode now auto‑detects system language (no language prompt)
- Colored dictionary output in both interactive and script modes
- Fixed `exit` error after packaging with PyInstaller
- Cleaned up unused arguments, refined help output

### v1.2 (2026-04)

- Dynamically generated line cipher dictionary with Chinese/English support
- Fixed dictionary layout and alignment
- Internal refactoring for better maintainability

### v1.0 (2025-08)

- Initial release, REPL interface based on `colorama`
- Basic text ↔ LC code translation

---

## Author

**BiaoZyx**

- Email: BiaoZyx@outlook.com
- Project inspiration: 2025-08-14

---

## License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.  
See the [LICENSE](LICENSE) file or https://www.gnu.org/licenses/gpl-3.0.html for details.

---

**Thank you for using LCT!**  
If you encounter any issues or have suggestions, feel free to open an Issue or send an email.
