# -*- coding: utf-8 -*-

import socket
import sys
import thread
import SocketServer

from daemon import Daemon

from player import Player

def shutdown_server(server):
    player.stop()
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
            player.play()
        elif cmd == "stop":
            player.stop()
        elif cmd == "pause":
            player.pause()
        elif cmd == "toggle":
            player.toggle()
        elif cmd == "skip":
            player.skip()
        elif cmd == "ban":
            player.ban()
        elif cmd == "rate":
            player.rate()
        elif cmd == "unrate":
            player.unrate()
        elif cmd == "info":   
            self.request.sendall(player.info().encode('utf-8'))
        elif cmd == "setch":
            if arg:
                player.setch(int(arg))
        elif cmd == "end":
            try:
                thread.start_new_thread(shutdown_server, (self.server, ))
            except:
                print "Error: unable to start shutdown thread"
        else:
            print "invalid command"

class TCPServerV4(SocketServer.TCPServer):
    address_family = socket.AF_INET
    allow_reuse_address = True


class ServerDaemon(Daemon):

    def run(self):

        HOST, PORT = "localhost", 8888

        # Create the server, binding to localhost on port 8888
        server = TCPServerV4((HOST, PORT), CmdHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()


if __name__ == "__main__":
    '''
    daemon = ServerDaemon('/tmp/doubanfmd.pid')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
    '''

    import ConfigParser, os

    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.expanduser("~/.fmd/fmd.conf")))

    player = Player(
        long(config.get("DoubanFM", "uid")),
        config.get("DoubanFM", "uname"),
        config.get("DoubanFM", "token"),
        long(config.get("DoubanFM", "expire"))
    )

    HOST, PORT = "localhost", 8888

    # Create the server, binding to localhost on port 8888
    server = TCPServerV4((HOST, PORT), CmdHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()





