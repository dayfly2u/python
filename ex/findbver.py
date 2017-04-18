import subprocess
import re
import xml.etree.ElementTree as ET
import sys    
import os

def processApps(fpath):
    print "APPS:  " + fpath
    f = open(fpath+r'\android.plf', "r")
    match = re.search(r'^@V([A-Z|a-z|_|\.|0-9]+)', f.readline(), re.MULTILINE)
    if match:
        print "\tAU: A" + match.group(1)   
    f.close()
    f = open(fpath+r'\LINUX\android\vendor\qcom\proprietary\wlan\prima\CORE\MAC\inc\qwlan_version.h',"r")
    for line in f:
        match = re.search('QWLAN_VERSIONSTR\s+"(\d\.\d+\.\d+\.\d+)', line)
        if match:
            print "\tWLAN Host: " + match.group(1)
            break
    f.close()     

def processWcnss(fpath):
    print "WCNSS: " + fpath
    psuffix = r'wcnss_proc\build\ms\bin\PIL_IMAGES'
    for dirname, dirnames, filenames in os.walk(fpath + psuffix):
        if len(dirnames) == 1:
            print "\tBIN: " + psuffix + "\\" + dirnames[0]
            break

def processRpm(fpath):
    print "RPM:   " + fpath

def processBoot(fpath):
    print "BOOT:  " + fpath
    
def processMeta(fpath):
    tree = ET.parse(fpath + "\\contents.xml")
    root = tree.getroot()
    for rootpath in root.getiterator('windows_root_path'):
        pathvar = rootpath.attrib.get('cmm_root_path_var')
        if pathvar == 'APPS_BUILD_ROOT':
            processApps(rootpath.text)
        elif pathvar == 'WCNSS_BUILD_ROOT':
            processWcnss(rootpath.text)
        elif pathvar == 'RPM_BUILD_ROOT':
            processRpm(rootpath.text)
        elif pathvar == 'BOOT_BUILD_ROOT':
            processBoot(rootpath.text)
            
if len(sys.argv)==1:
    print "Usage: python metaver.py [META ID]"
    exit()

output = subprocess.Popen(["findbuild", sys.argv[1]], stdout=subprocess.PIPE).communicate()[0]

match = re.search(r'^Location:\s+([^\s]*)', output, re.MULTILINE)
if match:
    buildpath = match.group(1)    
    if os.path.isfile(buildpath+"\\contents.xml"):
        processMeta(buildpath)
    elif os.path.isfile(buildpath+"\\android.plf"):
        processApps(buildpath)
    elif os.path.isfile(buildpath+"\\au_wconnect_riva.plf"):
        processWcnss(buildpath)
    

print ""
print output    