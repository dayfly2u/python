#!/usr/bin/env python
import sys
import os

OUTFILE_PREFIX = 'out_'

def error_exit(message, code=1):
    sys.stderr.write("Error:\n{}".format(str(message)))
    sys.exit(code)
                
def bsplit(in_filename, bytes_per_file):
    in_file = open(in_filename, "rb")
    outfile_idx = 1
    out_filename = OUTFILE_PREFIX + str(outfile_idx).zfill(4)
    out_file = open(out_filename, "wb")

    byte_count = tot_byte_count = file_count = 0
    c = in_file.read(1)

    while c != '':
        byte_count += 1
        out_file.write(c)
        if byte_count >= bytes_per_file:
            tot_byte_count += byte_count
            byte_count = 0
            file_count += 1
            out_file.close()
            outfile_idx += 1
            out_filename = OUTFILE_PREFIX + str(outfile_idx).zfill(4)
            out_file = open(out_filename, "wb")
        c = in_file.read(1)

    in_file.close()
    if not out_file.closed:
        out_file.close()

    if byte_count == 0:
        os.remove(out_filename)


    
def usage():
    sys.stderr.write(
        "Usage: python {} in_filename bytes_per_file\n".format(sys.argv[0]))
    sys.stderr.write(
        "splits in_filename into files with bytes_per_file bytes\n")

def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    try:
        in_filename = sys.argv[1]
        if not os.path.exists(in_filename):
            error_exit(
                "Input file'{}' not found.\n".format(in_filename))

        if os.path.getsize(in_filename) == 0:
            error_exit(
                "Input file '{}' has no data.\n".format(in_filename))

        bytes_per_file = int(sys.argv[2])
        if bytes_per_file <= 0:
            error_exit(
                "bytes_per_file cannot be less than or equal to 0.\n")

        bsplit(in_filename, bytes_per_file)
    except ValueError as ve:
                error_exit(str(ve))
    except IOError as ioe:
                error_exit(str(ioe))
    except Exception as e:
                error_exit(str(e))


if __name__ == '__main__':
                main()
                
