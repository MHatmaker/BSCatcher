import urllib2
import os
import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pdb

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


class CatchPodcasts():

    def __init__(self):
        self.loaded = {}
        self.urls = []

        self.todaysDate = datetime.datetime.now()
        print(self.todaysDate)
        daysM3 = datetime.timedelta(days=1)
        self.dM3 = self.todaysDate - daysM3
        print(self.dM3)
        dtObj = self.todaysDate.date()
        self.dtStr = dtObj.strftime("%Y-%b-%d")
        print(self.dtStr)
        try:
            os.mkdir(os.path.join('Podcasts', self.dtStr))
        except:
            pass
        self.logfile = open('NewPodcasts.log', 'w')

    def getLatestXml(self):
        url = "http://www.bloomberg.com/feeds/podcasts/surveillance.xml"
        s = urllib2.urlopen(url)
        contents = s.read()
        latestPath = os.path.join('Podcasts', "latest.xml")
        file = open(latestPath, 'w')
        file.write(contents)
        file.close()

    def mangleName(self, nm):
        file_name = os.path.join('Podcasts', self.dtStr, nm) + '.mp3'
        return file_name

    def renameUrls(self):
        for url in self.urls:
            # pdb.set_trace()
            file_name = url['srcUrl'] #url.split('/')[-2]
            file_name = self.mangleName(file_name)

            print(file_name)

    def downloadPodcasts(self):

        for url in self.urls:
            # pdb.set_trace()
            file_name = 'BS' + url['tm'] + url['srcUrl'].split('/')[6:7][0]
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
        tree = ET.parse(os.path.join('Podcasts', 'latest.xml'))
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
            # print(itm.text)
            d = self.loaded[ndx]
            d['pubDate'] = itm.text
            ndx += 1

    # 'Tue, 05 Apr 2016 14:52:33 GMT'
    # '%a %d %b %Y %T %Z'

    def catchUrls(self, url, timeStamp):
        # pdb.set_trace()
        uLast2 = url.split('/')[6:7][0]
        # print(uLast2)
        u = 'BS' + timeStamp + ':' + uLast2
        # print(u)
        mangled = self.mangleName(u)
        print("mangled {0} from {1}".format(mangled, url))
        if os.path.isfile(mangled) == False:
            self.urls.append({'srcUrl': url, 'tm': timeStamp})

    def reduceToLatest(self):
        for v in self.loaded.itervalues():
            u = v['url']
            # pdb.set_trace()
            pdt = v['pubDate'][5:-4]
            pd = datetime.datetime.strptime(pdt, "%d %b %Y %H:%M:%S")
            if pd > self.dM3:
                fixed = pd.strftime("%Y-%b-%d %H:%M:%S")
                tm = pd.time()
                tmStr = tm.strftime("%H:%M%S")
                v['tmStr'] = tmStr
                # print(u)
                # print(pd)
                self.logfile.write(u)
                self.logfile.write('\n')
                self.logfile.write(fixed)
                self.logfile.write('\n')
                self.catchUrls(u, tmStr)
        self.logfile.close

if __name__ == "__main__":
    catcher = CatchPodcasts()
    catcher.getLatestXml()
    catcher.parseXml()
    catcher.reduceToLatest()
    catcher.renameUrls()
    catcher.downloadPodcasts()
