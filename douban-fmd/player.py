# -*- coding: utf-8 -*-

import signal
import subprocess

from api import RadioAPI, ReportType

class PlayerStatus:
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

        self.status = PlayerStatus.STOP



    def __login(self):
        pass


    def __play(self):

        if self.current_song_index in range(len(self.play_list)):

            song_url = self.play_list[self.current_song_index]['url']

            self.mpg321_proc = subprocess.Popen(['mpg321', '-q', song_url.replace('\\', '')])

            #streamdata = self.mpg321_proc.communicate()[0]
            #rc = self.mpg321_proc.returncode
            #print rc

            #self.__opCurrentSong(ReportType.END)

            #self.current_song_index = self.current_song_index + 1

            #self.stop()
            #self.play()



    def play(self):
        print "play"

        if self.status == PlayerStatus.STOP:

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

            self.__play()



        elif self.status == PlayerStatus.PAUSE:
            self.mpg321_proc.send_signal(signal.SIGCONT)

        self.status = PlayerStatus.PLAY

    def stop(self):
        print "stop"

        if self.status != PlayerStatus.STOP:

            self.status = PlayerStatus.STOP

            self.mpg321_proc.send_signal(signal.SIGHUP)


    def pause(self):
        print "pause"

        self.status = PlayerStatus.PAUSE
        self.mpg321_proc.send_signal(signal.SIGSTOP)

    def toggle(self):
        print "toggle"

        if self.status == PlayerStatus.PLAY:
            self.pause()
        else:
            self.play()

    def skip(self):
        print "skip"

        self.__opCurrentSong(ReportType.SKIP)


        self.current_song_index = self.current_song_index + 1

        self.stop()
        self.play()



    def ban(self):
        print "ban"

        self.current_song_index = self.current_song_index + 1

        self.__opCurrentSong(ReportType.BAN)

        self.stop()
        self.play()


    def rate(self):
        print "rate"

        self.__opCurrentSong(ReportType.RATE)


    def unrate(self):
        print "unrate"

        self.__opCurrentSong(ReportType.UNRATE)



    def info(self):
        print "info"
        if self.current_song_index in range(len(self.play_list)):
            print self.play_list[current_song_index]

    def setch(self, ch):
        print "setch"

        self.channel = ch

        self.current_song_index = -1
        del self.play_list[:]

        if self.status != PlayerStatus.STOP:
            self.stop()

        self.play()

    def __maintarinPlayHistory(self, songId, op):

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
                self.__maintarinPlayHistory(songId, op)




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







