#!/usr/bin/python
import fileinput
import json
import time
import calendar
import re
import shutil

logfile = "/home/jumblesale/Code/irc/log"
outfile = "/home/krowbar/logs/chatcloud.json"
bannedUsersFile = "/home/krowbar/Code/python/bannedUsers"
bannedWordsFile = "/home/krowbar/Code/python/bannedWords"
wordData = {} # keyed by "word" that contains a count
#we only care about recent chats, let's say for the past sixteen hours
timeTo = calendar.timegm(time.gmtime())
timeCutoff = timeTo - (16 * 60 * 60)
print "Generating word cloud based off words from " + str(timeCutoff) + " to " + str(timeTo)
minOccurance = 3 #we'll have to reduce the minOccurances if we reduce the timeCutoff
minLength = 3 #number of letters long
bannedWords = open(bannedWordsFile).read().splitlines()
bannedUsers = open(bannedUsersFile).read().splitlines()

with open(logfile, "r") as log:
    for line in log:
        try:
            time, user, message = line.split("\t", 3)
            time = int(time)
        except ValueError:
            continue #There are some bad lines in the log file that we'll ignore if we can't parse
        if user in bannedUsers:
            continue #We don't care what they say
        if time >= timeCutoff and time <= timeTo:
            #print "Processing line from " + user + " at " + str(time)
            for word in re.sub('[\'\"\`\/\\;:,.?!*&^\-()<>\{\}|_\[\]0-9]', ' ', message).lower().split():
                #changing symbols into spaces instead of stripping them avoids compounded words
                if len(word) < minLength or word in bannedWords:
                    #print "Rejecting " + word
                    continue
                #if the word already exists in the list
                if word in wordData:
                    wordData[word] += 1
                else: #if they are new
                    wordData[word] = 1
                    #print "Added word: " + word
wordData = {i:wordData[i] for i in wordData if wordData[i] >= minOccurance }
if(len(wordData) == 0):
    wordData = {"NOTHING": 1, "INTERESTING": 1, "TODAY": 1}
with open(outfile + ".tmp", "w") as tmpFile:
    tmpFile.write(json.dumps(wordData))
shutil.move(outfile + ".tmp", outfile)