.data
python_path: .asciz "/data/data/com.termux/files/usr/bin/python3"
script_path: .asciz "/data/data/com.termux/files/home/jefsys/shell.py"

.text
.global _start
_start:
    // Аргументы для execve: argv[0]=python, argv[1]=script, argv[2]=NULL
    ldr r0, =python_path
    ldr r1, =arg_array
    mov r2, #0                  // envp = NULL
    mov r7, #11                 // sys_execve
    svc #0

    // Если попали сюда — ошибка
    mov r0, #1                  // exit code
    mov r7, #1                  // sys_exit
    svc #0

arg_array:
    .word python_path
    .word script_path
    .word 0
