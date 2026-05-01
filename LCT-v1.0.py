from colorama import *  # 颜色

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
    "3": "__'__",
    "4": "/-|",
    "5": "-|'_",
    "6": "_'____",
    "7": "-/",
    "8": "____'____",
    "9": "____'_",
    "0": "_____|",
    ",": "/",
    ".": "'",
    "?": "_|'",
    "'": "\\'",
    "!": "|'",
    "/": "//",
    "(": "/_",
    ")": "\\_",
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
}

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


# 定义函数：选择语言
def select_language():
    global lang_choice  # 声明 lang_choice 为全局变量
    try:
        print(Fore.GREEN + "Select language / 选择语言:")
        print(
            Fore.MAGENTA
            + """
    1. English
    2. 中文
    """
        )
        lang_choice = input(Fore.BLUE + "set_lang > " + Style.RESET_ALL)
        if lang_choice == "1":
            return "en"

        elif lang_choice == "2":
            return "zh"

        else:
            print(
                Fore.RED
                + "Invalid choice, please re-enter! / 无效的选择，请重新输入！ \n "
            )
            return select_language()  # 递归调用，直到用户输入有效的选择
    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting the program... / 正在退出程序...")
        exit()


# 加载语言
current_language = select_language()
TEXT = LANGUAGES[current_language]


# 定义函数：打印标题
def print_title():
    if lang_choice == "1":
        print(Back.CYAN + Style.NORMAL + "  -------------------------------  ")
        print(Back.CYAN + Style.NORMAL + "    ---<     LCT v1.0     >---     ")
        print(Back.CYAN + Style.NORMAL + "    Author  : BiaoZyx              ")
        print(Back.CYAN + Style.NORMAL + "    Email   : BiaoZyx@outlook.com  ")
        print(Back.CYAN + Style.NORMAL + "    Version : 1.0                  ")
        print(Back.CYAN + Style.NORMAL + "    Date    : 2025-8-15            ")
        print(Back.CYAN + Style.NORMAL + "  -------------------------------  ")
    elif lang_choice == "2":
        print(Back.CYAN + Style.NORMAL + "  -------------------------------  ")
        print(Back.CYAN + Style.NORMAL + "    ---<     LCT v1.0     >---     ")
        print(Back.CYAN + Style.NORMAL + "    作者 : 飙志                    ")
        print(Back.CYAN + Style.NORMAL + "    邮箱 : BiaoZyx@outlook.com     ")
        print(Back.CYAN + Style.NORMAL + "    版本 : 1.0                     ")
        print(Back.CYAN + Style.NORMAL + "    日期 : 2025-8-15               ")
        print(Back.CYAN + Style.NORMAL + "  -------------------------------  ")


# 定义函数：文本转线段密码
def text_to_LC(text):
    """将文本转换为线段密码"""
    LC_code = []
    for char in text.upper():
        if char in LC_CODE_DICT:
            LC_code.append(LC_CODE_DICT[char])
        else:
            LC_code.append(Fore.YELLOW + "?" + Style.RESET_ALL)  # 未知字符用 '?' 表示
    return " ".join(LC_code)


# 定义函数：线段密码转文本
def LC_to_text(LC):
    """将线段密码转换为文本"""
    text = []
    for code in LC.strip().split(" "):
        if code == "":
            continue  # 跳过多余空格
        if code in LC_CODE_REVERSE_DICT:
            text.append(LC_CODE_REVERSE_DICT[code])
        else:
            text.append(Fore.YELLOW + "?" + Style.RESET_ALL)  # 未知线段密码用 '?' 表示
    return "".join(text)


# 定义函数：显示版本信息
def show_version():
    if lang_choice == "1":
        print(
            Fore.GREEN
            + """
 _     ____ _____          _   ___
| |   / ___|_   _|  __   _/ | / _ \\
| |  | |     | |____\\ \\ / / || | | |
| |__| |___  | |_____\\ V /| || |_| |
|_____\\____| |_|      \\_/ |_(_)___/
Version : 1.0
Date    : 2025-8-15
This program is a simple LC code translator. It can convert text to LC code and vice versa. It also provides a LC code dictionary for reference.
I(Author) made create this code on 8-14.lol.
Thank you for using this program!
If you have any questions or suggestions, please feel free to contact me at BiaoZyx@outlook.com.
        """
        )
    elif lang_choice == "2":
        print(
            Fore.GREEN
            + """
 _     ____ _____          _   ___
| |   / ___|_   _|  __   _/ | / _ \\
| |  | |     | |____\\ \\ / / || | | |
| |__| |___  | |_____\\ V /| || |_| |
|_____\\____| |_|      \\_/ |_(_)___/
版本：1.0
日期：2025-8-15
本程序是一个简单的线段密码翻译器。它可以将文本转换为线段密码，反之亦然。同时提供线段密码字典供参考。
我（作者）在8-14想出了这个密码。（大笑）
感谢您使用本程序！
如果您有任何问题或建议，请随时通过 BiaoZyx@outlook.com 联系我。
        """
        )


