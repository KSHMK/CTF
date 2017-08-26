#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>
char buf[1000];
typedef int (*FuncPtr)(void);
void sig_handler(int signo)
{
	exit(-1);
}
int main(int argc, char *argv[])
{
	char buf[1000];
	int len;
	unsigned int EAX;
	if (signal(SIGSEGV, sig_handler) == SIG_ERR)
		return -2;

	EAX = atoi(argv[1]);
	len = atoi(argv[2]);

	buf[0] = '\xb8';
	*(unsigned int*)&buf[1] = EAX;
	read(0,&buf[5],len);
	
	buf[len+5] = '\xc3';
	FuncPtr runner = (FuncPtr*)buf;
	printf("%u\n", runner());
	return 0;
}
