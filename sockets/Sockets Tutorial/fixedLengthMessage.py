import socket

class mysocket:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''
    msgLen = 0

    def __init__(self, sock=None, msgLen = 0):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        self.msgLen = msgLen

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < self.msgLen:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        msg = ''
        while len(msg) < self.msgLen:
            chunk = self.sock.recv(self.msgLen-len(msg))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            msg = msg + chunk
        return msg