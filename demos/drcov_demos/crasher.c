#include <stdlib.h>
#include <stdio.h>
#include <signal.h>

void test(char *buf)
{
    int n=0;
    if(buf[0]=='b') n++;
    if(buf[1]=='a') n++;
    if(buf[2]=='d') n++;
    if(buf[3]=='!') n++;
    if(n == 4) {
        raise(SIGSEGV);
    }
}

int main(int argc, char *argv[])
{
    char buf[5];
    FILE* my_file = NULL;

    my_file = fopen(argv[1], "r");
    if (my_file != 0)
    {
        fscanf(my_file, "%4c", &buf);
        test(buf);
        fclose(my_file);
    }
}
