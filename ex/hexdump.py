#!/usr/bin/python
import sys

if sys.version[0]>="3": raw_input = input

filename = raw_input("full path and file name, then press ENTER:- ")
binary = open(filename, "rb+")
length = len(binary.read())
array = ""

for position in range(0, length, 1):
    binary.seek(position)
    char = hex(ord(binary.read(1)))[2:]
    if len(char) <= 1: char = "0" + char
    array = array + char + " "

binary.close()

print("%s" %(array))

filename = filename+ ".hex"
hexadecimal = open(filename, "w")
hexadecimal.write(array)
hexadecimal.close()

