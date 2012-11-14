import socket
import thread
import SocketServer

def shutdown_server(server):
    server.shutdown()

class CmdHandler(SocketServer.StreamRequestHandler):
    
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.rfile.readline().strip()
        
        # self.request.sendall(self.data.upper())
        print self.data
        if self.data == "play":
            pass
        elif self.data == "stop":
            pass
        elif self.data == "pause":
            pass
        elif self.data == "toggle":
            pass
        elif self.data == "skip":
            pass
        elif self.data == "ban":
            pass
        elif self.data == "rate":    
            pass
        elif self.data == "unrate":
            pass
        elif self.data == "info":
            pass
        elif self.data == "setch":
            pass
        elif self.data == "end":
            try:
                thread.start_new_thread(shutdown_server, (self.server, ))
            except:
                print "Error: unable to start shutdown thread"
        else:
            print "invalid command"   

class TCPServerV4(SocketServer.TCPServer):
  address_family = socket.AF_INET
  allow_reuse_address = True

if __name__ == "__main__":

    HOST, PORT = "localhost", 8888

    # Create the server, binding to localhost on port 8888
    server = TCPServerV4((HOST, PORT), CmdHandler)
    
    print "Server listen at %s:%d" % (HOST, PORT)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
    
    print "Server shutdown"
        
    

