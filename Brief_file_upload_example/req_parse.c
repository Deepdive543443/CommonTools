#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BOUNDARY "\r\n------WebKitFormBoundary****************--\r\n"

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

        ptr_l = (char *)    strstr(bytes, "filename=\"") + sizeof("filename=\"") - 1;
        ptr_r = (char *)    strstr(ptr_l, "\"\r\n") + 1;
        if (ptr_l && ptr_r) snprintf(filename, ptr_r - ptr_l, "%s", ptr_l);

        ptr_l = (char *)    strstr(bytes, "\"filesize\"\r\n\r\n") + sizeof("\"filesize\"\r\n\r\n") - 1;
        ptr_r = (char *)    strstr(ptr_l, "\r\n") + 1;
        if (ptr_l && ptr_r) {
            char buf[128];
            snprintf(buf, ptr_r - ptr_l, "%s", ptr_l);
            file_size = atoi(buf);
        }

        ptr_l = (char *)    strstr(bytes, "Content-Type: ") + sizeof("Content-Type: ") - 1;
        ptr_r = (char *)    strstr(ptr_l, "\r\n\r\n") + sizeof("\r\n\r\n") - 1;
        if (ptr_l && ptr_r) snprintf(filetype, ptr_r - ptr_l, "%s", ptr_l);


        FILE *parsed_file = fopen(filename, "wb");
        printf("filename:         %s\n", filename);
        printf("Content-Type:     %s\n", filetype);
        printf("filesize:        %ld\n", file_size);

        if (parsed_file) {
            fwrite(ptr_r, file_size, 1, parsed_file);
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