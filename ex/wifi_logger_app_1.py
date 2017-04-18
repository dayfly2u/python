import sys
import os
import os.path
import fileinput
import sys
import time
import re

input_path = r"C:\Users\kkim\Desktop\cn02676088"
def main():
    if os.path.exists(input_path+r"\dram_0x80000000--0xbfffffff.lst")==False:
        # addLabel(issue,"FRAMEWORK_ISSUE")
        print "****"
        pass
    else:
        if os.path.exists(input_path+r"\log4mdump1.txt")==False:
            try:
                loc1 = "C:\temp\strings\str1.txt"
                loc2 = "C:\temp\strings\str2.txt"
                loc3 = "C:\temp\strings\str3.txt"
                loc4 = "C:\temp\strings\str4.txt"
                op_file=open(r"C:\temp\strings\op.txt","w")
                #print "Hi"
                if os.path.exists(input_path+r"\dram_0x80000000--0xbfffffff.lst"):
                    loc1=str(r"C:\temp\strings\strings.exe "+input_path+r"\dram_0x80000000--0xbfffffff.lst >C:\temp\strings\str1.txt")#+str(FILE_DICT["crash_location"]
                    print loc1
                    print "Generating str1.txt"
                    os.system(loc1) #this will perform above operation i.e., it will take DDRCS0.BIN at that location and applies string.exe to that and output it into str1.txt
                    if loc1!="":
                        print "Finding the file containing Wlan in str1 :"
                        for line in fileinput.input([r"C:\temp\strings\str1.txt"]):
                            #print "Hello"
                            if  (line.find("] wlan: ["))>-1:
                                match=""
                                match =re.search('\[(.*)\] wlan: ' , line)
                                if match!=None:
                                    match=match.group(1)
                                match=str(match)
                                #print ("match = ",match)
                                if match!="None":
                                    while ((match.find("["))>-1 ):
                                        match=str(match)
                                        match=re.search('\[(.*)',match).group(1)
                                        #print match
                                prepend=""
                                if match!="None":
                                    prepend=match
                                    prepend=re.sub(' ','',prepend)
                                else :
                                    prepend=""
                                m1=prepend+str(line)
                                op_file.write(m1)
                       #print line
                        os.remove(r"C:\temp\strings\str1.txt")
                        print "Removed str1.txt"
                if os.path.exists(input_path+r"\OCIMEM.BIN"):
                    loc2=str(r"C:\temp\strings\strings.exe "+input_path+r"\OCIMEM.BIN >C:\temp\strings\str2.txt")#+str(FILE_DICT["crash_location"])
                    print loc2
                    print "Generating str2.txt"
                    os.system(loc2) #this will perform above operation i.e., it will take DDRCS1.BIN at that location and applies string.exe to that and output it into str2.txt
                    if loc2!="":
                        print "Finding the file containing Wlan in str2 :"
                        for line in fileinput.input([r"C:\temp\strings\str2.txt"]):
                            #print "Hello"
                            if  (line.find("] wlan: ["))>-1: 
                                match=""
                                match =re.search('\[(.*)\] wlan: ' , line)
                                if match!=None:
                                    match=match.group(1)
                                match=str(match)
                                #print ("match = ",match)
                                if match!="None":
                                    while ((match.find("["))>-1 ):
                                        match=str(match)
                                        match=re.search('\[(.*)',match).group(1)
                                        #print match
                                prepend=""
                                if match!="None":
                                    prepend=match
                                    prepend=re.sub(' ','',prepend)
                                else :
                                    prepend=""
                                m1=prepend+str(line)
                                op_file.write(m1)
                        #print line
                        os.remove(r"C:\temp\strings\str2.txt")
                        print "Removed str2.txt"
                if os.path.exists(input_path+r"\dram1_0xc0000000--0xffffffff.lst"):
                    loc2=str(r"C:\temp\strings\strings.exe "+input_path+r"\dram1_0xc0000000--0xffffffff.lst >C:\temp\strings\str3.txt")#+str(FILE_DICT["crash_location"])
                    print loc2
                    print "Generating str3.txt"
                    os.system(loc2) #this will perform above operation i.e., it will take DDRCS1.BIN at that location and applies string.exe to that and output it into str2.txt
                    if loc3!="":
                        print "Finding the file containing Wlan in str3 :"
                        for line in fileinput.input([r"C:\temp\strings\str3.txt"]):
                            #print "Hello"
                            if  (line.find("] wlan: ["))>-1:
                                match=""
                                match =re.search('\[(.*)\] wlan: ' , line)
                                if match!=None:
                                    match=match.group(1)
                                match=str(match)
                                #print ("match = ",match)
                                if match!="None":
                                    while ((match.find("["))>-1 ):
                                        match=str(match)
                                        match=re.search('\[(.*)',match).group(1)
                                        #print match
                                prepend=""
                                if match!="None":
                                    prepend=match
                                    prepend=re.sub(' ','',prepend)
                                else :
                                    prepend=""
                                m1=prepend+str(line)
                                op_file.write(m1)
                        #print line
                        os.remove(r"C:\temp\strings\str3.txt")
                        print "Removed str3.txt"
                if os.path.exists(input_path+r"\DDRCS3.BIN"):
                    loc2=str(r"C:\temp\strings\strings.exe "+input_path+r"\DDRCS3.BIN >C:\temp\strings\str4.txt")#+str(FILE_DICT["crash_location"])
                    print loc2
                    print "Generating str4.txt"
                    os.system(loc2) #this will perform above operation i.e., it will take DDRCS1.BIN at that location and applies string.exe to that and output it into str2.txt
                    if loc4!="":
                        print "Finding the file containing Wlan in str4 :"
                        for line in fileinput.input([r"C:\temp\strings\str4.txt"]):
                            #print "Hello"
                            if  (line.find("] wlan: ["))>-1:
                                match=""
                                match =re.search('\[(.*)\] wlan: ' , line)
                                if match!=None:
                                    match=match.group(1)
                                match=str(match)
                                #print ("match = ",match)
                                if match!="None":
                                    while ((match.find("["))>-1 ):
                                        match=str(match)
                                        match=re.search('\[(.*)',match).group(1)
                                        #print match
                                prepend=""
                                if match!="None":
                                    prepend=match
                                    prepend=re.sub(' ','',prepend)
                                else :
                                    prepend=""
                                m1=prepend+str(line)
                                op_file.write(m1)
                        #print line
                        os.remove(r"C:\temp\strings\str4.txt")
                        print "Removed str4.txt"
            except Exception as err:
                print err





            print "Successfully op.txt is generated\n"
            print "sorting the file op.txt"
            op_file.close()
            loc1=r"sort.exe "+r"C:\temp\strings\op.txt "+r"/o "+input_path+r"\log4mdump1.txt /rec 65535"
            os.system(loc1)
            os.remove(r"C:\temp\strings\op.txt")
            loggerApp = open("temp.txt",'w')
            for line in fileinput.input([input_path+r"\log4mdump1.txt"]):
                line=line.split('[',1)[1]
                loggerApp.write(line)
            loggerApp.close()
            op_file.close()
            print "sort start"
            loc1=r"sort.exe temp.txt /o " + input_path+r"\log4mdump2.txt /rec 65535"
            os.system(loc1)
            print "sort stop"
            # addLabel(issue,"LOGGER_ANALYZED")
            print r"log4mdump.txt successfully generated and it is in dump folder "
        else :
            print r"File log4mdump.txt Already exist in the specified location"
            # addLabel(issue,"LOGGER_ANALYZED")

if __name__ == '__main__':
    main()
