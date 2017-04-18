#!/usr/bin/env python
# author: Kyle Kim (kkim@qti.qualcomm.com)
# date: 2016/09/30

import os
import sys
import argparse
import subprocess
import re

def error_exit(message, code=1):
    sys.stderr.write("Error:\n{}".format(str(message)))
    sys.exit(code)
    
def generate_t32cmd(cfg):
    gen_t32cmd = ""
    if config.type == "64":
        findstr = "pc|lr|sp|x\d{1,2}|[a-f0-9]{16}"
    else:
        findstr = "pc|lr|sp|ip|fp|psr|r\d{1,2}|[a-f0-9]{8}"
        
    with open(cfg.source_kmsg, "r") as input:
        for inputline in input.readlines():
            splits = re.findall(findstr, inputline)
            index = 0
            for token in splits:
                if index % 2 == 0:
                    if config.type == "64":
                        if token.upper() == 'LR':
                            gen_t32cmd += "R.S ELR"
                        else:
                            gen_t32cmd += "R.S " + token.upper()
                    else:
                        if token.upper() == 'LR':
                            gen_t32cmd += "R.S R14"
                        elif token.upper() == 'SP':
                            gen_t32cmd += "R.S R13"
                        elif token.upper() == 'IP':
                            gen_t32cmd += "R.S R12"
                        elif token.upper() == 'FP':
                            gen_t32cmd += "R.S R11"
                        elif token.upper() == 'PSR':
                            gen_t32cmd += "R.S CPSR"
                        else:
                            gen_t32cmd += "R.S " + token.upper()
                else:
                    gen_t32cmd += " 0x" + token + "\r\n"

                index += 1

    print(gen_t32cmd)
    with open(cfg.source_kmsg + ".cmm", "w") as output:
        output.write(gen_t32cmd)

					             
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''DESCRIPTION:
            generate T32 command for coredump in case of apps panic''',
                                      formatter_class=argparse.RawDescriptionHelpFormatter,
                                      epilog='''USAGE:
            {0} -d [my_folder] -s <source_kmsg> -t <32|64>'''.format(os.path.basename(sys.argv[0])))

    parser.add_argument('--dir', '-d',
                        help='folder to search in; by default current folder',
                        default='.')

    parser.add_argument('--source_kmsg', '-s',
                        help='kernel log which prints coredump',
                        default='dump.txt')
    
    parser.add_argument('--type', '-t',
                        help='kernel 32bit or 64bit?',
                        default='64')
						
    config = parser.parse_args(sys.argv[1:])

    try:
        if not os.path.exists(config.source_kmsg):
            error_exit(
                "Input file'{}' not found.\n".format(config.source_kmsg))

        if os.path.getsize(config.source_kmsg) == 0:
            error_exit(
                "Input file '{}' has no data.\n".format(config.source_kmsg))

        generate_t32cmd(config)
    except ValueError as ve:
                error_exit(str(ve))
    except IOError as ioe:
                error_exit(str(ioe))
    except Exception as e:
                error_exit(str(e))

