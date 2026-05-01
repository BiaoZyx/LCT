import argparse
import os
import locale
import sys
import curses
import textwrap
from wcwidth import wcswidth
from colorama import init, Fore, Style

# ================== 全局定义 ==================
CURRENT_LANG = "en"

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
LC_CODE_REVERSE_DICT = {v: k for k, v in LC_CODE_DICT.items()}

LANGUAGES = {
    "en": {
        "enter_choice": "command > ",
        "enter_text": "text    > ",
        "enter_LC": "LC_code > ",
        "translated_LC": "Translated LC: ",
        "translated_text": "Translated text: ",
        "exit_message": "Exiting...",
        "empty_input": "Empty input!",
        "invalid_choice": "Invalid choice!",
    },
    "zh": {
        "enter_choice": "命令    > ",
        "enter_text": "文本    > ",
        "enter_LC": "线段密码> ",
        "translated_LC": "线段密码：",
        "translated_text": "文本：",
        "exit_message": "正在退出...",
        "empty_input": "输入为空！",
        "invalid_choice": "无效命令！",
    },
}

EGG_COLORS = {"red": 1, "green": 2, "blue": 6, "yellow": 4, "purple": 5, "cyan": 7}


def text_to_LC(text):
    return " ".join(LC_CODE_DICT.get(c.upper(), "?") for c in text)


def LC_to_text(lc):
    return "".join(LC_CODE_REVERSE_DICT.get(code, "?") for code in lc.split())


def select_language():
    print("Select language / 选择语言:")
    print("1. English\n2. 中文")
    try:
        c = input("set_lang > ").strip()
        if c == "2":
            return "zh"
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)  # ← 这里改用 sys.exit
    return "en"


def run_once(args):
    # 启用彩色输出（一次性模式专用）
    init(autoreset=True)
    TEXT = LANGUAGES[CURRENT_LANG]

    # 文本转LC
    if args.text:
        print(Fore.GREEN + TEXT["translated_LC"] + Style.BRIGHT + text_to_LC(args.text))

    # LC转文本
    if args.lc:
        print(Fore.GREEN + TEXT["translated_text"] + Style.BRIGHT + LC_to_text(args.lc))

    # 字典
    if args.dict:
        lines = get_lc_dict_lines(CURRENT_LANG)
        for i, line in enumerate(lines):
            if i == 0:  # 标题
                print(Fore.GREEN + Style.BRIGHT + line)
            elif line.startswith("  [") and line.endswith("]"):  # 分类名
                print(Fore.CYAN + line)
            elif line.startswith("-"):  # 分隔线
                print(Fore.CYAN + line)
            elif line == "":  # 空行
                print()
            else:  # 数据
                print(Fore.YELLOW + line)

    # 版本信息
    if args.version:
        print(Fore.GREEN + Style.BRIGHT + "LCT v1.3")

    # 彩蛋
    if args.egg:
        color_map = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "blue": Fore.BLUE,
            "yellow": Fore.YELLOW,
            "purple": Fore.MAGENTA,
            "cyan": Fore.CYAN,
        }
        egg_color = args.egg.lower() if args.egg != "list" else None
        if egg_color and egg_color in color_map:
            print(
                color_map[egg_color] + f"0 <= This is a {egg_color} Easter egg! :)"
                if CURRENT_LANG == "en"
                else f"0 <= 这是一个{egg_color}的彩蛋！ :)"
            )
        else:
            print(
                Fore.GREEN
                + "Available egg colors: red, green, blue, yellow, purple, cyan"
            )


def get_system_lang():
    """
    跨平台自动检测系统语言，优先返回 'zh' 或 'en'。
    使用当前推荐的 locale API，避免弃用警告。
    """
    # 方法1：使用 locale.getlocale() （当前推荐）
    try:
        lang, _ = locale.getlocale(category=locale.LC_CTYPE)
        if lang and lang.startswith("zh"):
            return "zh"
    except:
        pass

    # 方法2：环境变量（Linux/macOS 常用）
    try:
        env_lang = os.environ.get("LANG", "")
        if env_lang.startswith("zh"):
            return "zh"
    except:
        pass

    # 方法3：Windows API（仅在 Windows 上有效）
    try:
        import ctypes

        windll = ctypes.windll.kernel32
        lang_id = windll.GetUserDefaultUILanguage()
        if lang_id in (0x0804, 0x0404, 0x0C04, 0x1004, 0x1404):
            return "zh"
    except:
        pass

    # 默认回退英文
    return "en"


