import urllib2
import urllib
import socket

localIP = socket.gethostbyname(socket.gethostname())
print "local ip: %s " % localIP

# ipList = socket.gethostbyname_ex(socket.gethostname())
# for i in ipList:
#     if i != localIP:
#        print "external IP:%s" % i

data = {'ipv4': localIP}
f = urllib2.urlopen(
        # url='http://localhost:5000/admin/monitor/',
        url='http://demo-joylin.rhcloud.com/admin/monitor/',
        data=urllib.urlencode(data)
        )
print f.read()
