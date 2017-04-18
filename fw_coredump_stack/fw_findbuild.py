#!/usr/bin/env python
# author: Kyle Kim (kkim@qti.qualcomm.com)
# date: 2017/03/23

import os
import sys
import argparse
import subprocess
import re
import shutil 


def error_exit(message, code=1):
    sys.stderr.write("Error:\n{}".format(str(message)))
    sys.exit(code)
    
def xt_addr2line(addr):
    output = subprocess.Popen(["xt-addr2line", "-f", "-e", "sw.rom.out", addr], stdout=subprocess.PIPE).communicate()[0]
    if output[0:2] == "??":
        output = subprocess.Popen(["xt-addr2line", "-f" ,"-e", "athwlan.out", addr], stdout=subprocess.PIPE).communicate()[0]
    if output[0:2] == "??":
        output = "symbol not found"
    return output 
    
def parse_fwcoredump(cfg):
    result = ""
    findstr = "[a-fA-F0-9]{8}"
        
    print "input target coredump: (type 'end' to finish it)"
    contents = []
    while True:
        line = raw_input("")
        if line == "end":
            break
        contents.append(line)

    index = 0
    for inputline in contents:
        splits = re.findall(findstr, inputline)
        
        for token in splits:
            if index >= 20:
                if index % 4 == 0:
                    result += "[" + str(index) + "]" + "0x" + token + " : \n" + xt_addr2line(token[2:8]) + "\n"
            else:
                result += "[" + str(index) + "]" + "0x" + token
                if index == 0:
                    result += " : target ID\n"
                elif index == 1:
                    result += " : assert line\n"                
                elif index == 2: 
                    result += " : PC\n" + xt_addr2line(token[2:8]) + "\n"
                elif index == 3: 
                    result += " : badvaddr\n"    
                elif index == 4: 
                    result += " : xt_pc\n"    
                elif index == 5: 
                    result += " : xt_ps\n"    
                elif index == 6: 
                    result += " : xt_sar\n"    
                elif index == 7: 
                    result += " : xt_vpri\n"    
                elif index == 8: 
                    result += " : xt_a2\n"    
                elif index == 9: 
                    result += " : xt_a3\n"    
                elif index == 10: 
                    result += " : xt_a4\n"    
                elif index == 11: 
                    result += " : xt_a5\n"    
                elif index == 12: 
                    result += " : xt_exccause\n"    
                elif index == 13: 
                    result += " : xt_lcount\n"    
                elif index == 14: 
                    result += " : xt_lbeg\n"    
                elif index == 15: 
                    result += " : xt_lend\n"    
                elif index == 16: 
                    result += " : epc1\n"    
                elif index == 17: 
                    result += " : epc2\n"    
                elif index == 18: 
                    result += " : epc3\n"    
                elif index == 19: 
                    result += " : epc4\n"                        
                    
            index += 1 

    print result
               
def findbuild(bid):
    find_result = subprocess.Popen([".\FindBuild.exe", bid], stdout=subprocess.PIPE).communicate()[0]         
    for line in find_result.splitlines(): 
        print line
        words = line.split()
        if words[0] == "Location:":
            fw_path = words[1] + r"\wlan_proc\wlan\fw\target\.output\AR6320\npl1.0\image"
            
            if os.path.exists(fw_path):
                if os.path.isfile(fw_path + r"\sw.rom.out"):
                    shutil.copy2(fw_path + r"\sw.rom.out", r".")
                    print fw_path + r"\sw.rom.out copied to the local"
                    shutil.copy2(r".\sw.rom.out",r"\\harv-kkim\kyle\fwdump")
                if os.path.isfile(fw_path + r"\athwlan.out"):
                    shutil.copy2(fw_path + r"\athwlan.out", r".")
                    print fw_path + r"\athwlan.out copied to the local" 
                    shutil.copy2(r".\athwlan.out",r"\\harv-kkim\kyle\fwdump")
            else:
                print fw_path + "does not exist"
            return 
        
    print "Not found"
        
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''DESCRIPTION:
            findbuild ''',
                                      formatter_class=argparse.RawDescriptionHelpFormatter,
                                      epilog='''USAGE:
            {0} [FW build ID] -t <32|64>'''.format(os.path.basename(sys.argv[0])))
    
    parser.add_argument('--type', '-t',
                        help='kernel 32bit or 64bit?',
                        default='64')
                        
    config = parser.parse_args(sys.argv[2:])

    try:
        if not os.path.exists(".\FindBuild.exe"):
            error_exit("Findit util not found.\n")
        findbuild(sys.argv[1])
        #parse_fwcoredump(config)
    except ValueError as ve:
                error_exit(str(ve))
    except IOError as ioe:
                error_exit(str(ioe))
    except Exception as e:
                error_exit(str(e))