def get_lc_dict_lines(lang):
    """
    返回一个列表，每个元素是一行格式化好的字符串。
    lang: 'en' 或 'zh'
    """
    letters = [chr(i) for i in range(65, 91)]
    digits = [str(i) for i in range(10)]
    symbols = [c for c in ',.?!/()&:;=+-_"$@ \\~#%^*[]{}<>`|']

    category_names = {
        "en": ("Letters", "Digits", "Symbols"),
        "zh": ("字母", "数字", "符号"),
    }
    title = "LC Code Dictionary:" if lang == "en" else "线段密码字典："
    names = category_names[lang]

    def block(items, cat_name):
        lines = []
        existing = [(ch, LC_CODE_DICT[ch]) for ch in items if ch in LC_CODE_DICT]
        if not existing:
            return lines
        max_ch = max((len(c) for c, _ in existing), default=0)
        max_cd = max((len(d) for _, d in existing), default=0)
        row = []
        for i, (c, d) in enumerate(existing):
            entry = f"{c.ljust(max_ch)} {d.ljust(max_cd)}"
            row.append(entry)
            if len(row) == 3 or i == len(existing) - 1:
                lines.append("   ".join(row))
                row = []
        return lines

    result = [title, ""]
    for name, group in zip(names, [letters, digits, symbols]):
        result.append(f"  [{name}]")
        result.extend(block(group, name))
        result.append("-" * 65)
    return result


