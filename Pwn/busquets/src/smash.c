#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>

void print_flag() {
    char buf[2048];
    int fd = open("/flag.txt", O_RDONLY);
    if (fd == -1)
        return;
    memset(buf, 0, sizeof(buf));
    ssize_t size = read(fd, buf, sizeof(buf));
    if (size != -1)
        write(1, buf, size);
    close(fd);
}

/* rest unchanged, but using a struct for deterministic layout */
void vulnerable(void) {
    struct {
        char name[64];
        volatile unsigned int authorized;
    } u;

    /* initialize authorized to 0 */
    u.authorized = 0;

    puts("Who ARE YOUU???");
    ssize_t n = read(STDIN_FILENO, u.name, 512);
    if (n < 0) {
        perror("read");
        exit(1);
    }

    /* ensure a null-terminated name (search only within name buffer) */
    for (int i = 0; i < (int)n && i < (int)sizeof(u.name); ++i) {
        if (u.name[i] == '\n') { u.name[i] = '\0'; break; }
    }

    printf("Hi, %s\n", u.name);

    if (u.authorized == 0x1337beef) {
        puts("Authorized! Revealing flag:");
        print_flag();
    } else {
        puts("Access denied: you are not authorized.");
    }
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("=== SmashMore (I love Burgers) ===");
    vulnerable();
    return 0;
}
