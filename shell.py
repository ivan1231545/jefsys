import sys, os, subprocess

base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.join(os.path.abspath(__file__), "sysdata", "utils", "coreutils.py"))  # если shell.py лежит рядом с sys/
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from sysdata.utils.coreutils import ls, cd, shell, echo

root = False

def runcmd(cmd):
    global root
    match cmd[0]:
        case "shell":
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
            cd(cmd[1])
        case "ls":
            ls(cmd[1])
        case "echo":
            echo(cmd[1:])
        case _:
             print(f"No such cmd, programm, bash, or shell script: '{cmd[0]}'")
while True:
    if root:
        cmd = input(os.getcwd() + "/ root$ ").split(" ")
    else:
        cmd = input(os.getcwd() + "/ e$ ").split(" ")
    runcmd(cmd)
