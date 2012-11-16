# -*- coding: utf-8 -*-

import signal
import socket
import sys
import thread
import threading
import time
import SocketServer

from daemon import Daemon

from player import Player

def shutdown_server_by_cmd(server):
    server.running = False    
    server.player.stop()
    server.shutdown()
    

class CmdHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.rfile.readline().strip()

        print "cmd =", self.data

        if not self.data:
            return

        cmd = self.data.split()
        arg = None

        if len(cmd) == 2:
            arg = cmd[1]

        cmd = cmd[0]


        if cmd == "play":
            self.server.player.play()
        elif cmd == "stop":
            self.server.player.stop()
        elif cmd == "pause":
            self.server.player.pause()
        elif cmd == "toggle":
            self.server.player.toggle()
        elif cmd == "skip":
            self.server.player.skip()
        elif cmd == "ban":
            self.server.player.ban()
        elif cmd == "rate":
            self.server.player.rate()
        elif cmd == "unrate":
            self.server.player.unrate()
        elif cmd == "info":   
            self.request.sendall(self.server.player.info().encode('utf-8'))
        elif cmd == "setch":
            if arg:
                self.server.player.setch(int(arg))
        elif cmd == "end":
            try:
                thread.start_new_thread(shutdown_server, (self.server, ))
            except:
                print "Error: unable to start shutdown thread"
        else:
            print "invalid command"

class PlayerSocketServer(SocketServer.TCPServer):
    address_family = socket.AF_INET
    allow_reuse_address = True
    

def init_player_server():

    import ConfigParser, os

    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.expanduser("~/.fmd/fmd.conf")))

    player = Player(
        long(config.get("DoubanFM", "uid")),
        config.get("DoubanFM", "uname"),
        config.get("DoubanFM", "token"),
        long(config.get("DoubanFM", "expire"))
    )
    
    signal.signal(signal.SIGUSR1, player.playNextSong)

    HOST, PORT = "localhost", 8888

    # Create the server, binding to localhost on port 8888
    server = PlayerSocketServer((HOST, PORT), CmdHandler)
    server.player = player

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    #server.serve_forever()  
    
    server.running = True
    
    server_thread = threading.Thread(target=server.serve_forever) 
    server_thread.start()
    
    while server.running:
        time.sleep(1)

    server_thread.join()
    
    

class ServerDaemon(Daemon):

    def run(self):    
        init_player_server()



if __name__ == "__main__":
    '''
    daemon = ServerDaemon()

    daemon.start()
    ''' 
    
    init_player_server()
    
    





