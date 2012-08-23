import xmlrpclib
import datetime

def LJPost(postplace, message_obj):
    server = xmlrpclib.ServerProxy("http://www.livejournal.com/interface/xmlrpc")
    now = datetime.datetime.now()
    message = message_obj['title']
    if message_obj['attachements']:
        for attach in message_obj['attachements']:
            if attach['type'] == "url":
                message += "<a href='%s'>%s</a><br>" % (attach['src'] , attach['src'])
            if attach['type'] == "img":
                message += "<img src='%s'><br>" % (attach['src'])
    else:
        message = message_obj['text']

    args = {"username" : postplace.login,
            "hpassword" : postplace.password,
            "event" : message,
            "subject" : message_obj['title'],
            "year" : now.year,
            "mon" : now.month,
            "day" : now.day,
            "hour": now.hour,
            "min" : now.minute
    }
    
    response = server.LJ.XMLRPC.postevent(args)
    return True