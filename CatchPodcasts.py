import urllib
import os
import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pdb
from BSurv import PodcastDBChecker
import argparse
from concat import ConcatVideos
import shutil

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
        'url' : 'http://feeds.bloomberg.fm/BLM2561581769',
        'prefix' : 'BS'
    },
    {
        'subdir' :'takingstock',
        'url' : 'http://feeds.bloomberg.fm/BLM2236960495',
        'prefix' : 'TS'
    },
    {
        'subdir' :'maddow',
        'url' : 'http://podcastfeeds.nbcnews.com/drone/api/query/audio/podcast/1.0/MSNBC-MADDOW-NETCAST-MP3.xml',
        'prefix' : 'RM'
    },
    {
        'subdir' :'axelrod',
        'url' : 'https://rss.art19.com/axe-files',
        'prefix' : 'AX'
    },
    {
        'subdir' : 'planetmoney',
        'url' : 'https://www.npr.org/rss/podcast.php?id=510289',
        'prefix' : 'PM'
    },
    {
        'subdir' : 'gabfest',
        'url' : 'https://feeds.megaphone.fm/slatespoliticalgabfest',
        'prefix' : 'GF'
    },
    {
        'subdir' : 'podsaveamerica',
        'url' : 'http://feeds.feedburner.com/pod-save-america',
        'prefix' : 'PS'
    },
    {
        'subdir' : 'soundinvesting',
        # 'url' : 'http://paulmerriman.com/feed/podcast',
        'url' : 'http://feeds.feedburner.com/PaulMerriman',
        'prefix' : 'SI'
    },
    {
        'subdir' : 'authorswriters',
        'url' : 'https://www.kmweiland.com/wp-content/podcast/podcast-rss.xml',
        'prefix' : 'AW'
    },
    # {
    #     'subdir' : 'wellstoried',
    #     'url' : 'http://feeds.soundcloud.com/users/soundcloud:users:306512413/sounds.rss',
    #     'prefix' : 'WS'
    # },

    #{
    #    'subdir' : 'storygrid',
    #    'url' : 'https://rss.simplecast.com/podcasts/1431/rss',
    #    'prefix' : 'SG'
    #},
    {
        'subdir' : 'otm',
        'url' : 'http://feeds.wnyc.org/onthemedia',
        'prefix' : 'OM'
    },
    {
        'subdir' : 'studio360',
        'url' : 'http://feeds.feedburner.com/studio360/podcast',
        'prefix' : 'S3'
    },
    {
        'subdir' : 'staytuned',
        'url' : 'https://rss.art19.com/stay-tuned-with-preet',
        'prefix' : 'ST'
    },
    {
        'subdir' : 'adventuresng',
        'url' : 'https://feeds.feedwrench.com/AdventuresInAngularOnly.rss',
        'prefix' : 'NG'
    },
    {
        'subdir' : 'talkpython',
        'url' : 'https://talkpython.fm/episodes/rss',
        'prefix' : 'PY'
    },
    {
        'subdir' : 'tdi',
        'url' : 'http://feeds.feedburner.com/tdicasts',
        'prefix' : 'TD'
    },
    {
        'subdir' : 'oath',
        'url' : 'https://feeds.megaphone.fm/theoath',
        'prefix' : 'OT'
    },
    {
        'subdir' : 'nutritionfacts',
        'url' : 'http://nutritionfacts.org/audio/feed/podcast/',
        'prefix' : 'NF'
    },
    {
       'subdir' : 'politicaljunkie',
       'url' : 'https://www.krpoliticaljunkie.com/feed/podcast',
       'prefix' : 'PJ'
    },
    {
       'subdir' : 'backstory',
       'url' : 'http://feeds.feedburner.com/BackStoryRadio',
       'prefix' : 'BK'
    }

]


