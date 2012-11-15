# -*- coding: utf-8 -*-

import multiprocessing
import signal
import subprocess

from api import RadioAPI, ReportType


class PlayerStatus:
    INIT = 0
    PLAY = 1
    PAUSE = 2
    STOP = 3

class Player:

    def __init__(self, uid, uname, token, expire):

        self.channel = 0

        self.radioAPI = RadioAPI(uid, uname, token, expire)

        self.play_list = []
        self.play_history = []
        self.current_song_index = -1

        self.mpg321_proc = None
        self.play_proc = None

        self.status = PlayerStatus.INIT
        
        #proc = multiprocessing.Process(target=self.__checkSongIsEnd, args=())
        #proc.start()


    def __login(self):
        pass
        
        
    def __mpg321_proc(self, song_url, output):
    
        mpg321_proc = subprocess.Popen(['mpg123', '-q', song_url.replace('\\', '')])
        
        output.put(mpg321_proc)
        
        print "mpg321 pid is", mpg321_proc.pid
        print "will block here"
        
        mpg321_proc.wait() 
        
        print "mpg321 stopped" 
        
<<<<<<< HEAD
        if mpg321_proc.returncode >= 0: # not kill
=======
        if mpg321_proc.returncode >= 0:
>>>>>>> parent of d58fabc... play proc
            self.__get_next_song()
            self.__play() 
        
          
    
    def __playInAnotherProc(self, song_url):        
        
        print "play %s in another proc" % song_url
        
        queue = multiprocessing.Queue()
        
        play_proc = multiprocessing.Process(target=self.__mpg321_proc, args=(song_url, queue))
        play_proc.start()
        
        mpg321_proc = queue.get()
        
        queue.close()
        
        play_proc.terminate()
        
        return mpg321_proc, None
        
        

    def __play(self):
    
        if self.play_proc:
            print "current play_proc pid is", self.play_proc.pid
            self.play_proc.terminate()
            print "current play_proc pid terminated"
        else:
            print "self.play_proc is None"
            
        
        #self.__killPlayProc()
        
        if self.current_song_index in range(len(self.play_list)):

            song_url = self.play_list[self.current_song_index]['url']
            
            self.mpg321_proc, self.play_proc = self.__playInAnotherProc(song_url)
            
            print "new mpg321_proc.pid =", self.mpg321_proc.pid
            print "new play_proc is", self.play_proc
            
            
    def __stop(self):
        
        print "current mpg321 pid is", self.mpg321_proc.pid
        self.mpg321_proc.send_signal(signal.SIGKILL)
                    
        print "stop at index:", self.current_song_index        
        
        
        
    def __pause(self):
    
        print "current mpg321 pid is", self.mpg321_proc.pid
        self.mpg321_proc.send_signal(signal.SIGSTOP)        
            
    
    def __get_next_song(self):
    
        if self.current_song_index == -1:

            self.play_list = self.radioAPI.sendLongReport(
                self.channel,
                0,
                ReportType.NEW,
                self.play_history
            )
            self.current_song_index = 0

        elif self.current_song_index >= len(self.play_list):

            self.play_list = self.radioAPI.sendLongReport(
                self.channel,
                self.play_list[-2:-1][0]['sid'],
                ReportType.PLAY,
                self.play_history
            )
            self.current_song_index = 0
        else:
            self.current_song_index = self.current_song_index + 1       
        

    def play(self):
        print "play"

        if self.status == PlayerStatus.INIT:
        
            self.__get_next_song()
            self.__play()
            
        elif self.status == PlayerStatus.STOP:        
            
            self.__play()

        elif self.status == PlayerStatus.PAUSE:
            self.mpg321_proc.send_signal(signal.SIGCONT)

        self.status = PlayerStatus.PLAY

    def stop(self):
        print "stop"

        if self.status != PlayerStatus.STOP:            

            self.__stop()
            self.status = PlayerStatus.STOP


    def pause(self):
        print "pause"
        self.__pause()
        self.status = PlayerStatus.PAUSE
        

    def toggle(self):
        print "toggle"

        if self.status == PlayerStatus.PLAY:
            self.pause()
        else:
            self.play()
            

    def skip(self):
        print "skip"

        self.__opCurrentSong(ReportType.SKIP)

        self.__stop()
        self.__get_next_song()
        self.__play()



    def ban(self):
        print "ban"

        self.__opCurrentSong(ReportType.BAN)

        self.__stop()
        self.__get_next_song()
        self.__play()


    def rate(self):
        print "rate"

        self.__opCurrentSong(ReportType.RATE)


    def unrate(self):
        print "unrate"

        self.__opCurrentSong(ReportType.UNRATE)



    def info(self):
        print "info"
        if self.current_song_index in range(len(self.play_list)):
                        
            song = self.play_list[self.current_song_index]
                        
            return u"Album: %s\nTitle: %s\nArtist: %s\nLike:%s\n" % (
                song['albumtitle'],
                song['title'],
                song['artist'],
                song['like'],
            )
        
        return ""    

    def setch(self, ch):
        print "setch"

        self.channel = ch

        self.current_song_index = -1
        del self.play_list[:]

        if self.status != PlayerStatus.STOP:
            self.stop()

        self.play()
        

    def __maintainPlayHistory(self, songId, op):

        self.play_history.append({
                'sid': songId,
                'type': op
            })

        if len(self.play_history) > 20:
            del self.play_history[0]
            

    def __opCurrentSong(self, op):

        if self.current_song_index in range(len(self.play_list)):

            songId = self.play_list[self.current_song_index]['sid']

            self.radioAPI.sendShortReport(
                    self.channel,
                    songId,
                    op
                )

            if op in [ReportType.END, ReportType.SKIP, ReportType.BAN]:
                self.__maintainPlayHistory(songId, op)
                
            if op in [ReportType.RATE, ReportType.UNRATE]:
                if op == ReportType.RATE:
                    
                    self.play_list[self.current_song_index]['like'] = '1'
                    
                else:
                
                    self.play_list[self.current_song_index]['like'] = '0' 



if __name__ == "__main__":

    import ConfigParser, os

    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.expanduser("~/.fmd/fmd.conf")))

    #print "uid =", config.get("DoubanFM", "uid")

    player = Player(
        long(config.get("DoubanFM", "uid")),
        config.get("DoubanFM", "uname"),
        config.get("DoubanFM", "token"),
        long(config.get("DoubanFM", "expire"))
    )

    player.play()







