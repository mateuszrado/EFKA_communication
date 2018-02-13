import socket
import threading
import queue
import os
import signal
import time

TCP_IP = ('127.0.0.1')
TCP_PORT = 3010
BUFFER_SIZE = 32

no = 0

class ClientThread(threading.Thread):

    def __init__(self, ip, port, sock):
        threading.Thread.__init__(self)
        global no
        no = no + 1
        self.ip = ip
        self.port = port
        self.sock = sock
        self.number = no
        print("New thread no. " + str(no) + " started for " + ip + " : " + str(port))

    def run(self):
        filename = str(no) + "_data.txt"
        file = open(filename, "w+")
        while True:
            l = file.read(BUFFER_SIZE)
            while l:
                self.sock.send(l)
                l = file.read(BUFFER_SIZE)
            if not l:
                file.close()
                self.sock.close()
                break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((TCP_IP, TCP_PORT))
    threads = []
    print("TCP Server:\n\n")

    while True:
        server.listen(5)
        print ("Waiting for incoming connections...")
        (connection, (ip, port)) = server.accept()
        print ("Got connection from ", (ip,port))
        newthread = ClientThread(ip, port, connection)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()

#s = socket(AF_INET, SOCK_STREAM)    #create socket s
#s.bind(('', TCP_PORT))
#s.listen(5)     #socket backlog (max 5)

#while char != q:
#    client, addr = s.accept()
#    print ("Connection with ", addr)
#    data = client.recv(BUFFER_SIZE)
#    print ("received data: ", data)
#    client.send("ODEBRANO\n".encode())
#    client.close()
