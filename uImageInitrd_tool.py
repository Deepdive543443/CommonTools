import argparse

INITRD_FILESIZE_OFFSET = 54
INITRD_FILESIZE_SIZE   = 8
ALIGN_SIZE             = 0x40000
SIGNATURE_SIZE         = 0x100

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-k', '--kernel', required=True, default=None, help="Uncompressed Linux Kernel(uImage)") 
PARSER.add_argument('-r', '--ramdisk', required=True, default=None, help="Ramdisk image(initrd.cpio)")
PARSER.add_argument('-o', '--output', required=True, default=None, help="Save path of the uImageInitrd.bin")
ARGS = PARSER.parse_args()

if __name__ == "__main__":
    with open(ARGS.kernel, "rb") as f:
        kernel_bytes = f.read()
        f.close()

    with open(ARGS.ramdisk, "rb") as f:
        initrd_bytes = bytes(f.read())
        f.close()

    kernel_size     = len(kernel_bytes)
    initrd_size     = len(initrd_bytes) - SIGNATURE_SIZE
    kernel_pad_size = int(kernel_size / ALIGN_SIZE + 1) * ALIGN_SIZE - kernel_size

    # Padding and inserting
    kernel_bytes += (0).to_bytes(1, "little") * kernel_pad_size
    initrd_bytes = (initrd_bytes[:INITRD_FILESIZE_OFFSET] 
                    + initrd_size.to_bytes(8, "little") # Insert  
                    + initrd_bytes[INITRD_FILESIZE_OFFSET + INITRD_FILESIZE_SIZE:])
                
    print(f"kernel_size: {kernel_size}\ninitrd_size: {initrd_size}\nkernel_pad_size: {kernel_pad_size}\n"
          f"Padded_kernel_size: {len(kernel_bytes)}\n")

    with open(ARGS.output, "wb") as f:
        f.write(kernel_bytes + initrd_bytes)
        f.close()
        print(f"Saving concat image to: {ARGS.output}")

