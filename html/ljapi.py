import xmlrpclib
import datetime

def LJPost(postplace, message_obj):
    server = xmlrpclib.ServerProxy("http://www.livejournal.com/interface/xmlrpc")
    now = datetime.datetime.now()
    message = message_obj['text']
    if message_obj['attachements']:
        for attach in message_obj['attachements']:
            message = "%s <br> %s " % (message, attach['src'])
    args = {"username" : postplace.login,
            "hpassword" : postplace.password,
            "event" : message,
            "subject" : "",
            "year" : now.year,
            "mon" : now.month,
            "day" : now.day,
            "hour": now.hour,
            "min" : now.minute
    }
    
    response = server.LJ.XMLRPC.postevent(args)
    return True