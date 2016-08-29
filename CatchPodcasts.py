import urllib2
import os
import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pdb
from BSurv import PodcastDBChecker
import argparse
import concat

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# podpathRoot = r'/home/htmkr/Development/PythonProjects/Bloomberg/Podcasts'
podpathRoot = r'/home/htmkr/BloombergPodcasts'

feeds = [
    {
        'subdir' :'surveillance',
        'url' : 'http://www.bloomberg.com/feeds/podcasts/surveillance.xml',
        'prefix' : 'BS'
    },
    {
        'subdir' :'takingstock',
        'url' : 'http://www.bloomberg.com/feeds/podcasts/taking_stock.xml',
        'prefix' : 'TS'
    }
]

class CatchPodcasts():

    def __init__(self, fd, startover, srcDir):
        self.loaded = {}
        self.urls = []
        self.startover = startover
        self.checker = None
        self.feed = fd

        self.todaysDate = datetime.datetime.now()
        print(self.todaysDate)
        daysM3 = datetime.timedelta(days=1)
        self.dM3 = self.todaysDate - daysM3
        print(self.dM3)
        dtObj = self.todaysDate.date()
        self.dtStr = dtObj.strftime("%Y-%m-%d")
        print(self.dtStr)

        self.podpath = os.path.join(podpathRoot, self.feed['subdir'], srcDir)
        print(self.podpath)


        try:
            os.mkdir(self.podpath)
        except:
            pass
        self.logfile = open('NewPodcasts.log', 'w')

    def getLatestXml(self):
        url = self.feed['url']
        s = urllib2.urlopen(url)
        contents = s.read()
        # pdb.set_trace()
        latest = "latest.xml"
        latestPath = os.path.join('Podcasts', self.feed['subdir'], latest)
        file = open(latestPath, 'w')
        file.write(contents)
        file.close()

    def mangleName(self, nm):
        file_name = os.path.join(podpathRoot, self.feed['subdir'], self.dtStr, nm) + '.mp3'
        return file_name

    def renameUrls(self):
        for url in self.urls:
            # pdb.set_trace()
            file_name = url['srcUrl'] #url.split('/')[-2]
            file_name = self.mangleName(file_name)

            print(file_name)

    def fetchPodcasts(self):

        for url in self.urls:
            # pdb.set_trace()Download
            file_name = self.feed['prefix'] + url['tm'] + url['srcUrl'].split('/')[6:7][0]
            # pdb.set_trace()
            # uLast2 = url.split('/')[6:7][0]
            # print(uLast2)
            # u = 'BS' + timeStamp + ':' + uLast2
            file_name = self.mangleName(file_name)
            # firstPart = file_name[:20]
            # fixedUrl = os.path.join(firstPart, uLast2) + ".mp3"
            print("urlopen {0}".format(url))
            u = urllib2.urlopen(url['srcUrl'])

            f = open(file_name, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print("Downloading: %s Bytes: %s" % (file_name, file_size))

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                # print(status)

            f.close()

    def parseXml(self):
        tree = ET.parse(os.path.join('Podcasts', self.feed['subdir'], 'latest.xml'))
        root = tree.getroot()
        tree = ET.parse(os.path.join('Podcasts', self.feed['subdir'], 'latest.xml'))
        root = tree.getroot()
        parsed = prettify(root)
        # print(parsed)

        root = tree.getroot()
        ndx = 0
        for itm in root.iter('enclosure'):
            ats = itm.attrib
            d = {}
            self.loaded[ndx] = d
            d['url'] = ats['url']
            ndx += 1


        ndx = 0
        for itm in root.iter('pubDate'):
            # print(itm.text)parse
            d = self.loaded[ndx]
            d['pubDate'] = itm.text
            ndx += 1

    # 'Tue, 05 Apr 2016 14:52:33 GMT'
    # '%a %d %b %Y %T %Z'

    def catchUrls(self, url, dateStr, timeStamp):
        # pdb.set_trace()

        uLast2 = url.split('/')[6:7][0]
        if self.checker.addPodcast(uLast2, dateStr):
            # print(uLast2)
            u = self.feed['prefix'] + timeStamp + ':' + uLast2
            # print(u)
            mangled = self.mangleName(u)
            print("mangled {0} from {1}".format(mangled, url))
            if os.path.isfile(mangled) == False:
                self.urls.append({'srcUrl': url, 'tm': timeStamp})

    def reduceToLatest(self):
        self.checker = PodcastDBChecker(self.startover)

        # pdb.set_trace()
        for v in self.loaded.itervalues():
            u = v['url']
            # pdb.set_trace()
            pdt = v['pubDate'][5:-4]
            pd = datetime.datetime.strptime(pdt, "%d %b %Y %H:%M:%S")
            if pd > self.dM3:
                fixed = pd.strftime("%Y-%m-%d %H:%M:%S")
                tm = pd.time()
                tmStr = tm.strftime("%H:%M%S")
                v['tmStr'] = tmStr
                dateStr = pd.strftime("%Y-%m-%d")
                tm = pd.time()
                # print(u)
                # print(pd)
                self.logfile.write(u)
                self.logfile.write('\n')
                self.logfile.write(fixed)
                self.logfile.write('\n')
                self.catchUrls(u, dateStr, tmStr)
        self.logfile.close

def runPodcastCatcher(args):
    startover = False
    testurls = False
    if(args['startover']):
        startover = args['startover']

    if args['testurls']:
        testurls = True

    if testurls:
        checker = PodcastDBChecker(startover)
        return checker.loadTestUrls()
    else:
        dt = datetime.date.today() # date will be used as directory name
        srcdir = dt.strftime('%Y-%m-%d')
        if(args['dir']):
            srcdir = args['dir']

        for fd in feeds:
            # pdb.set_trace()
            catcher = CatchPodcasts(fd, startover, srcdir)
            catcher.getLatestXml()
            catcher.parseXml()
            catcher.reduceToLatest()
            catcher.renameUrls()
            catcher.fetchPodcasts()

        tspath = os.path.join(podpathRoot, 'takingstock', srcdir)
        concatVideos = ConcatVideos(tspath)
        concatVideos.concat()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-d','--dir', help='Specify a source directory', required=False)
    parser.add_argument('-s','--startover', help='Startover', required=False)
    parser.add_argument('-t','--testurls', help='Test Urls from log file', required=False)

    args = vars(parser.parse_args())
    runPodcastCatcher(args)
