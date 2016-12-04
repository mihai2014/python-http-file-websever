#!/usr/bin/python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi, urlparse
import os
import urllib2

from browse import template

HOST = ''
PORT = 8000
LOCAL = os.getcwd()
CHUNK_SIZE = 128

#replace "#local#" tags with local directory in index.html and page.html
def index(): 
    global LOCAL
    
    #if(os.name == "nt"):
    LOCAL = LOCAL.replace("C:","")
    LOCAL = LOCAL.replace("\\","/")
 
    f = open(LOCAL + sep + "index_base.html","rb")
    indexFile = f.read()
    indexFile = indexFile.replace("#local#",LOCAL + "/")
    f.close()
        
    f = open(LOCAL + sep +"index.html","wb")  
    f.write(indexFile)
    f.close()

    f = open(LOCAL + sep +"page_base.html","rb")
    pageFile = f.read()
    pageFile = pageFile.replace("#local#",LOCAL + "/")
    f.close()
    
    f = open(LOCAL + sep + "page.html","wb")
    f.write(pageFile)
    f.close()



def sendData(self):

    totalsent = 0
    size = str(os.stat(self.path).st_size)
    f = open(self.path,"rb")

    while totalsent < size:
        chunk = f.read(CHUNK_SIZE)
        self.wfile.write(chunk)
        sent = len(chunk)
        #print "sent", sent
        totalsent = totalsent + sent
        if(sent == 0): break

    f.close()





def mimeType(path):
    if path.endswith(".html"):
        mimetype='text/html'
    elif path.endswith(".js"):
        mimetype='application/javascript'
    elif path.endswith(".css"):
        mimetype='text/css'

    elif path.endswith(".jpg"):
        mimetype='image/jpg'
    elif path.endswith(".gif"):
        mimetype='image/gif'
    elif path.endswith(".ico"):
        mimetype='image/x-icon'
    elif path.endswith(".png"):
        mimetype='imge/png'

#    force download action in browser

    elif path.endswith(".pdf"):
        mimetype='application/pdf'
    elif path.endswith(".txt"):
        mimetype='text/plain'
    elif path.endswith(".doc"):
        mimetype='application/msword'

    else:
        mimetype = 'application/octet-stream'

    return mimetype

class myHandler(BaseHTTPRequestHandler):
	
    #Handler for the GET requests
    def do_GET(self):
        #print self.headers
	#print self.path
	back = LOCAL.count("/")
	rootDir = "../" * back

	#Example params: /list?path=/home/pi&flag=0
	#Example params: /?path=/home/pi&flag=0

	args = {}

        #===========getting args
        if self.path.startswith("/?"):
            params = self.path[2:len(self.path)]
            items = params.split("&")
            for item in items:
                values = item.split("=")
                args[values[0]] =  urllib2.unquote(values[1])

	    #args mode => select/list folder content

            path = args["path"]
            page = template("page.html",path,rootDir)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.send_header('Content-length',str(len(page)))
            self.end_headers()
            self.wfile.write(page)
            return

	else:

	    #file path mode  => download selected file

	    if (self.path == "/"):
                self.path = LOCAL + "/index.html"

            self.path = urllib2.unquote(self.path)

            try:
                self.send_response(200)
                self.send_header('Content-type',mimeType(self.path))
                self.send_header('Content-length',str(os.stat(self.path).st_size))
                self.end_headers()
                sendData(self)
                return
		
            #except Exception as e:
            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)


        def do_POST(self):
		form_action = self.path

	        ctype, boundary = cgi.parse_header(self.headers.getheader('content-type'))

	        if ctype == 'multipart/form-data':
	            postvars = cgi.parse_multipart(self.rfile, boundary)
	        elif ctype == 'application/x-www-form-urlencoded':
	            length = int(self.headers.getheader('content-length'))
		    postvars = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1)
	        else:
	            postvars = {}

	        #print(postvars.get("lastName", "didn't find it"))
		#print "file is :", postvars['file']

                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                # Send the html message
                self.wfile.write("This is post!! <br> You sent: " + str(postvars))
                return


try:
        #init index.html
        index()

	server = HTTPServer((HOST, PORT), myHandler)
	print 'Started httpserver on port ' , PORT

	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
