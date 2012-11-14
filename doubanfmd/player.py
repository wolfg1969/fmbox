from api import RadioAPI

class PlayerStatus:
    PLAY = 1
    PAUSE = 2
    STOP = 3

class Player:

    def __init__(self, uid, uname, token, expire):
        
        self.channel = 0
        
        self.radioAPI = RadioAPI(uid, uname, token, expire)
        
        self.play_list = []
        self.play_history_list = []
        
        self.status = PlayerStatus.STOP
        
        
        
    def __login(self):
        pass       
      
    def play(self):
        print "play"
        
        if self.status == PlayerStatus.STOP:        
            
            if not self.play_list:
                #self.play_list = self.radioAPI.getNewPlayList(
                #    self.channel, self.play_history_list)
                
                
            
        elif self.status == PlayerStatus.PAUSE:
            pass
            
        self.status = PlayerStatus.PLAY
        
    def stop(self):
        print "stop"
        
        if self.status != PlayerStatus.STOP:
            self.status = PlayerStatus.STOP    
        
    def pause(self):
        print "pause"
        
    def toggle(self):
        print "toggle"
        
    def skip(self):
        print "skip"
        
    def ban(self):
        print "ban"
        
    def rate(self):
        print "rate"
        
    def unrate(self):
        print "unrate"
        
    def info(self):
        print "info"
        
    def setch(self):
        print "setch"
        
        
if __name__ == "__main__":

    import ConfigParser, os
    
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.expanduser("~/.fmd/fmd.conf")))
    
    #print "uid =", config.get("DoubanFM", "uid")
        
    player = Player(
        config.get("DoubanFM", "uid"),
        config.get("DoubanFM", "uname"),
        config.get("DoubanFM", "token"),
        config.get("DoubanFM", "expire")
    )
    

        
        
    
    

