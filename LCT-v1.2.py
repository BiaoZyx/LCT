import argparse, os, shutil, sys
from colorama import init, Fore, Back, Style

# 初始化 colorama
init(autoreset=True)

"""颜色注释"""
# 输入：蓝色
# 输出提示：绿色
# 输出：白色
# 未知字符：黄色
# 菜单：紫色
# 标题：青色
# 错误：红色

# 定义线段密码字典
LC_CODE_DICT = {
    "A": "/\\-",
    "B": "|__'__",
    "C": "___",
    "D": "|__",
    "E": "|---",
    "F": "|--",
    "G": "___-",
    "H": "|-|",
    "I": "-|-",
    "J": "-|_",
    "K": "|/\\",
    "L": "|-",
    "M": "|\\/|",
    "N": "|\\|",
    "O": "____",
    "P": "|_",
    "Q": "____\\",
    "R": "|_\\",
    "S": "__",
    "T": "-|",
    "U": "|_|",
    "V": "\\/",
    "W": "\\/\\/",
    "X": "/\\",
    "Y": "\\/|",
    "Z": "-/-",
    "1": "|",
    "2": "_/-",
    "3": "___'___",
    "4": "/-|",
    "5": "-|'_",
    "6": "_'____",
    "7": "-/",
    "8": "____'____",
    "9": "____'_",
    "0": "_____|",
    ",": "/",
    ".": "'\\",
    "?": "_|'",
    "'": "'",
    "!": "|'",
    "/": "//",
    "(": "/_",
    ")": "\\_/",
    "&": "\\___/___",
    ":": "\\''",
    ";": "'/",
    "=": "--",
    "+": "\\-|",
    "-": "-",
    "_": "\\_",
    '"': "''",
    "$": "__|__",
    "@": "___'____\\",
    " ": "=",
    "\\": "\\\\",
    "~": "__'__",
    "#": "//--",
    "%": "____/____",
    "^": "'/'\\",
    "*": "'''''",
    "[": "'|'",
    "]": "\\'|'",
    "{": "_|_|_",
    "}": "\\_|_|_",
    "<": "\\/\\",
    ">": "\\\\/",
    "`": "\\'",
    "|": "\\|",
}

# 反转字典（放在全局，只构建一次）
LC_CODE_REVERSE_DICT = {value: key for key, value in LC_CODE_DICT.items()}

# 定义语言字典
LANGUAGES = {
    "en": {
        "enter_choice": "command > ",
        "enter_text": "text    > ",
        "enter_LC": "LC_code > ",
        "translated_LC": "The translated LC code is: ",
        "translated_text": "The translated text is: ",
        "exit_message": "Exiting the program...",
        "empty_input": "You have not entered anything, please re-enter! ",
        "space_input": "You have entered a space, please re-enter!",
        "invalid_choice": 'Invalid selection, please re-enter! Use "/menu" to show the menu! ',
    },
    "zh": {
        "enter_choice": "命令    > ",
        "enter_text": "文本    > ",
        "enter_LC": "线段密码> ",
        "translated_LC": "翻译后的线段密码是：",
        "translated_text": "翻译后的文本是：",
        "exit_message": "正在退出程序……",
        "empty_input": "您没有输入任何内容，请重新输入！",
        "space_input": "您输入了一个空格，请重新输入！",
        "invalid_choice": "无效的选择，请重新输入！用“/menu”查看菜单！ ",
    },
}

# 全局语言标识（由 main 设置）
CURRENT_LANG = "en"

# ---------- 辅助函数 ----------
def clear_screen():
    """清屏（兼容 Windows 和 Linux/Mac）"""
    os.system('cls' if os.name == 'nt' else 'clear')

# 获取终端高度（行数），用于定位底栏
def get_terminal_height():
    return shutil.get_terminal_size().lines

def print_bottom_bar(text):
    sys.stdout.write("\033[s")
    h = get_terminal_height()
    sys.stdout.write(f"\033[{h};0H")
    sys.stdout.write("\033[K" + Back.CYAN + Fore.BLACK + text + Style.RESET_ALL)
    sys.stdout.write("\033[u")
    sys.stdout.flush()