# ================== CURSES 类 ==================
class LctCursesApp:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.lang = CURRENT_LANG
        self.text = LANGUAGES[self.lang]
        self.running = True
        self.cmd_history = []
        self.has_output = False
        self.last_h = self.last_w = 0  # 记录上次终端尺寸

        self.setup_colors()
        self.create_windows()  # 初始创建
        self.mid_win.scrollok(True)
        self.add_message("Welcome to LCT v1.3\nType /help for help.\n")
        self.draw_top_bar()
        self.draw_bottom_bar()

    def setup_colors(self):
        curses.start_color()
        try:
            curses.use_default_colors()
        except:
            pass
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)
        curses.init_pair(4, curses.COLOR_YELLOW, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)
        curses.init_pair(6, curses.COLOR_BLUE, -1)
        curses.init_pair(7, curses.COLOR_CYAN, -1)
        self.COLOR_TOP = curses.color_pair(1)
        self.COLOR_GREEN = curses.color_pair(2)
        self.COLOR_RED = curses.color_pair(3)
        self.COLOR_YELLOW = curses.color_pair(4)
        self.COLOR_MAGENTA = curses.color_pair(5)
        self.COLOR_BLUE = curses.color_pair(6)
        self.COLOR_CYAN = curses.color_pair(7)

    def create_windows(self):
        """根据当前终端尺寸创建窗口，并记录尺寸"""
        h, w = self.stdscr.getmaxyx()
        if h < 10 or w < 60:
            raise RuntimeError("终端窗口太小，请至少调整到 60x10")
        self.top_win = curses.newwin(1, w, 0, 0)
        self.bot_win = curses.newwin(1, w, h - 2, 0)
        self.input_win = curses.newwin(1, w, h - 1, 0)
        self.mid_win = curses.newwin(h - 3, w, 1, 0)
        self.last_h, self.last_w = h, w

    def adjust_windows_if_resized(self):
        """如果终端尺寸变化，移动并调整现有窗口大小（保留内容）"""
        h, w = self.stdscr.getmaxyx()
        if h == self.last_h and w == self.last_w:
            return False  # 尺寸未变

        # 调整各窗口位置和尺寸
        try:
            self.top_win.mvwin(0, 0)
            self.top_win.resize(1, w)
            self.bot_win.mvwin(h - 2, 0)
            self.bot_win.resize(1, w)
            self.input_win.mvwin(h - 1, 0)
            self.input_win.resize(1, w)
            self.mid_win.mvwin(1, 0)
            self.mid_win.resize(h - 3, w)
            self.mid_win.scrollok(True)
        except curses.error:
            raise RuntimeError("终端窗口太小，请至少调整到 60x10")

        self.last_h, self.last_w = h, w
        # 重绘顶栏和底栏以适应新宽度
        self.draw_top_bar()
        self.draw_bottom_bar()
        return True

    def draw_top_bar(self):
        w = self.top_win.getmaxyx()[1]
        title = (
            " LCT v1.3   |   飙志   |   /help "
            if self.lang == "zh"
            else " LCT v1.3   |   BiaoZyx   |   /help "
        )
        disp = title.center(w)[:w]
        self.top_win.bkgd(" ", self.COLOR_TOP)
        try:
            self.top_win.addstr(0, 0, disp)
        except curses.error:
            pass
        self.top_win.refresh()

    def draw_bottom_bar(self):
        """绘制底部快捷键栏，强制固定在倒数第二行"""
        h, w = self.stdscr.getmaxyx()
        self.bot_win.mvwin(h - 2, 0)  # 重新定位到正确位置
        self.bot_win.resize(1, w)  # 确保尺寸正确
        bar = (
            " [1]文本→LC [2]LC→文本 [3]字典 [/menu] [/help] [/exit] [/history] "
            if self.lang == "zh"
            else " [1]Text→LC [2]LC→Text [3]Dict [/menu] [/help] [/exit] [/history] "
        )
        disp = bar.center(w)[:w]
        self.bot_win.bkgd(" ", self.COLOR_TOP)
        try:
            self.bot_win.addstr(0, 0, disp)
        except curses.error:
            pass
        self.bot_win.refresh()

    def add_message(self, text, color=None):
        if color is None:
            color = 0
        h, w = self.mid_win.getmaxyx()
        for line in text.splitlines():
            if line == "":
                try:
                    self.mid_win.addstr("\n")
                except curses.error:
                    pass
                continue
            for sub in textwrap.wrap(line, width=w) or [""]:
                y, _ = self.mid_win.getyx()
                if y >= h - 1:
                    self.mid_win.scroll(1)
                    self.mid_win.move(h - 1, 0)
                try:
                    self.mid_win.addstr(sub + "\n", color)
                except curses.error:
                    pass
        self.has_output = True
        self.mid_win.refresh()

    def separator_if_needed(self):
        if self.has_output:
            w = self.mid_win.getmaxyx()[1]
            try:
                # self.mid_win.addstr("\n")
                self.mid_win.addstr("\n" + "─" * w + "\n", self.COLOR_CYAN)
            except curses.error:
                pass
            self.mid_win.refresh()

    def get_input(self, prompt=""):
        curses.flushinp()
        h, w = self.stdscr.getmaxyx()
        self.input_win.mvwin(h - 1, 0)
        self.input_win.resize(1, w)
        self.input_win.erase()
        self.input_win.bkgd(" ", 0)

        # 计算提示符在终端中的实际列宽，并截断到安全长度
        prompt_disp_width = wcswidth(prompt)
        while prompt_disp_width >= w:
            prompt = prompt[:-1]
            prompt_disp_width = wcswidth(prompt)
        prompt_safe = prompt

        try:
            self.input_win.addstr(0, 0, prompt_safe, self.COLOR_BLUE)
        except curses.error:
            pass
        self.input_win.refresh()

        # 光标位置使用显示宽度
        cursor_pos = min(prompt_disp_width, w - 1)
        self.input_win.move(0, cursor_pos)

        curses.echo()
        curses.curs_set(1)
        try:
            s = self.input_win.getstr(0, cursor_pos, w - cursor_pos - 1)
        except:
            s = b""
        curses.noecho()
        curses.curs_set(0)

        out = s.decode("utf-8", errors="ignore").strip()

        self.input_win.erase()
        self.input_win.bkgd(" ", 0)
        try:
            self.input_win.addstr(0, 0, prompt_safe, self.COLOR_BLUE)
        except:
            pass
        self.input_win.refresh()

        if not out or out[0] == "\x1b" or all(ord(c) < 32 for c in out):
            out = ""
        return out

    # ---------- 信息展示（菜单、版本、帮助、字典） ----------
    def show_menu(self):
        # 原有代码不变
        items = (
            [
                "1            : text to LC code",
                "2            : LC code to text",
                "3            : LC code dictionary",
                "/menu        : show this menu",
                "/version     : version info",
                "/help        : detailed help",
                "/clear       : clear screen",
                "/history     : command history",
                "/exit        : exit",
                "/egg <color> : Easter egg",
            ]
            if self.lang == "en"
            else [
                "1           ：文本转线段密码",
                "2           ：线段密码转文本",
                "3           ：线段密码字典",
                "/menu       ：显示菜单",
                "/version    ：版本信息",
                "/help       ：帮助",
                "/clear      ：清屏",
                "/history    ：命令历史",
                "/exit       ：退出",
                "/egg <颜色> ：彩蛋",
            ]
        )
        self.add_message("", self.COLOR_MAGENTA)
        for line in items:
            self.add_message("  ●  " + line, self.COLOR_MAGENTA)
        self.add_message("", self.COLOR_MAGENTA)

    def show_version(self):
        ver = (
            (
                " _     ____ _____          _   _____\n"
                "| |   / ___|_   _|  __   _/ | |___ /\n"
                "| |  | |     | |____\\ \\ / / |   |_ \\\n"
                "| |__| |___  | |_____\\ V /| |_ ___) |\n"
                "|_____\\____| |_|      \\_/ |_(_)____/\n"
                "Version : 1.3  Date : 2026-5-1\n"
                "Author : BiaoZyx"
            )
            if self.lang == "en"
            else (
                " _     ____ _____          _   _____\n"
                "| |   / ___|_   _|  __   _/ | |___ /\n"
                "| |  | |     | |____\\ \\ / / |   |_ \\\n"
                "| |__| |___  | |_____\\ V /| |_ ___) |\n"
                "|_____\\____| |_|      \\_/ |_(_)____/\n"
                "版本：1.3  日期：2026-5-1\n"
                "作者：飙志"
            )
        )
        self.add_message(ver, self.COLOR_GREEN)

    def show_help(self):
        if self.lang == "en":
            help_text = (
                "This program translates between text and Line Cipher (LC) code.\n"
                "It supports uppercase letters, digits, and common punctuation.\n\n"
                "Commands:\n"
                "  1            - text → LC\n"
                "  2            - LC → text\n"
                "  3            - full LC dictionary\n"
                "  /menu        - show command menu\n"
                "  /version     - version info\n"
                "  /help        - this help\n"
                "  /clear       - clear output area\n"
                "  /history     - last 20 commands\n"
                "  /exit /quit  - exit\n"
                "  /egg <color> - Easter egg\n\n"
                "Enter LC codes separated by spaces.\n"
                "Example:  text > HELLO  →  |-| ___ |- |- ---\n"
                "         LC_code > |-| ___ |- |- ---  →  HELLO\n"
            )
        else:
            help_text = (
                "本程序用于文本与线段密码（LC）的互转。\n"
                "支持大写字母、数字及常用英文标点。\n\n"
                "命令列表：\n"
                "  1            - 文本 → LC\n"
                "  2            - LC → 文本\n"
                "  3            - 完整密码字典\n"
                "  /menu        - 显示菜单\n"
                "  /version     - 版本信息\n"
                "  /help        - 本帮助\n"
                "  /clear       - 清空输出区\n"
                "  /history     - 最近20条命令\n"
                "  /exit /quit  - 退出\n"
                "  /egg <颜色>  - 彩蛋\n\n"
                "输入线段密码时用空格分隔每个字符的密码。\n"
                "例：文本 > HELLO  →  |-| ___ |- |- ---\n"
                "    线段密码> |-| ___ |- |- ---  →  HELLO\n"
            )
        self.add_message(help_text, self.COLOR_GREEN)

    def show_lc_dict(self):
        lines = get_lc_dict_lines(self.lang)
        # 第一行标题用粗体绿色，其他行根据类型着色
        for i, line in enumerate(lines):
            if i == 0:  # 标题
                self.add_message(line, self.COLOR_GREEN | curses.A_BOLD)
            elif line.startswith("  [") and line.endswith("]"):
                self.add_message(line, self.COLOR_CYAN)
            elif line.startswith("-"):
                self.add_message(line, self.COLOR_CYAN)
            elif line == "":
                self.add_message(line)
            else:
                self.add_message(line, self.COLOR_YELLOW)

    # ---------- 主循环 ----------
    def run(self):
        while self.running:
            # 只在尺寸变化时调整窗口，不重建
            self.adjust_windows_if_resized()
            self.draw_top_bar()
            self.draw_bottom_bar()

            cmd = self.get_input(self.text["enter_choice"])
            if not cmd:
                continue
            self.cmd_history.append(cmd)

            self.separator_if_needed()
            self.add_message(f">>> {self.text['enter_choice']}{cmd}", self.COLOR_CYAN)

            # 命令处理（与之前完全相同）
            if cmd == "1":
                txt = self.get_input(self.text["enter_text"])
                if txt:
                    self.add_message(
                        f">>> {self.text['enter_text']}{txt}", self.COLOR_CYAN
                    )
                    self.add_message(
                        self.text["translated_LC"] + text_to_LC(txt), self.COLOR_GREEN
                    )
                else:
                    self.add_message(self.text["empty_input"], self.COLOR_RED)
            elif cmd == "2":
                lc = self.get_input(self.text["enter_LC"])
                if lc:
                    self.add_message(
                        f">>> {self.text['enter_LC']}{lc}", self.COLOR_CYAN
                    )
                    self.add_message(
                        self.text["translated_text"] + LC_to_text(lc), self.COLOR_GREEN
                    )
                else:
                    self.add_message(self.text["empty_input"], self.COLOR_RED)
            elif cmd == "3":
                self.show_lc_dict()
            elif cmd == "/menu":
                self.show_menu()
            elif cmd == "/help":
                self.show_help()
            elif cmd == "/version":
                self.show_version()
            elif cmd == "/clear":
                self.mid_win.clear()
                self.mid_win.refresh()
                self.has_output = False
            elif cmd in ("/history", "/hist"):
                start = max(0, len(self.cmd_history) - 20)
                for i in range(start, len(self.cmd_history)):
                    self.add_message(
                        f"{i - start + 1:3d}: {self.cmd_history[i]}", self.COLOR_MAGENTA
                    )
            elif cmd.startswith("/egg"):
                parts = cmd.split()
                if len(parts) == 1:
                    self.add_message(
                        "Available: red,green,blue,yellow,purple,cyan", self.COLOR_GREEN
                    )
                elif parts[1] in EGG_COLORS:
                    self.add_message(f"0 <= {parts[1]} egg! :)", self.COLOR_GREEN)
                else:
                    self.add_message(self.text["invalid_choice"], self.COLOR_RED)
            elif cmd in ("/exit", "/quit"):
                self.add_message(self.text["exit_message"], self.COLOR_RED)
                self.running = False
            elif not cmd or cmd.isspace():
                self.add_message(self.text["empty_input"], self.COLOR_RED)
            else:
                self.add_message(self.text["invalid_choice"], self.COLOR_RED)


