#include <stdio.h>
#include "filesys.h"

int main(void)
{
	init_filesys();
	struct myfile *file;
	file = filesys_make();
	printf("%x\n",file);
	return 0;
}