def print_title():
    """打印程序标题"""
    if CURRENT_LANG == "en":
        print(Back.CYAN + Style.NORMAL + "  -------------------------------  ")
        print(Back.CYAN + Style.NORMAL + "    ---<     LCT v1.2     >---     ")
        print(Back.CYAN + Style.NORMAL + "    Author  : BiaoZyx              ")
        print(Back.CYAN + Style.NORMAL + "    Email   : BiaoZyx@outlook.com  ")
        print(Back.CYAN + Style.NORMAL + "    Version : 1.2                  ")
        print(Back.CYAN + Style.NORMAL + "    Date    : 2026-5-1             ")
        print(Back.CYAN + Style.NORMAL + "  -------------------------------  ")
    else:
        print(Back.CYAN + Style.NORMAL + "  -------------------------------  ")
        print(Back.CYAN + Style.NORMAL + "    ---<     LCT v1.2     >---     ")
        print(Back.CYAN + Style.NORMAL + "    作者 : 飙志                    ")
        print(Back.CYAN + Style.NORMAL + "    邮箱 : BiaoZyx@outlook.com     ")
        print(Back.CYAN + Style.NORMAL + "    版本 : 1.2                     ")
        print(Back.CYAN + Style.NORMAL + "    日期 : 2026-5-1                ")
        print(Back.CYAN + Style.NORMAL + "  -------------------------------  ")

def show_menu():
    """显示菜单"""
    if CURRENT_LANG == "en":
        print(Fore.MAGENTA + """
  ●  1            : text to LC code
  ●  2            : LC code to text
  ●  3            : LC code dictionary
  ●  /menu        : show this menu
  ●  /version     : show version info
  ●  /help        : show help info
  ●  /clear       : clear the screen
  ●  /exit        : exit the program
  ●  /egg <color> : Easter egg
""")
    else:
        print(Fore.MAGENTA + """
  ●  1           ：文本转线段密码
  ●  2           ：线段密码转文本
  ●  3           ：线段密码字典
  ●  /menu       ：显示此菜单
  ●  /version    ：显示版本信息
  ●  /help       ：帮助
  ●  /clear      ：清屏
  ●  /exit       ：退出程序
  ●  /egg <颜色> ：彩蛋
""")

def show_version():
    """显示版本信息"""
    if CURRENT_LANG == "en":
        print(Fore.GREEN + """
 _     ____ _____          _   ____
| |   / ___|_   _|  __   _/ | |___ \\
| |  | |     | |____\\ \\ / / |   __) |
| |__| |___  | |_____\\ \\V /| |_ / __/
|_____\\____| |_|      \\_/ |_(_)_____|
Version : 1.2
Date    : 2026-5-1
This program is a simple LC code translator.
It can convert text to LC code and vice versa.
It also provides a LC code dictionary for reference.
I (Author) created this code on 2025-8-14. lol.
Thank you for using this program!
If you have any questions or suggestions,
please feel free to contact me at BiaoZyx@outlook.com.
""")
    else:
        print(Fore.GREEN + """
 _     ____ _____          _   ____
| |   / ___|_   _|  __   _/ | |___ \\
| |  | |     | |____\\ \\ / / |   __) |
| |__| |___  | |_____\\ \\V /| |_ / __/
|_____\\____| |_|      \\_/ |_(_)_____|
版本：1.2
日期：2026-5-1
本程序是一个简单的线段密码翻译器。
它可以将文本转换为线段密码，反之亦然。
同时提供线段密码字典供参考。
我（作者）在2025-8-14想出了这个密码。
感谢您使用本程序！
如果您有任何问题或建议，
请随时通过 BiaoZyx@outlook.com 联系我。
""")

def show_help():
    """显示帮助信息"""
    if CURRENT_LANG == "en":
        print(Fore.GREEN + """
This program is a simple LC code translator.
It can convert text to LC code and vice versa.
It also provides a LC code dictionary for reference.
This tool is capable of translating English letters, 
Arabic numerals, and some English punctuation marks.

Usage:
1. Enter the command to select the operation;
2. Enter the text or LC code to be converted,
   if you enter LC code, please use a space to separate
   each LC code;
3. If you are not sure about the command,
   you can enter "/menu" to view the menu;
4. You can exit by pressing <Ctrl + C> or entering "/exit".
""")
    else:
        print(Fore.GREEN + """
本程序是一个简单的线段密码翻译器。
它可以将文本转换为线段密码，反之亦然。
同时它提供线段密码字典供参考。
本工具能够翻译英文、阿拉伯数字和一些英文标点。

使用方法：
1. 输入命令选择操作；
2. 输入文本或线段密码进行转换，
   如果你输入了线段密码，请用空格分隔每个线段密码；
3. 如果不清楚命令，可以输入“/menu”查看菜单；
4. 退出可以按 <Ctrl + C> 或输入“/exit”。
""")

