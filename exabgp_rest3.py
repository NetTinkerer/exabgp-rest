#!/usr/bin/env python
import web
from sys import stdout
from netaddr import *
from pprint import pprint
urls = (
    '/announce/(.*)', 'announce',
    '/withdraw/(.*)', 'withdraw',
)
class MyOutputStream(object):
    def write(self, data):
        pass   # Ignore output
	
web.httpserver.sys.stderr = MyOutputStream()
class bgpPrefix:
    def __init__(self,prefix,action="announce",next_hop="self",attributes={}):
        self.prefix=prefix
        self.action=action
        self.next_hop=next_hop
        self.attributes=attributes
        print self.attributes
    def get_exabgp_message(self):
        if (self.action=='withdraw'):
            exabgp_message="{0} route {1} next-hop {2}".format(self.action,self.prefix,self.next_hop)
        else:
            attribute_string=""
            for attribute in self.attributes:
                 if attribute == "local-preference":
                     attribute_string+=" local-preference {0}".format(self.attributes[attribute])
                 elif attribute == "med":
                     attribute_string+=" med {0}".format(self.attributes[attribute])
                 elif attribute == "community":
                     print self.attributes[attribute]
                     if len(self.attributes[attribute])>0:
			 attribute_string+=" community [ "
			 for comm in self.attributes[attribute]:
			     attribute_string+=" {0} ".format(comm)
			 attribute_string+=" ]"

                     
            exabgp_message="{0} route {1} next-hop {2}{3}".format(self.action,self.prefix,self.next_hop,attribute_string)
	return exabgp_message
     
def verifyIp(ip):
    if not '/' in ip:
        ip="{0}/32".format(ip)
    try:
        ip_object=IPNetwork(ip)
    except:
        raise web.badrequest("invalid IP")
    return(ip_object)

class announce:
    def GET(self, prefix):
        ip_object=verifyIp(prefix)
       # bgp_prefix=bgpPrefix(str(ip_object),action="announce",attributes={'local-preference': 300})
        bgp_prefix=bgpPrefix(str(ip_object),action="announce",attributes=web.input(community=[]))
        stdout.write( bgp_prefix.get_exabgp_message() + '\n')
        stdout.flush()
        return "OK"


class withdraw:
    def GET(self, prefix):
        ip_object=verifyIp(prefix)
        bgp_prefix=bgpPrefix(str(ip_object),action="withdraw")
        stdout.write( bgp_prefix.get_exabgp_message() + '\n')
        stdout.flush()
        return "OK"

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
