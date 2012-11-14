# -*- coding: utf-8 -*-

import pycurl
import cStringIO


APP_NAME        = "radio_desktop_win"
VERSION         = 100
LOGIN_API_URL   = "http://www.douban.com/j/app/login"
CHANNEL_API_URL = "http://www.douban.com/j/app/radio/channels"
RADIO_API_URL   = "http://www.douban.com/j/app/radio/people"

class ReportType:
    
    BAN     = 'b'   # 不再播放当前歌曲  [短报告]                          
    END     = 'e'   # 当前歌曲播放完毕，播放列表非空  [短报告]             
    NEW     = 'n'   # 当前不在播放，播放列表为空 [长报告]
    PLAY    = 'p'   # 正在播放，播放列表为空，需要新的播放列表  [长报告]
    SKIP    = 's'   # 跳过当前播放的歌曲，播放列表非空  [短报告] 
    RATE    = 'r'   # 为当前播放歌曲加红心    [短报告] 
    UNRATE  = 'u'   # 取消当前歌曲的红心     [短报告] 

class RadioAPI:

    def __init__(self, uid, uname, token, expire):
    
        self.uid = uid
        self.uname = uname
        self.token = token
        self.expire = expire
        
        self.curl = pycurl.Curl()
        self.curl.setopt(self.curl.CONNECTTIMEOUT, 5)
        self.curl.setopt(self.curl.TIMEOUT, 5)
        #self.curl.setopt(self.curl.VERBOSE, True)
        
        
    def sendLongReport(self, channel, songId, reportType, playHistory):
    
        buf = cStringIO.StringIO()
        
        url = "%s?app_name=%s&version=%s&user_id=%d&expire=%d&token=%s&channel=%d&sid=%d&type=%c&h=%s" % (
            RADIO_API_URL,
            APP_NAME,
            VERSION,
            self.uid,
            self.expire,
            self.token,
            channel,
            songId,
            reportType,
            playHistory,    
        )
        
        self.curl.setopt(self.curl.URL, url)
        self.curl.setopt(self.curl.WRITEFUNCTION, buf.write)
        self.curl.perform()
        
        print buf.getvalue()
        
        
        buf.close()
        
        
    def sendShortReport(self, channel, songId, reportType):
        
        url = "%s?app_name=%s&version=%s&user_id=%d&expire=%d&token=%s&channel=%d&sid=%d&type=%c" % (
            RADIO_API_URL,
            APP_NAME,
            VERSION,
            self.uid,
            self.expire,
            self.token,
            channel,
            songId,
            reportType,    
        )
        
        self.curl.setopt(self.curl.URL, url)
        self.curl.perform()
            
   
if __name__ == "__main__":

    import ConfigParser, os
    
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.expanduser("~/.fmd/fmd.conf")))
    
    #print "uid =", config.get("DoubanFM", "uid")
        
    api = RadioAPI(
        long(config.get("DoubanFM", "uid")),
        config.get("DoubanFM", "uname"),
        config.get("DoubanFM", "token"),
        long(config.get("DoubanFM", "expire"))
    )  
    
    api.sendShortReport(1, 1433383, ReportType.RATE)   
        
        
