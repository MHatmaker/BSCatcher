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
    cleaner.removeEmptyFolders(rootdir, True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-d','--startdir', help='Specify a source directory', required=False)

    # pdb.set_trace()
    args = vars(parser.parse_args())
    startCleanup(args)
