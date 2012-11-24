"""
http://stackoverflow.com/questions/8994937/send-image-using-socket-programming-python
"""

#!/usr/bin/python
# TCP client example
import socket
import os

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("", 5000))
k = ' '
size = 1024

while(1):
    print "Do you want to transfer a \n1.Text File\n2.Image\n3.Video\n"
    k = raw_input()
    client_socket.send(k)
    k = int (k)
    if(k == 1):
        print "Enter file name\n"
        strng = raw_input()
        client_socket.send(strng)
        size = client_socket.recv(1024)
        size = int(size)
        print "The file size is - ",size," bytes"
        size = size*2
        strng = client_socket.recv(size)
        print "\nThe contents of that file - "
        print strng

    if (k==2):
        # print "Enter file name of the image with extentsion (example: filename.jpg,filename.png) - "
        # fname = raw_input()
        fname = 'sky.jpg'
        client_socket.send(fname)
        size = client_socket.recv(1)
        # print size
        # size = int(size)
        print "The file size is - ",size
        size = size*2
        strng = client_socket.recv(256456)
        print "\nThe file will be saved and opened- "
        fname = 'downloads/'+fname
        nf = open(fname,'w')
        nf.write(strng)
        nf.close()
        fname = 'viewnior '+ fname
        print fname
        os.system(fname)