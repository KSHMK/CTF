
struct myfile{
	unsigned long long int id;
}__attribute__((packed));


void init_filesys();
struct myfile* filesys_make();
int filesys_read(struct myfile *file, size_t offset, char *dst, size_t len);
int filesys_write(struct myfile *file, size_t offset, char *src, size_t len);
void filesys_delete(struct myfile *file);