# ================== 主入口 ==================
def main():
    global CURRENT_LANG

    parser = argparse.ArgumentParser(description="LC Code Translator")
    parser.add_argument("-t", "--text", help="Text to translate to LC code")
    parser.add_argument(
        "-l", "--lc", help="LC code to translate to text (separate codes by space)"
    )
    parser.add_argument("--dict", action="store_true", help="Show LC code dictionary")
    parser.add_argument("--version", action="store_true", help="Show version info")
    parser.add_argument(
        "--egg",
        nargs="?",
        const="list",
        help="Easter egg, optionally give a color name",
    )
    parser.add_argument(
        "--lang", choices=["en", "zh"], default=None, help="Force language (en/zh)"
    )
    args = parser.parse_args()

    # ---------- 语言设置 ----------
    if args.lang:
        CURRENT_LANG = args.lang
    else:
        # 一次性模式则自动检测系统语言，否则交互选择
        if any([args.text, args.lc, args.dict, args.version, args.egg]):
            CURRENT_LANG = get_system_lang()
        else:
            CURRENT_LANG = select_language()

    # ---------- 执行 ----------
    if any([args.text, args.lc, args.dict, args.version, args.egg]):
        run_once(args)
    else:
        try:
            curses.wrapper(lambda stdscr: LctCursesApp(stdscr).run())
        except RuntimeError as e:
            print(e)
            sys.exit(1)
        except Exception as e:
            print(f"启动失败: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
