from pydub import AudioSegment
import os
import glob

mp3dir = '/home/htmkr/BloombergPodcasts/takingstock/2016-08-26'
os.chdir(mp3dir)
glb = glob.glob('*.mp3')

all = AudioSegment.from_mp3(os.path.join(mp3dir, glb[0]))

for i in range(len(glb) - 1) :
    nxtmp3 = AudioSegment.from_mp3(os.path.join(mp3dir, glb[i+1]))
    print(glb[i])
    all = all + nxtmp3

all.export(os.path.join(mp3dir, 'all.mp3'), format = 'mp3')
