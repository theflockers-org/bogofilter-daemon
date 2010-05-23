#!/usr/bin/env python2.6
''' 
    Bogofilter Daemon is a daemon wrapper to bogofilter in STDIN mode.

    It opens max_procs instances of bogofilter in STDIN mode and escales 
    the inputs for each instance.

    Author: Leandro Mendes <leandro at gmail dot com>
    --------------------------------------------------------------------
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys, os, re, errno
import setproctitle, socket, threading
import SocketServer
from subprocess import *

max_procs  = 10
index      = 0
bogofilter = []

bogofilter_path = '/usr/bin/bogofilter'
bind_address    = 'localhost'
bind_port       = 4321

banner     = '+ Hello! Bogofilter Daemon is developed by Leandro Mendes (leandro at gmail dot com) and is a software\r\n\
  with no warranty and no support. Use it by you own. First, don\'t forget to train you bogofilter!\r\n\
  * COMMANDS: SCAN [filepath] and QUIT\r\n'

def start_procs():
    for num in range(max_procs):
        bogofilter.append(Popen([bogofilter_path,'-l','-t','-b'], stdin=PIPE, stdout=PIPE, bufsize=4096))

class ServerRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        self.send_data(banner)

        try:
            while True:
                self.data = self.request.recv(1024)

                if len(self.data.strip()) == 0:
                    self.send_data('ERR: unknown command')
                else:
                    self.parse_commands()
        except IOError, e:
            if e.errno == errno.EPIPE:
                return
    
    def do_SCAN(self):

        global index

        filepath = self.data.split(' ')[1].strip()
        if os.path.exists(filepath) == True:
            if index == max_procs:
                index = 0
     
            bogofilter[index].stdin.write(filepath + "\n")
            bogofilter[index].stdin.flush()
            output = bogofilter[index].stdout.readline()
            bogofilter[index].stdout.flush()
            self.send_data(output)
    
            index = index + 1
        else:
            self.send_data('%s: no such file' % (filepath))
    
    def do_QUIT(self):
        self.send_data('Bye!')
        self.request.close()

    def send_data(self, data):
        self.request.send(data + "\r\n")

    def parse_commands(self):
        cmd = []
        cmd = self.data.split(' ')
        if (len(cmd) < 2) and (len(self.data) < 4):
            cmd[0] = self.data.strip()
            self.send_data('ERR: unknown command')
            return

        methodStr = 'do_' + cmd[0].upper().strip()
        method = 'self.'+ methodStr + '()'

        if hasattr(self, methodStr):
            eval(method)
        else:
            self.send_data('ERR: unknown command')
        
class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer): 
    daemon_threads      = True
    allow_reuse_address = True

try:
    setproctitle.setproctitle('Bogofilter-Daemon (%i children)' % (max_procs))
    start_procs()
    server = Server((bind_address, bind_port), ServerRequestHandler)
    server.serve_forever()

except KeyboardInterrupt:
    sys.exit()
