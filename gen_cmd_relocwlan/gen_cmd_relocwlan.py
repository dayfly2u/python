#!/usr/bin/env python
# author: Kyle Kim (kkim@qti.qualcomm.com)
# date: 2016/08/19

import os
import sys
import argparse
import subprocess
import re

PIDX_START = 7
PIDX_END = 102

def error_exit(message, code=1):
    sys.stderr.write("Error:\n{}".format(str(message)))
    sys.exit(code)
    
def generate_t32cmd(cfg):
    output = subprocess.Popen(["readelf", "-S", cfg.source_ko], stdout=subprocess.PIPE).communicate()[0]
    split_output = re.split("\r\n", output)

    gen_t32cmd = "B::Data.LOAD.elf <path>wlan.ko 0xffff:0x0 "
    idx_cnt = 0
    for line in split_output[PIDX_START:PIDX_END]:
        idx_cnt += 1
        if idx_cnt % 2 == 1:
            line_div = line.split("]")
            line_split = re.split("[\t ]*",line_div[1])
            cal_hexa = int(line_split[4],16) + int(cfg.base_address,16)
            gen_t32cmd += "/RELOC " + line_split[1] + " at " + hex(cal_hexa)[:-1] + " "

    gen_t32cmd += "/nocode /noclear"
    print(gen_t32cmd)
             
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''DESCRIPTION:
            relocate all elf area based on wlan.ko module address in SLIS Exynos''',
                                      formatter_class=argparse.RawDescriptionHelpFormatter,
                                      epilog='''USAGE:
            {0} -d [my_folder] -s <wlan_symbol_name> -b <base_address>'''.format(os.path.basename(sys.argv[0])))

    parser.add_argument('--dir', '-d',
                        help='folder to search in; by default current folder',
                        default='.')

    parser.add_argument('--source_ko', '-s',
                        help='source (unstripped wlan ko)',
                        default='wlan.ko')

    parser.add_argument('--base_address', '-b',
                        help='base address in exynos', required=True)

    config = parser.parse_args(sys.argv[1:])

    try:
        if not os.path.exists(config.source_ko):
            error_exit(
                "Input file'{}' not found.\n".format(config.source_ko))

        if os.path.getsize(config.source_ko) == 0:
            error_exit(
                "Input file '{}' has no data.\n".format(config.source_ko))

        generate_t32cmd(config)
    except ValueError as ve:
                error_exit(str(ve))
    except IOError as ioe:
                error_exit(str(ioe))
    except Exception as e:
                error_exit(str(e))