def show_LC_dict():
    """根据 LC_CODE_DICT 动态生成格式化的字典显示"""
    # 定义显示顺序：字母 -> 数字 -> 符号
    letters = [chr(i) for i in range(65, 91)]          # A-Z
    digits = [str(i) for i in range(10)]               # 0-9
    symbols = [
        ',', '.', '?', "'", '!', '/', '(', ')', '&', ':', ';',
        '=', '+', '-', '_', '"', '$', '@', ' ', '\\', '~', '#',
        '%', '^', '*', '[', ']', '{', '}', '<', '>', '`', '|'
    ]

    category_names = {
        'en': ("Letters", "Digits", "Symbols"),
        'zh': ("字母", "数字", "符号")
    }
    title_en = "LC Code Dictionary:"
    title_zh = "线段密码字典："

    def format_category(items, cat_name):
        lines = []
        lines.append(Fore.CYAN + f"  [{cat_name}]" + Style.RESET_ALL)
        existing = [(ch, LC_CODE_DICT[ch]) for ch in items if ch in LC_CODE_DICT]
        if not existing:
            lines.append("  (none)")
            return "\n".join(lines)

        max_ch = max(len(ch) for ch, _ in existing)
        max_code = max(len(code) for _, code in existing)

        row = []
        for i, (ch, code) in enumerate(existing):
            entry = f"{ch.ljust(max_ch)} {Fore.YELLOW}{code.ljust(max_code)}{Style.RESET_ALL}"
            row.append(entry)
            if len(row) == 3 or i == len(existing) - 1:
                lines.append("   ".join(row))
                row = []
        return "\n".join(lines)

    if CURRENT_LANG == "en":
        title = title_en
        names = category_names['en']
    else:
        title = title_zh
        names = category_names['zh']

    print(Fore.GREEN + Style.BRIGHT + title + Style.RESET_ALL)
    print(format_category(letters, names[0]))
    print("-" * 65)
    print(format_category(digits, names[1]))
    print("-" * 65)
    print(format_category(symbols, names[2]))

# ---------- 文本转换 ----------
def text_to_LC(text):
    """将文本转换为线段密码"""
    LC_code = []
    for char in text.upper():
        if char in LC_CODE_DICT:
            LC_code.append(LC_CODE_DICT[char])
        else:
            LC_code.append(Fore.YELLOW + "?" + Style.RESET_ALL)
    return " ".join(LC_code)

def LC_to_text(LC):
    """将线段密码转换为文本"""
    text = []
    for code in LC.strip().split(" "):
        if code == "":
            continue
        if code in LC_CODE_REVERSE_DICT:
            text.append(LC_CODE_REVERSE_DICT[code])
        else:
            text.append(Fore.YELLOW + "?" + Style.RESET_ALL)
    return "".join(text)

# ---------- 彩蛋 ----------
EGG_COLORS = {
    'red': Fore.RED,
    'green': Fore.GREEN,
    'blue': Fore.BLUE,
    'yellow': Fore.YELLOW,
    'purple': Fore.MAGENTA,
    'cyan': Fore.CYAN
}

def show_egg_list():
    if CURRENT_LANG == "en":
        print(Fore.GREEN + "Available egg colors: " + ", ".join(EGG_COLORS.keys()))
    else:
        print(Fore.GREEN + "可用彩蛋颜色：" + ", ".join(EGG_COLORS.keys()))

def show_egg(color_name):
    color = EGG_COLORS.get(color_name, Fore.WHITE)
    if CURRENT_LANG == "en":
        msg = f"{color}0{Style.RESET_ALL} <= This is a {color_name} Easter egg! :)"
    else:
        msg = f"{color}0{Style.RESET_ALL} <= 这是一个{color_name}的彩蛋！ :)"
    print(msg)

# ---------- 选择语言 ----------
def select_language():
    """让用户交互选择语言，返回 'en' 或 'zh'"""
    try:
        print(Fore.GREEN + "Select language / 选择语言:")
        print(Fore.MAGENTA + """
    1. English
    2. 中文
""")
        choice = input(Fore.BLUE + "set_lang > " + Style.RESET_ALL)
        if choice == "1":
            return "en"
        elif choice == "2":
            return "zh"
        else:
            print(Fore.RED + "Invalid choice, please re-enter! / 无效的选择，请重新输入！\n")
            return select_language()
    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting the program... / 正在退出程序...")
        exit()

# ---------- 命令行一次性执行 ----------
def run_once(args):
    TEXT = LANGUAGES[CURRENT_LANG]
    if args.text:
        print(Fore.GREEN + TEXT["translated_LC"], text_to_LC(args.text))
    if args.lc:
        print(Fore.GREEN + TEXT["translated_text"], LC_to_text(args.lc))
    if args.dict:
        show_LC_dict()
    if args.version:
        show_version()
    if args.help_info:
        show_help()
    if args.egg:
        if args.egg == 'list':
            show_egg_list()
        else:
            egg_color = args.egg.lower()
            if egg_color in EGG_COLORS:
                show_egg(egg_color)
            else:
                print(Fore.RED + "Unknown egg color. Use --egg to see available colors.")

