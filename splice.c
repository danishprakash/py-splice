#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

ssize_t splice_copy(int fd_out, int fd_in, size_t len) {
    int fd_pipe[2];
    ssize_t total_bytes_sent = 0;
    size_t buf_size = 128;
    loff_t in_off = 0;
    loff_t out_off = 0;

    if (pipe(fd_pipe) < 0) {
        perror("Error creating pipe");
        return 1;
    }

    printf("len before: %zd\n", len);
    printf("stat before: %zd\n", buf_size);

    while(len > 0) {
        if (buf_size > len) buf_size = len;
        // splice data to pipe
        if ((splice(fd_in, &in_off, fd_pipe[1], NULL, buf_size, SPLICE_F_MOVE)) == -1) {
            perror("assplice");
            return 1;
        }

        // splice data from pipe to fd_out
        if ((splice(fd_pipe[0], NULL, fd_out, &out_off, buf_size, SPLICE_F_MOVE)) == -1) {
            perror("splice");
            return 1;
        }

        len -= buf_size;
        printf("total bytes: %zd\n", len);
    }
    return 1;
}

int main(){
    int fin, fout;
    size_t fsize;
    fin = open("read.txt", O_RDONLY);
    fout = open("write.txt", O_WRONLY);
    fsize = lseek(fin, 0, SEEK_END);

    /* printf("%zd", fsize); */
    printf("%zd", splice_copy(fout, fin, fsize));
}
