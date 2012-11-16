# -*- coding: utf-8 -*-

import logging
import signal
import socket
import sys
import thread
import threading
import time
import SocketServer

from daemon import Daemon
from player import Player

logging.basicConfig(filename="/tmp/douban-fmd.log", level=logging.DEBUG)

server_logger = logging.getLogger('douban-fmd.server')

def shutdown_server_by_cmd(server):

    server_logger.info("server shutdown")
    
    server.running = False    
    server.player.stop()
    server.shutdown()
    

class CmdHandler(SocketServer.StreamRequestHandler):

    def __current_playing_info(self):
        self.request.sendall(self.server.player.info().encode('utf-8'))

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.rfile.readline().strip()

        server_logger.debug("cmd=%s" % self.data)

        if not self.data:
            return

        cmd = self.data.split()
        arg = None

        if len(cmd) == 2:
            arg = cmd[1]

        cmd = cmd[0]

        if cmd == "play":
            self.server.player.play()
            self.__current_playing_info()
        elif cmd == "stop":
            self.server.player.stop()
        elif cmd == "pause":
            self.server.player.pause()
        elif cmd == "toggle":
            self.server.player.toggle()
        elif cmd == "skip":
            self.server.player.skip()
            self.__current_playing_info()
        elif cmd == "ban":
            self.server.player.ban()
            self.__current_playing_info()
        elif cmd == "rate":
            self.server.player.rate()
            self.__current_playing_info()
        elif cmd == "unrate":
            self.server.player.unrate()
            self.__current_playing_info()
        elif cmd == "info":   
            self.__current_playing_info()
        elif cmd == "setch":
            if arg:
                self.server.player.setch(int(arg))
                self.__current_playing_info()
            else:
                self.request.sendall("invalid channel id")    
        elif cmd == "end":
            try:
                thread.start_new_thread(shutdown_server, (self.server, ))
            except:
                log.exception("Error: unable to start shutdown thread")
        else:
            server_logger.info("invalid command")
            

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
    
    daemon = ServerDaemon("/tmp/douban-fmd.pid")

    daemon.start()   
    
    
    #init_player_server()
    
    





