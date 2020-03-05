# remove unused directories
import os, shutil
import argparse
import pdb

class DirCleaner():
    def __init__(self, rootdir):
        self.rootdir = rootdir
        self.bkupdir = ''

    def checkDirectories(self):
        # pdb.qrace()
        print(self.rootdir)
        for dirpath, dirnames, files in os.walk(self.rootdir):
            # pdb.set_trace()
            if files:
                print(dirpath, 'has files')
            if not files:
                print(dirpath, 'is empty')

    def startBackup(self, bkupdir):
        print("copy files from {0}".format(self.rootdir))
        print("to destination {0}".format(bkupdir))
        self.bkupdir = bkupdir

        # if(os.path.isdir(bkupdir) == False):
        #     os.mkdir(bkupdir)
        self.backup(bkupdir)

    def backup(self, path):    NEED TO LOSE RECURSION
        for dirpath, dirnames, files in os.walk(self.rootdir):
            # pdb.set_trace()
            if files:
                print(dirpath, 'has files')
                print("number of files in {0} is {1}".format(path, len(files)))
            if len(files):
                for f in files:
                    fullpath = os.path.join(path, f)
                    if os.path.isdir(fullpath):
                        self.backup(fullpath)
                    else:
                        shutil.copytree(path, self.bkupdir)

            if not files:
                print


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
    if(args['backup']):
        bkupdir = args['backup']
        cleaner.startBackup(bkupdir)
    else:
        cleaner.removeEmptyFolders(rootdir, True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-d','--startdir', help='Specify a source directory', required=False)
    parser.add_argument('-c', '--backup', help='Specify a copy destination directory', required=False)

    # pdb.set_trace()
    args = vars(parser.parse_args())
    startCleanup(args)
