from pydub import AudioSegment
import os
import glob

class ConcatVideos(object):
    def __init__(self, videodir):
        self.mp3dir = videodir

    def concat(self):
        os.chdir(self.mp3dir)
        glb = glob.glob('*.mp3')

        all = AudioSegment.from_mp3(os.path.join(self.mp3dir, glb[0]))

        for i in range(len(glb) - 1) :
            nxtmp3 = AudioSegment.from_mp3(os.path.join(self.mp3dir, glb[i+1]))
            print(glb[i])
            all = all + nxtmp3

        all.export(os.path.join(self.mp3dir, 'TakinStock.mp3'), format = 'mp3')

if __name__ == "__main__":
    mp3dir = '/home/htmkr/BloombergPodcasts/takingstock/2016-08-26'
    concatVideos = ConcatVideos(mp3dir)
    concatVideos.concat()
