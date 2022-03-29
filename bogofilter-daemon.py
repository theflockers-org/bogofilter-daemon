#!/usr/bin/python27
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
import pwd, shutil, random
import socket, threading
import SocketServer
import ConfigParser
from subprocess import *



# get configs

config = ConfigParser.ConfigParser()
try:
    config.readfp(open('/etc/bogofilter-daemon.conf'))
except Exception, e:
    print str(e)
    sys.exit()

config.get('daemon','bogofilter_path')

max_procs  = int(config.get('daemon', 'max_procs'))
index      = int(config.get('daemon', 'index'))
run_user   = config.get('daemon', 'run_user')
tmpdir     = config.get('daemon', 'tmpdir')
bogofilter_path = config.get('daemon', 'bogofilter_path')
bind_address    = config.get('daemon', 'bind_address')
bind_port       = int(config.get('daemon', 'bind_port'))


bogofilter = []
locker     = []

banner     = '+ Hello! Bogofilter Daemon is developed by Leandro Mendes (leandro at gmail dot com) and is a software\r\n\
  with no warranty and no support. Use it by you own. First, don\'t forget to train you bogofilter!\r\n\
  * COMMANDS: SCAN [filepath] and QUIT\r\n'

def start_procs():
    user_info = pwd.getpwnam(run_user)
    homedir = user_info[5]
    for num in range(max_procs):
        wordlist_dir = '%s/bogofilter/%s/' % (tmpdir, num)
        if os.path.exists(wordlist_dir) != True:
            os.makedirs(wordlist_dir)

        shutil.copy( '%s/.bogofilter/wordlist.db' % (homedir), wordlist_dir )
        bogofilter.append(Popen([bogofilter_path,'-l','-t','-b','-d', wordlist_dir], stdin=PIPE, stdout=PIPE, bufsize=4096))

class NonRootException(Exception): pass

class ServerRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        # self.send_data(banner)

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

        global locker

        filepath = self.data.split(' ')[1].strip()
        if os.path.exists(filepath) == True:
            random.seed()
            # print 'Selecting process'
            index = random.randint(0, max_procs-1)
            while index in locker:
                # print 'Is locked:' + str(index)
                index = random.randint(0, max_procs-1)

            # print 'Locking: '+ str(index)
            locker.append(index)

            bogofilter[index].stdin.write(filepath + "\n")
            bogofilter[index].stdin.flush()
            output = bogofilter[index].stdout.readline()
            bogofilter[index].stdout.flush()
            self.send_data(output)

            #print 'Removing: ' + str(index)
            if index in locker:
                locker.remove(index)
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
#class Server(SocketServer.ForkingMixIn, SocketServer.TCPServer): 
    daemon_threads      = True
    allow_reuse_address = True

def run_as_user(user):
    if os.getuid() != 0:
        raise NonRootException('this program must to be started as root')

    user_info = pwd.getpwnam(user)
    uid = user_info[2]
    os.putenv('HOME', user_info[5])
    os.setuid(uid)

try:

    run_as_user(run_user)

    # setproctitle.setproctitle('Bogofilter-Daemon (%i children)' % (max_procs))
    start_procs()
    server = Server((bind_address, bind_port), ServerRequestHandler)
    server.serve_forever()
except IOError, e:
    print str(e)
    sys.exit(1)
except NonRootException, e:
    print e
except KeyError, e:
    print e
except KeyboardInterrupt:
    sys.exit()