downloaded = []

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
        # pdb.set_trace()
        try:
            url = self.feed['url']
            s = urllib.urlopen(url)
            contents = s.read()
            # pdb.set_trace()
            if(os.path.isdir(os.path.join(podpathRoot, self.feed['subdir']))) == False:
                os.mkdir(os.path.join(podpathRoot, self.feed['subdir']))
            latest = "latest.xml"
            latestPath = os.path.join(podpathRoot, self.feed['subdir'], latest)
            file = open(latestPath, 'w')
            file.write(contents)
            file.close()
        except:
            pass

    def mangleName(self, nm):
        if(os.path.isdir(os.path.join(podpathRoot, self.feed['subdir'], self.dtStr))) == False:
            os.mkdir(os.path.join(podpathRoot, self.feed['subdir'], self.dtStr))
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
            # pdb.set_trace()
	    uLastPart = url['srcUrl'].rfind('/') + 1
	    uLast = url['srcUrl'][uLastPart:]
            file_name = self.feed['prefix'] + url['tm'] + uLast[0:-4]
            # pdb.set_trace()
            # uLast2 = url.split('/')[6:7][0]
            # print(uLast2)
            # u = 'BS' + timeStamp + ':' + uLast2
            file_name = self.mangleName(file_name)
            # firstPart = file_name[:20]
            # fixedUrl = os.path.join(firstPart, uLast2) + ".mp3"
            print("urlopen {0}".format(url))
            u = urllib.urlopen(url['srcUrl'])

            f = open(file_name, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print(">>>>>>>>>> Downloading: %s Bytes: %s" % (file_name, file_size))
            downloaded.append(file_name)

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
        try:
            tree = ET.parse(os.path.join(podpathRoot, self.feed['subdir'], 'latest.xml'))
            root = tree.getroot()
            tree = ET.parse(os.path.join(podpathRoot, self.feed['subdir'], 'latest.xml'))
            root = tree.getroot()
            parsed = prettify(root)
            #print(parsed)
            # pdb.set_trace()
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
                try:
                    d = self.loaded[ndx]
                    d['pubDate'] = itm.text
                    ndx += 1
                except:
                    print('index error on pubDate')

            #ndx = 0
            #for itm in root.iter('title'):
            #    print(itm.text)
            #    d = self.loaded[ndx]
            #    d['title'] = itm.text
            #    ndx += 1
        except:
            print("no element found error in parsing xml")

    # 'Tue, 05 Apr 2016 14:52:33 GMT'
    # '%a %d %b %Y %T %Z'

    def catchUrls(self, url, dateStr, timeStamp):
        # pdb.set_trace()

    	print("catchUrls {0}".format(url));
            # uLast2 = url.split('/')[3][0:-4]
    	uLastPart = url.rfind('/') + 1
    	uLast2 = url[uLastPart:][0:-4]
        if self.checker.addPodcast(uLast2, dateStr):
            # print(uLast2)
            u = self.feed['prefix'] + timeStamp + ':' + uLast2
            # print(u)
            mangled = self.mangleName(u)
            print("mangled {0} \n from {1}".format(mangled, url))
            if os.path.isfile(mangled) == False:
                self.urls.append({'srcUrl': url, 'tm': timeStamp})

    def reduceToLatest(self):
        self.checker = PodcastDBChecker(self.startover)

        # pdb.set_trace()
        for v in self.loaded.itervalues():
            u = v['url']
            # pdb.set_trace()
            # pdt = v['pubDate'][5:-4]  <--- started having extra -0000 on end
            pdt = v['pubDate']
            pos = pdt.rfind(':') + 3
            pdt = pdt[5:pos]
            try:
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
            except:
                print("date/time formatting problem in {0}".format(pdt))
        self.logfile.close

def summarize():
    print("\n\n|||||||| Downloads ||||||||")
    for download in downloaded:
        print(download)

def collect():
    todaysDate = datetime.datetime.now()
    dtObj = todaysDate.date()
    dtStr = dtObj.strftime("%Y-%m-%d")
    dstdir = os.path.join(podpathRoot, 'collected', dtStr)
    print("\n\n collect podcasts in {0}\n".format(dstdir))
    if(os.path.isdir(dstdir) == False):
        os.mkdir(dstdir)
    for download in downloaded:
        shutil.copy2(download, dstdir)

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
            # catcher.renameUrls()
            catcher.fetchPodcasts()
        summarize()
        collect()

        # tspath = os.path.join(podpathRoot, 'takingstock', srcdir)
        # concatVideos = ConcatVideos(tspath)
        # concatVideos.concat()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-d','--dir', help='Specify a source directory', required=False)
    parser.add_argument('-s','--startover', help='Startover', required=False)
    parser.add_argument('-t','--testurls', help='Test Urls from log file', required=False)

    args = vars(parser.parse_args())
    runPodcastCatcher(args)
