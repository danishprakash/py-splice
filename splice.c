#define GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

// create pipe
static int fd_pipe[2];
// TODO: error handling for creation of pipe
//
pipe(fd_pipe);

off_t fsize(const char *filename) {
    struct stat st; 

    if (stat(filename, &st) == 0)
        return st.st_size;

    return -1; 
}

int splice_copy(int fd_out, int fd_in, ssize_t len) {
    ssize_t bytes, bytes_sent, bytes_in_pipe;
    size_t total_bytes_sent;
    loff_t in_off = 0;
    loff_t out_off = 0;

    while(total_bytes_sent < len) {
        // splice data to pipe
        if ((bytes = splice(fd_in, in_off, fd_pipe[1], NULL, len-total_bytes_sent)) <= 0) {
            perror("splice");
            return 1;
        }

        // splice data from pipe to fd_out
        if ((bytes = splice(fd_pipe[0], NULL, fd_out, out_off, bytes)) <= 0) {
            perror("splice");
            return 1;
        }

        total_bytes_sent += bytes;
    }
    return total_bytes_sent;
}

int main(){
    FILE *fin, *fout;
    fin = fopen("read.txt", "r");
    fout = fopen("write.txt", "w");
    printf(splice_copy(fileno(fin), fileno(fout), fsize(fin)));
}
