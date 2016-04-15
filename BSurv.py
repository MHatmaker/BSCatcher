#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import datetime
import argparse
import pdb

class PodcastDBChecker(object):
    def __init__(self, startover=False):

        self.existingCatches = []
        self.con = lite.connect('bbsurv.db')
        self.cur = self.con.cursor()
        with self.con:
            if startover:
                self.cur.execute("DROP TABLE IF EXISTS latest")
                self.cur.execute("CREATE TABLE latest(Id INT, Name TEXT, d TEXT)")
                self.id = 0
            else:
                self.cur.execute("select MAX(Id) from latest")
                row = self.cur.fetchone()
                if row[0] == None:
                    self.id = 0
                else:
                    self.id = row[0]
                print("Max ID is {0}".format(self.id))

                self.grabExisting()

    def grabExisting(self):
        self.cur.execute("select Id, Name, d from latest")
        rows = self.cur.fetchall()
        for row in rows:
            self.existingCatches.append(row[1])

    def addPodcast(self, name, dt):
        self.id += 1
        print("name {0}, dt {1}".format(name, dt))
        if self.checkPodcastName(name, dt) == False:
            print("insert {0}".format(name))
            with self.con:
                self.cur.execute("insert into latest(Id, Name, d) values (?, ?, ?)", (self.id, name, dt))
            self.existingCatches.append(name)

    def checkPodcastName(self, nm, today):
        # pdb.set_trace()
        sqlstmt = "select Id, Name, d from latest where Name='{0}'".format(nm)
        self.cur.execute(sqlstmt)
        row = self.cur.fetchone()
        # if row != None:
        #     print("id {0} {1}, Name {2} {3}, date {4} {5}".format(row[0], type(row[0]),
        #         row[1], type(row[1]), row[2], type(row[2])))
        if row != None:
            if row[1] in self.existingCatches:
                print("{0} is already in latest".format(nm))
                return True
            else:
                return False
        else:
            return False

    def loadTestUrls(self):
        with open("NewPodcasts.log") as inf:
            names = inf.readlines()
        odd = True
        uLast2 = ''
        for nm in names:
            if odd :
                # print(nm)
                # pdb.set_trace()
                uLast2 = nm.split('/')[6:7][0]
                print(uLast2)
                self.addPodcast(uLast2, 'ffoooo')
                odd = False
            else:
                odd = True

        print("final print")
        self.cur.execute("select Id, Name, d from latest")
        rows = self.cur.fetchall()
        for row in rows:
            print("id {0}, name {1}".format(row[0], row[1]))

    def checkAgain(self, nm):
        self.cur.execute('select Name as "Name [TEXT]", current_date as "d [date]"')
        row = cur.fetchone()

        print("podcastname {0} {1}, current_date {1} {2}".format(row[0], type(row[0]), row[1], type(row[1])))

def runPodcastDBChecker(args):
    startover = False
    testurls = False
    if(args['startover']):
        startover = args['startover']

    if args['testurls']:
        testurls = True
    checker = PodcastDBChecker(startover)
    if testurls:
        return checker.loadTestUrls()
    else:
        today = datetime.date.today()
        latestpod = 'BS123abcZYX'
        checker.addPodcast(latestpod, today)
        checker.checkPodcastName(latestpod, today)
        # checker.checkAgain(latestpod)

        latestpod = 'abcZYXBS123'
        checker.addPodcast(latestpod, today)
        checker.checkPodcastName(latestpod, today)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-s','--startover', help='Startover', required=False)
    parser.add_argument('-t','--testurls', help='Test Urls from log file', required=False)

    args = vars(parser.parse_args())
    runPodcastDBChecker(args)
