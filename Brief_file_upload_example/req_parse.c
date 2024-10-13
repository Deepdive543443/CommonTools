#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    FILE *f_ptr = fopen("uploaded_files/byte_dump", "rb");
    if (f_ptr) {
        long byte_size, file_size;
        char filename[128], filetype[128], *ptr_l = NULL, *ptr_r = NULL; 

        fseek(f_ptr, 0, SEEK_END);
        byte_size = ftell(f_ptr);
        fseek(f_ptr, 0, SEEK_SET);
        printf("Parsing Request bytesize: %ld\n", byte_size);
        
        char *bytes = malloc(byte_size);
        fread(bytes, byte_size, 1, f_ptr);

        ptr_l = (char *)    strstr(bytes, "<SIZE>") + sizeof("<SIZE>") - 1;
        ptr_r = (char *)    strstr(ptr_l, "<NAME>") + 1;
        if (ptr_l && ptr_r) {
            snprintf(filename, ptr_r - ptr_l, "%s", ptr_l);
            file_size = atoi(filename);
        }

        ptr_l = (char *)    strstr(bytes, "<NAME>") + sizeof("<NAME>") - 1;
        ptr_r = (char *)    strstr(ptr_l, "<BYTE>") + 1;
        if (ptr_l && ptr_r) snprintf(filename, ptr_r - ptr_l, "%s", ptr_l);

        ptr_l = (char *)    strstr(bytes, "<BYTE>") + sizeof("<BYTE>") - 1;

        FILE *parsed_file = fopen(filename, "wb");
        printf("filename:         %s\n", filename);
        printf("filesize:        %ld\n", file_size);
        if (parsed_file) {
            fwrite(ptr_l, file_size, 1, parsed_file);
            fclose(parsed_file);
        } else {
            char errorString[128];
            perror(errorString);
            printf("%s\n", errorString);
        } 

        free(bytes);
        fclose(f_ptr);

    } else {
        char errorString[128];
        perror(errorString);
        printf("%s\n", errorString);
    }
    return 0;
}