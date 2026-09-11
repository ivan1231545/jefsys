import sys, os, subprocess
from sysdata.utils.helputils import color

def cd(path: str) -> None:
    if os.path.exists(path):
        os.chdir(path)
    else:
        print(f"jefsys: cd: folder '{path}' does not exist")

def ls(path: str=".") -> None:
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                print(f"file: {entry.name}")
            if entry.is_dir():
                print(f"dir:  {color(entry.name, "1;34")}")
                

def shell(cmd):
    try:
        shcmd = cmd[1:]
        shcmd = " ".join(shcmd)
        result = subprocess.run(
            shcmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,          # Автоматически декодирует байты в str
            timeout=30          # Защита от зависания (можно убрать)
        )
    
        # Выводим stdout через твой raw_write
        if result.stdout:
            print(result.stdout)
    
        # Если есть ошибки, выводим их тоже
        if result.stderr:
            print(result.stderr)  # 2 = stderr
    except Exception as e:
        print("shell: exception: " + str(e))
def echo(cmd: list) -> None:
    if not cmd:
        return
    print(" ".join(cmd).strip())

def txtedit(path: str) -> None:
    # Если файла нет — создаём пустой
    if not os.path.exists(path):
        open(path, 'a').close()

    # Запускаем micro (или nano, если micro нет)
    try:
        subprocess.run(["micro", path])
    except FileNotFoundError:
        try:
            subprocess.run(["nano", path])
        except FileNotFoundError:
            print("This programm uses micro or nano but no micro nor nano was found. Install it by running:\nlinux: apt intsall micro nano")