# 定义函数：显示帮助信息
def show_help():
    if lang_choice == "1":
        print(
            Fore.GREEN
            + """
This program is a simple LC code translator. It can convert text to LC code and vice versa.
It also provides a LC code dictionary for reference.
It strictly follows the translation standards of the International LC Code Association
and is capable of translating English letters, Arabic numerals, and some English punctuation marks.

It works as follows:
1. Enter the command to select the operation;
2. Enter the text or LC code to be converted,
   if you enter LC code, please use a space to separate each LC code;
3. If you are not sure about the command, you can enter "/menu" to view the menu;
4. You can exit by pressing <Ctrl + C> or entering "/exit" .
"""
        )
    elif lang_choice == "2":
        print(
            Fore.GREEN
            + """
本程序是一个简单的线段密码翻译器。它可以将文本转换为线段密码，反之亦然。
同时它提供线段密码字典供参考。
它严格遵循国际线段密码协会的翻译标准，
能够翻译英文、阿拉伯数字和一些英文标点。

它的使用方法如下：
1. 输入命令选择操作；
2. 输入文本或线段密码进行转换，
   如果你输入了线段密码，请用空格分隔每个线段密码；
3. 如果不清楚命令，可以输入“/menu”查看菜单；
4. 退出可以按 <Ctrl + C> 或输入“/exit”。
"""
        )


# 定义函数：显示菜单
def show_menu():
    if lang_choice == "1":
        print(
            Fore.MAGENTA
            + """
    1            : text to LC code
    2            : LC code to text
    3            : LC code dictionary
    /menu        : show this menu
    /version     : show version info
    /help        : show help info
    /exit        : exit the program
    /egg <color> : Easter egg
"""
        )
    if lang_choice == "2":
        print(
            Fore.MAGENTA
            + """
    1           ：文本转线段密码
    2           ：线段密码转文本
    3           ：线段密码字典
    /menu       ：显示此菜单
    /version    ：显示版本信息
    /help       ：帮助
    /exit       ：退出程序
    /egg <颜色> ：彩蛋
"""
        )


# 定义函数：显示线段密码字典
def show_LC_dict():
    if lang_choice == "1":
        print(
            Fore.GREEN
            + """
LC Code Dictionary:
A   /\\-         F   |--         K   |/\\         P   |_
B   |__'__      G   ___-        L   |-          Q   ____\\
C   ___         H   |-|         M   |\\/|        R   |_\\
D   |__         I   -|-         N   |\\|         S   __
E   |---        J   -|_         O   ____        T   -|

P   |_          U   |_|         Z   -/-
Q   ____\\       V   \\/
R   |_\\         W   \\/\\/
S   __          X   /\\
T   -|          Y   \\/|
-----------------------------------------------------------------
1   |           6   _'____      ,   /           /   //
2   _/-         7   -/          .   '           (   /_
3   __'__       8   ____'____   ?   _|'         )   \\_
4   /-|         9   ____'_      '   \\'          &   \\___/___
5   -|'_        0   ____|       !   |'          :   \''

;   '/          $   __|__
=   --          @   ___'____
+   \\-|         \\   \\\\
-   -
_   \\_    <space>  =
"   ''
"""
        )
    elif lang_choice == "2":
        print(
            Fore.GREEN
            + """
线段密码字典：
A   /\\-         F   |--         K   |/\\         P   |_
B   |__'__      G   ___-        L   |-          Q   ____\\
C   ___         H   |-|         M   |\\/|        R   |_\\
D   |__         I   -|-         N   |\\|         S   __
E   |---        J   -|_         O   ____        T   -|

P   |_          U   |_|         Z   -/-
Q   ____\\       V   \\/
R   |_\\         W   \\/\\/
S   __          X   /\\
T   -|          Y   \\/|
-----------------------------------------------------------------
1   |           6   _'____      ,   /           /   //
2   _/-         7   -/          .   '           (   /_
3   __'__       8   ____'____   ?   _|'         )   \\_
4   /-|         9   ____'_      '   \\'          &   \\___/___
5   -|'_        0   ____|       !   |'          :   \''

;   '/          $   __|__
=   --          @   ___'____
+   \\-|         \\   \\\\
-   -
_   \\_    <space>  =
"   ''
"""
        )


print_title()  # 打印标题
show_menu()  # 显示菜单


