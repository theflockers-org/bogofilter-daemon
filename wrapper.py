#!/usr/bin/env python2.6

import sys, os, re
import setproctitle, socket, threading
import SocketServer
from subprocess import *

max_procs  = 10
index      = 0
bogofilter = []

def start_procs():
    for num in range(max_procs):
        bogofilter.append(Popen(['/usr/bin/bogofilter','-l','-t','-b'], stdin=PIPE, stdout=PIPE, bufsize=4096))

class ServerRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        global index
  
        while True:
            data = self.request.recv(1024)
            filepath = data.strip()
            if len(filepath) == 0:
                self.request.send('ERR: give me a file to scan\r\n')
                continue

            if os.path.exists(filepath) == True:
                if index == max_procs:
                    index = 0
            
                bogofilter[index].stdin.write(filepath + "\n")
                bogofilter[index].stdin.flush()
                output = bogofilter[index].stdout.readline()
                bogofilter[index].stdout.flush()
                # print output
                self.request.send(output)
                # reg = re.match(r"([SUH]) ([\d\.]+)", output) 
                # result = reg.group(1)
                # score  = reg.group(2)
        
                index = index + 1

            else:
                self.request.send('%s: no such file\r\n' % (filepath))

        
class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer): 
    pass

try:
    setproctitle.setproctitle('PyBogofilter (%i children)' % (max_procs))
    start_procs()
    server = Server(('localhost', 6666), ServerRequestHandler)
    server.allow_reuse_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

except KeyboardInterrupt:
    print 'bye'
    sys.exit()
