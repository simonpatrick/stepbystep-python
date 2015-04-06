__author__ = 'simon'

import os
import sys
from UserDict import UserDict

def stripulls(data):
    "strip whitespace and nulls"
    return data.replace("\00"," ").strip()

class FileInfo(UserDict):
    "store file metadata"
    def __init__(self,filename=None):
        UserDict.__init__(self)
        self["name"]=filename

class MP3FileInfo(FileInfo):
    "store MP3 tages ID3V1.0"
    tagDataMap = {"title"   : (  3,  33, stripulls),
                  "artist"  : ( 33,  63, stripulls),
                  "album"   : ( 63,  93, stripulls),
                  "year"    : ( 93,  97, stripulls),
                  "comment" : ( 97, 126, stripulls),
                  "genre"   : (127, 128, ord)}

    def __parse(self,filename):
        "parse ID3V1.0 tags from MP3 file"
        self.clear()
        try:
            fsock = open(filename,"rb",0)
            try:
                fsock.seek(-128,2)
                tagdata = fsock.read(128)
            finally:
                fsock.close()
            if(tagdata[:3]=='TAG'):
                for tag,(start,end,parseFunc) in self.tagDataMap.items():
                    self[tag]=parseFunc(tagdata[start:end])
        except IOError:
            pass

    def __setitem__(self, key, item):
        if key=="name" and item:
            self.__parse(item)
        FileInfo.__setitem__(self.key,item)

    def listDirectory(directory,fileExtList):
        "get list of file info objects from files and particular extensions"
        fileList=[os.path.normcase(f) for f in os.listdir(directory)]
        filelist=[os.path.join(directory,f) for f in fileExtList \
            if os.path.splitext(f)[1] in fileExtList]

        def getFileInfoClass(filename,module=sys.modules[FileInfo.__module__]):
            "get file info class form filename extension"
            subclass="%sFileInfo" % os.path.splitext(filename)[1].upper()[1:]
            return hasattr(module,subclass) and getattr(module,subclass) or FileInfo

        return [getFileInfoClass(f)(f) for f in fileList]

    if __name__ == '__main__':
        for info in listDirectory("~/tools/gitbook",[".md"]):
            print "\n".join(["%s=%s" % (k,v) for k,v in info.items()])
            print