# “try”处理 <Ctrl + C> 退出有报错的问题
try:
    # 主循环
    while True:
        # 反转字典用于线段密码解码
        LC_CODE_REVERSE_DICT = {value: key for key, value in LC_CODE_DICT.items()}

        choice = input(
            Fore.BLUE + TEXT["enter_choice"] + Style.RESET_ALL
        )  # 用户输入命令
        choice = choice.strip()  # 去除前后空格

        # 根据用户选择执行操作

        # 1. 文本转线段密码
        if choice == "1":
            user_input = input(Fore.BLUE + TEXT["enter_text"] + Style.RESET_ALL)
            user_input = user_input.strip()  # 去除前后空格

            # 处理用户输入的文本
            print(Fore.GREEN + TEXT["translated_LC"], text_to_LC(user_input))

        # 2. 线段密码转文本
        elif choice == "2":
            user_input = input(Fore.BLUE + TEXT["enter_LC"] + Style.RESET_ALL)
            user_input = user_input.strip()  # 去除前后空格

            # 处理用户输入的线段密码
            print(Fore.GREEN + TEXT["translated_text"], LC_to_text(user_input))

        # 3. 显示线段密码字典
        elif choice == "3":
            show_LC_dict()

        # 4. 显示菜单
        elif choice == "/menu":
            show_menu()

        # 5. 显示版本信息
        elif choice == "/version":
            show_version()

        # 6. 显示帮助信息
        elif choice == "/help":
            show_help()

        # 7. 退出程序
        elif choice == "/exit":
            print(Fore.RED + TEXT["exit_message"])
            break

        # 8.彩蛋 （呵呵，好一个彩蛋！）
        elif choice == "/egg":
            if lang_choice == "1":
                print(
                    Fore.GREEN
                    + """
You have found the Easter egg!
There is some color information for you:
    1. red
    2. green
    3. blue
    4. yellow
    5. purple
    6. cyan
    """
                )
            elif lang_choice == "2":
                print(
                    Fore.GREEN
                    + """
你发现了彩蛋！
这里有一些颜色信息供你参考：
    1. red     #红色
    2. green   #绿色
    3. blue    #蓝色
    4. yellow  #黄色
    5. purple  #紫色
    6. cyan    #青色
    """
                )
        elif choice == "/egg red":
            if lang_choice == "1":
                print(
                    Fore.RED
                    + "0"
                    + Style.RESET_ALL
                    + " <= This is a red Easter egg! :)"
                )
            elif lang_choice == "2":
                print(Fore.RED + "0" + Style.RESET_ALL + " <= 这是一个红色的彩蛋！ :)")
        elif choice == "/egg green":
            if lang_choice == "1":
                print(
                    Fore.GREEN
                    + "0"
                    + Style.RESET_ALL
                    + " <= This is a green Easter egg! :)"
                )
            elif lang_choice == "2":
                print(
                    Fore.GREEN + "0" + Style.RESET_ALL + " <= 这是一个绿色的彩蛋！ :)"
                )
        elif choice == "/egg blue":
            if lang_choice == "1":
                print(
                    Fore.BLUE
                    + "0"
                    + Style.RESET_ALL
                    + " <= This is a blue Easter egg! :)"
                )
            elif lang_choice == "2":
                print(Fore.BLUE + "0" + Style.RESET_ALL + " <= 这是一个蓝色的彩蛋！ :)")
        elif choice == "/egg yellow":
            if lang_choice == "1":
                print(
                    Fore.YELLOW
                    + "0"
                    + Style.RESET_ALL
                    + " <= This is a yellow Easter egg! :)"
                )
            elif lang_choice == "2":
                print(
                    Fore.YELLOW + "0" + Style.RESET_ALL + " <= 这是一个黄色的彩蛋！ :)"
                )
        elif choice == "/egg purple":
            if lang_choice == "1":
                print(
                    Fore.MAGENTA
                    + "0"
                    + Style.RESET_ALL
                    + " <= This is a purple Easter egg! :)"
                )
            elif lang_choice == "2":
                print(
                    Fore.MAGENTA + "0" + Style.RESET_ALL + " <= 这是一个紫色的彩蛋！ :)"
                )
        elif choice == "/egg cyan":
            if lang_choice == "1":
                print(
                    Fore.CYAN
                    + "0"
                    + Style.RESET_ALL
                    + " <= This is a cyan Easter egg! :)"
                )
            elif lang_choice == "2":
                print(Fore.CYAN + "0" + Style.RESET_ALL + " <= 这是一个青色的彩蛋！ :)")

        # 其他输入（这某种意义上也算是彩蛋了……）
        elif choice == "":
            print(Fore.RED + TEXT["empty_input"])

        elif choice == " ":
            print(Fore.RED + TEXT["space_input"])

        else:
            print(Fore.RED + TEXT["invalid_choice"])
except KeyboardInterrupt:
    print(Fore.RED + "\n" + TEXT["exit_message"])
