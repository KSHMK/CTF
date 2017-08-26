#include<stdio.h>
#include<string.h>
char buf[4096]= {0x90};
typedef int (*Func)(char*, char*);
int main(int argc,char *argv[]){
	Func fun = (Func)buf;
	if(fun(argv[1],buf) == 1)
		return 1;
	else
		return 0;
}
