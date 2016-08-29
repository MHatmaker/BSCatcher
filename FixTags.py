
import eyed3
import eyed3.id3
import pdb
import os
import argparse
import datetime
eyed3.log.setLevel("ERROR")

uPodCast = unicode('Podcast', "UTF-8")
podpathRoot = r'/home/htmkr/BloombergPodcasts'

feeds = [
    {
        'subdir' :'surveillance',
        'prefix' : u'BS'
    },
    {
        'subdir' :'takingstock',
        'prefix' : u'TS'
    }
]

def stringType(s):
    strtype = None
    if isinstance(s, unicode):
        strtype = 'u'
        # print("{0} is unicode".format(s))
    elif isinstance(s, str):
        strtype = 'a'
        # print("{0} is ascii".format(s))
    else:
        pass
        # print("{0} is not a string".format(s))
    return strtype

class TagFixer(object):
    def __init__(self, ppath, fd):
        self.feed = fd
        self.podpath = os.path.join(podpathRoot, fd['subdir'], ppath)
        self.dateToday = unicode(ppath, "UTF-8")
        print(self.podpath)

        for filename in os.listdir(self.podpath):
            fn = self.checkFileName(filename)
            f = eyed3.load(os.path.join(self.podpath, fn))

            # if fn == 'tech_20150716_pod_64.mp3':
            #     pdb.set_trace()
            genreName = None
            self.checkTagExists(f, fn)
            print("<<<<<<<file {0} version {1}".format(fn, f.tag.version))

            self.checkTagNone(f, fn)

            print("f.tag is other than None")
            if hasattr(f.tag, 'genre') == False:
                self.addGenre(f)
            genreName = uPodCast
            try:
                # pdb.set_trace()
                try:
                    album = f.tag.album
                except:
                    album = 'album exception'
                album = self.updateTag(album, self.dateToday, "album")
                try:
                    artist = f.tag.artist
                except:
                    artist = 'artist exception'
                artist = self.updateTag(artist, unicode('nobody', "UTF-8"), 'artist')

                genreName = self.updateTag(genreName, uPodCast, 'genre')
                if genreName.isdigit():
                    genreName = uPodCast

                if genreName == u'Audio':
                    print('genreName is Audio, set it to Podcast')
                    genreName = uPodCast
                try:
                    gname = f.tag.genre.name
                except:
                    print('still no genre tag : generate genre')
                    self.addGenre(f)

                self.addDT2Name(f, fn, fd.prefix)
                f.tag.album, f.tag.artist, f.tag.genre.name = album, artist, genreName
                print(">>>>>>>artist : {0}, album : {1}, genreName : {2}".format(f.tag.album, f.tag.artist, f.tag.genre.name))

                # print("save us")
                f.tag.save(os.path.join(self.podpath, fn), encoding='utf-8', version=eyed3.id3.ID3_V2_3)

                print("saved {0}".format(fn))
                f = None
            except:
                print('whoops')

    def checkFileName(self, fn):
        fbase, fext = os.path.splitext(fn)
        if len(fext) == 0:
            fnRenamed = fn + '.mp3'
            os.rename(os.path.join(self.podpath, fn), os.path.join(self.podpath, fnRenamed))
            fn = fnRenamed
        return fn

    def addGenre(self, f):
        f.tag.genre = eyed3.id3.Genre(uPodCast)
        print("initialized {0}".format(f.tag.genre.name))

    def addTag(self, f, fn):
        f.tag = eyed3.id3.Tag()
        f.tag.file_info = eyed3.id3.FileInfo(os.path.join(self.podpath, fn))
        self.addGenre(f)

    def checkTagNone(self, f, fn):
        if f.tag is None:
            print("f.tag is None")
            self.addTag(f, fn)

    def checkTagExists(self, f, fn):
        try:
            print('version is {0}'.format(f.tag.version))
        except:
            print('no tag')
            self.addTag(f, fn)

    def addDT2Name(self, f, fn, prefix):
        m, s = f.info.time_secs / 60, f.info.time_secs % 60
        # if 41 < m and m < 43:
        print('renaming BS file {0}, with minutes {1}, seconds (2)'.format(fn, m, s))
        f.tag.title = prefix + unicode(fn, "UTF-8")

    def updateTag(self, tagVal, fixVal, msg):
        if tagVal == None:
            strtype = None
        else:
            strtype = stringType(tagVal)
        try:
            if strtype == 'u':
                fixedVal = tagVal
            elif strtype == 'a':
                fixedVal = unicode(tagVal, "UTF-8")
            else:
                fixedVal = fixVal

        except:
            print(msg + " problem")
            fixedVal = unicode(fixVal, "UTF-8")
        return fixedVal

def runTagFixer(args):
    dt = datetime.date.today() # date will be used as directory name
    srcdir = dt.strftime('%Y-%m-%d')
    if(args['dir']):
        srcdir = args['dir']
    for fd in feeds:
        tf = TagFixer(srcdir, fd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-d','--dir', help='Specify a source directory', required=False)

    args = vars(parser.parse_args())
    runTagFixer(args)
