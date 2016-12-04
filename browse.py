import sys
import os
import time

lastPage = ""

def getDir(reqPath):
    #directory and files listing 
    data = []
    
#    if(os.name == "nt"):
#	reqPath = reqPath.replace("/","\\")    
    
    for (path, dirs, files) in os.walk(reqPath):
        localDirs = sorted(dirs)
        localFiles = sorted(files)
        break

    for name in localDirs:
        dirPath = os.path.join(reqPath, name)
	dirPath = dirPath.replace("\\","/")
	dirPath = dirPath.replace("c:","")
	data.append(("D",name,'','',dirPath))
        #print "D %s [%s]" % (name, dirPath)

    for name in localFiles:
        filePath = os.path.join(reqPath, name)
	filePath = filePath.replace("\\","/")
	filePath = filePath.replace("c:","")
        statinfo = os.stat(filePath)
        modifTime = time.localtime(statinfo.st_mtime)    
	#data.append(("F",name, str(statinfo.st_size), time.strftime("%a, %d %b %Y %H:%M:%S  %Z", modifTime), filePath))
	#data.append(("F",name, str(statinfo.st_size) + " bytes", time.strftime("%a, %d %b %Y %H:%M:%S", modifTime), filePath))
	data.append(("F",name, str(statinfo.st_size) + " bytes", time.strftime("%a, %d %b %Y %H:%M:%S", modifTime), filePath))
	#print "F %s [%s]" % (name, filePath)
	
#    for item in data:
#	print item

    return data

#generate display zone = rows with folders and files
def replaceTags(string, replaceData):
    LOCAL = os.getcwd()
    LOCAL = LOCAL.replace("C:","")
    LOCAL = LOCAL.replace("\\","/")    

    fileOrDir = replaceData[0]
    name = replaceData[1]
    size = replaceData[2]
    date = replaceData[3]
    path = replaceData[4]
    #print fileOrDir, name, size, date, path

    if(fileOrDir == "D"):
	ico = LOCAL + "/folder.png"
	string = string.replace("#download#", "" )
	string = string.replace("#link#", "?path=" + path)
    if(fileOrDir == "F"):
        ico = LOCAL + "/file.png"
	string = string.replace("#download#", "download=" + '"' + name + '"')
	string = string.replace("#link#", path)

    string = string.replace("#ico#", ico)
    string = string.replace("#name#", name)
    string = string.replace("#size#", size)
    string = string.replace("#date#", date)
    #string = string.replace("#link#", path)

    return string


def template(fileName, path, rootDir):
  
    newPage = ""

    file = open(fileName,"r")
    strFile = file.read()
    #print strFile
    file.close()    

    begin = strFile.find("<!--begin_display-->")
    end = strFile.find("<!--end_display-->")
    firstPart = strFile[0:begin-1]
    displayZone = strFile[begin:end+len("<!--end_display-->")]
    secondPart = strFile[end+len("<!--end_display-->"):len(strFile)]

    #I)
    newPage = firstPart

    if(path == ""):
	if(os.name == "nt"):
	    path = "c:\\"
	elif(os.name == "posix"):
	    path = os.sep
	else:
	    path = os.sep	

    data = getDir(path)

    #II)
    for item in data:
	line = replaceTags(displayZone, item)
	newPage = newPage + line

    #III)
    newPage = newPage + secondPart

    return newPage


#print template("page.html","/home/pi")
#print template("page.html","")
#getDir("/home/pi")


#directories selected (cd); for back option
#history = []

#print os.name
#print os.listdir(os.getcwd())
#print os.sep
#print os.getcwd()

#i = 0
#for (path, dirs, files) in os.walk("."):
#    print "Directory: ", path
#    #print dirs.sort()
#    print sorted(files)
#    print "----"
#    i += 1
#    if i >= 4:
#        break
