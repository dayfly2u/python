import sys

def main(argv):
    if len(argv) != 4:
        return -2
    with open(argv[2], "w") as output:
        output.write("#include <stdint.h>\n")
        output.write("const uint8_t %s[] = {\n" % argv[3])
        with open(argv[1], "rb") as input:
            count = 0
            for inputByte in input.read():
                if count > 0:
                    output.write(',')
                output.write("0x%02x" % (ord(inputByte)))
                count += 1
                if (count % 50) == 0:
                    output.write("\n")
            if (count % 50) != 0:
                output.write("\n")
        output.write("};\n")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