# ---------- Nano 风格交互循环 ----------
def interactive_loop():
    TEXT = LANGUAGES[CURRENT_LANG]
    last_output = ""

    # 各种提示语
    prompt_choice = f"{Fore.BLUE}▶ {Style.BRIGHT}{TEXT['enter_choice']}{Style.RESET_ALL}"
    prompt_text   = f"{Fore.BLUE}▶ {Style.BRIGHT}{TEXT['enter_text']}{Style.RESET_ALL}"
    prompt_lc     = f"{Fore.BLUE}▶ {Style.BRIGHT}{TEXT['enter_LC']}{Style.RESET_ALL}"

    def get_input_at_bottom(prompt):
        """在屏幕倒数第二行（底栏上方）获取输入，保持底栏不动"""
        h = get_terminal_height()
        input_line = h - 1
        sys.stdout.write(f"\033[{input_line};0H")   # 移动光标
        sys.stdout.write("\033[K")                  # 清除该行
        return input(prompt).strip()

    while True:
        # 1. 重绘整个界面
        clear_screen()
        print_title()
        show_menu()

        if last_output:
            print(Fore.GREEN + last_output)
            print()

        # 2. 固定底栏
        bar = (" [1]Text→LC [2]LC→Text [3]Dict [/menu]Menu [/help]Help [/exit]Exit "
               if CURRENT_LANG == "en" else
               " [1]文本→LC [2]LC→文本 [3]字典 [/menu]菜单 [/help]帮助 [/exit]退出 ")
        print_bottom_bar(bar)

        # 3. 在底栏上方获取命令
        choice = get_input_at_bottom(prompt_choice)

        # 4. 处理命令
        if choice == "1":
            user_input = get_input_at_bottom(prompt_text)
            last_output = TEXT["translated_LC"] + text_to_LC(user_input)

        elif choice == "2":
            user_input = get_input_at_bottom(prompt_lc)
            last_output = TEXT["translated_text"] + LC_to_text(user_input)

        elif choice == "3":
            # 字典内容较长，单独清屏显示，避免布局错乱
            clear_screen()
            print_title()
            show_LC_dict()
            input("\n" + ("Press Enter to continue..." if CURRENT_LANG=="en" else "按回车键继续..."))
            last_output = ""

        elif choice == "/menu":
            last_output = ""          # 菜单一直显示，无需额外动作

        elif choice == "/help":
            clear_screen()
            print_title()
            show_help()
            input("\n" + ("Press Enter to continue..." if CURRENT_LANG=="en" else "按回车键继续..."))
            last_output = ""

        elif choice == "/version":
            clear_screen()
            print_title()
            show_version()
            input("\n" + ("Press Enter to continue..." if CURRENT_LANG=="en" else "按回车键继续..."))
            last_output = ""

        elif choice == "/egg":
            clear_screen()
            print_title()
            show_egg_list()
            input("\n" + ("Press Enter to continue..." if CURRENT_LANG=="en" else "按回车键继续..."))
            last_output = ""

        elif choice.startswith("/egg "):
            parts = choice.split()
            if len(parts) == 2 and parts[1].lower() in EGG_COLORS:
                clear_screen()
                print_title()
                show_egg(parts[1].lower())
                input("\n" + ("Press Enter to continue..." if CURRENT_LANG=="en" else "按回车键继续..."))
                last_output = ""
            else:
                last_output = Fore.RED + ("Invalid egg color." if CURRENT_LANG=="en" else "无效的颜色。")

        elif choice == "/clear":
            last_output = ""          # 重新绘制时自然就是清屏

        elif choice == "/exit" or choice == "/quit":
            print(Fore.RED + TEXT["exit_message"])
            break

        elif not choice or choice.isspace():
            last_output = Fore.RED + TEXT["empty_input"]

        else:
            last_output = Fore.RED + TEXT["invalid_choice"]
            
# ---------- 主入口 ----------
def main():
    global CURRENT_LANG
    parser = argparse.ArgumentParser(description="LC Code Translator")
    parser.add_argument('-t', '--text', help='Text to translate to LC code')
    parser.add_argument('-l', '--lc', help='LC code to translate to text (separate codes by space)')
    parser.add_argument('--dict', action='store_true', help='Show LC code dictionary')
    parser.add_argument('--version', action='store_true', help='Show version info')
    parser.add_argument('--help-info', action='store_true', help='Show help info')
    parser.add_argument('--egg', nargs='?', const='list', help='Easter egg, optionally give a color name')
    parser.add_argument('--lang', choices=['en', 'zh'], default=None, help='Language (en/zh)')
    args = parser.parse_args()

    # 设置语言
    if args.lang:
        CURRENT_LANG = args.lang
    else:
        CURRENT_LANG = select_language()

    # 判断模式：如果提供了除 --lang 外的任何任务参数，则一次性执行
    if any([args.text, args.lc, args.dict, args.version, args.help_info, args.egg]):
        run_once(args)
    else:
        interactive_loop()

if __name__ == "__main__":
    main()