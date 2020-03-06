# remove unused directories
import os
import argparse
import pdb

class DirCleaner():
    def __init__(self, rootdir):
        self.rootdir = rootdir

    def checkDirectories(self):
        # pdb.qrace()
        print(self.rootdir)
        for dirpath, dirnames, files in os.walk(self.rootdir):
            # pdb.set_trace()
            if files:
                print(dirpath, 'has files')
            if not files:
                print(dirpath, 'is empty')

    def cleanSubDirectories(self, path):
        files = os.listdir(path)
        if len(files):
            for f in files:     # date subdirectories for podcast, plus latest.xml file
                fullpath = os.path.join(path, f)
                if os.path.isdir(fullpath):        # date subdirectory
                    for fn in os.listdir(fullpath):
                        if fn.endswith('.mp3'):
                            os.remove(os.path.join(fullpath, fn))
                    os.rmdir(fullpath)


    def cleanDirectories(self):
        rtdir = self.rootdir
        files = os.listdir(rtdir)
        if len(files):
            for f in files:              # podcast directories with date subdirectories
                fullpath = os.path.join(rtdir, f)
                if os.path.isdir(fullpath):
                    self.cleanSubDirectories(fullpath)


    def removeEmptyFolders(self, path, removeRoot=True):
      'Function to remove empty folders'
    #   pdb.set_trace()
      if not os.path.isdir(path):
        return

      # remove empty subfolders
      files = os.listdir(path)
      print("number of files in {0} is {1}".format(path, len(files)))
      if len(files):
        for f in files:
          fullpath = os.path.join(path, f)
          if os.path.isdir(fullpath):
            self.removeEmptyFolders(fullpath)

      # if folder empty, delete it
      files = os.listdir(path)
      if len(files) == 0 and removeRoot:
        print("Removing empty folder: {0}".format(path))
        try:
            os.rmdir(path)
        except:
            print("bad directory")


def startCleanup(args) :
    rootdir = "/home/htmkr/Documents/Development/PythonProjects/PodcastCleanTests"
    if(args['startdir']):
        rootdir = args['startdir']
    cleaner = DirCleaner(rootdir)
    if(args['remove'] == True)  :
        cleaner.removeEmptyFolders(rootdir, True)
    elif(args['clean'] == True) :
        cleaner.cleanDirectories()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-d','--startdir', help='Specify a source directory', required=False)
    parser.add_argument('-c', '--clean', help="Clean intermediate directories", default=False, action='store_true')
    parser.add_argument('-r', '--remove', help="Remove only empty directories", default=False, action='store_true')

    # pdb.set_trace()
    args = vars(parser.parse_args())
    if(args['clean']) :
        if(args['clean'] == True) :
            startCleanup(args)

    if(args['remove']) :
        if(args['remove'] == True) :
            startCleanup(args)
