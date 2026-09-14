import sys, os, subprocess, random
import readline
import platform

# читаем историю и обрабатываем команды "^[[C", "^[[A" и т.д.
# Опционально: файл, где хранить историю между запусками
HISTORY_FILE = os.path.expanduser("~/.jefsys_history")

try:
    readline.read_history_file(HISTORY_FILE)
except FileNotFoundError:
    pass

readline.set_history_length(1000)  # сколько команд хранить

curarch = platform.machine()
base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.join(os.path.abspath(__file__), "sysdata", "utils", "coreutils.py"))  # если shell.py лежит рядом с sys/
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from sysdata.utils.coreutils import *
from sysdata.utils.helputils import *

root = False
'''
def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"
'''
def runcmd(cmd):
    global root
    match cmd[0]:
        case "shell":
            if len(cmd) < 2:
                print("jefsys: shell: missing 1 requered argument: command\nUsage: shell <command>\nWhere command is more than 1-word argument.\n\nRuns command in external shell.")
                return
            shell(cmd)
        case "shutdown":
            if root:
                print("jefsys exited with code 232 (SUPERUSR_EXIT_CAUGHT)")
            else:
                print("jefsys exited with code 235 (EXECUSR_EXIT_CAUGHT)")
            exit()
        case "su":
            try:
                with open("sysdata/rooted-usrs", "r") as f:
                    if f.readlines()[0].strip("\n").strip() == "current":
                        root = True
            except FileNotFoundError:
                print("No file rooted-usrs in sysdata/, root failed")
        case "cd":
            if len(cmd) < 2:
                print("jefsys: cd: missing 1 requered argument: folderpath\nUsage: cd <folderpath>\nWhere folderpath is folder path argument.\n\nChanges current directory.")
                return
            cd(cmd[1])
        case "ls":
            path = "."
            if len(cmd) >= 2:
                path = cmd[1]
            ls(path)
        case "echo":
            echo(cmd[1:])
        case "jpkg":
            from sysdata.utils.jpkg import jpkg
            jpkg(cmd)
        case ".":
            if not os.path.isfile(cmd[1]):
                return
            if not cmd[1].split(".") == "jesh":
                print(f"jefsys: jesh: file not supported: \"{cmd[1]}\". Supported files ends with .jesh.")
                return
            with open(cmd[1], "r") as script:
                for jeshcmd in script.readlines():
                    if not jeshcmd or jeshcmd.startswith("#"):
                        continue
                    runcmd(jeshcmd.strip("\n").strip().split())
        case "txtedit":
            if len(cmd) < 2: return
            txtedit(cmd[1])
        case "randomnum":
            if len(cmd) < 2: return
            print(random.randint(int(cmd[1]), int(cmd[2])))
        case "cat":
            if len(cmd) < 2: return
            result = subprocess.run(
                [f"bin/{curarch}/cat_utility", cmd[1]],
                capture_output=True,
                text=True
            )
            print(result.stdout)
        case _:
             if cmd[0] == "":
                 return
             if os.path.isfile(cmd[0]) &  cmd[0].endswith("jesh"):
                runcmd(f". {cmd[0]}")
             print(f"No such cmd, programm, bash, or shell script: '{cmd[0]}'")
while True:
    try:
        if root:
            cmd = input(color(os.getcwd() + "/", 36) + color(" supr$ ", 35)).split(" ")
        else:
            cmd = input("\033[36m" + os.getcwd() + "/\033[0m exec$ ").split(" ")
        runcmd(cmd)
    except EOFError:
        continue
# сохраняем историю ввода (можно опустить)
try:
    readline.write_history_file(HISTORY_FILE)
except Exception:
    pass  # на случай ошибок записи
