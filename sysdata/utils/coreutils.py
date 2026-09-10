import sys, os

def cd(path: str) -> None:
    if os.path.exists(path):
        os.chdir(path)
    else:
        print(f"jefsys: cd: folder '{path}' does not exist")

def ls(path: str=".") -> None:
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                print(f"file: {entry}")
            if entry.is_dir():
                print(f"dir:  {entry}")

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
