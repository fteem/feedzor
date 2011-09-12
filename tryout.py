#!/usr/bin/python3


#Forcing feedparser module in path
import os, sys
feedparser_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedparser")
if feedparser_dir not in sys.path:
  sys.path.insert(0, feedparser_dir)

import feedparser
import pickle   
import time
from collections import defaultdict

def storeToDB(feeds):
  '''A function that gets an argument: all the feeds urls into an list and stores it into a file on disk.'''
  try:
    with open('feedurls.data', 'wb') as data_file:
      pickle.dump(feeds, data_file)
    print("All RSS Feeds stored!")    
  except IOError as ioerr:
    print("Error occured: ", ioerr)


def loadFromDB():
  '''A function that retrieves all the feeds urls from a file on disk, and returns it.'''
  try:
    with open("feedurls.data", "rb") as data_file:
      tmp = pickle.load(data_file)
  except IOError:
    tmp = []
  return tmp
  
    
def getRSS(feed_urls):
  '''A function that parses all the feed results for the URLs in feed_urls array and prints the results in human readable form.'''
  feed_results = defaultdict(list)
  for url in feed_urls: 
    tmp = feedparser.parse(url)
    for entry in tmp.entries[:10]:
      feed_results[tmp.feed.title].append([entry.updated_parsed, entry.title, entry.link])
  for feed_name, entries in feed_results.items():
    print(120*"=")
    print("Feed for: ",feed_name)
    print(120*"=")
    for entry in entries:
      print("[Posted:] {0}\t[Title:] {1}\t[URL:] {2}".format(time.asctime(entry[0]), entry[1], entry[2]))


def printMenu():
  print("="*120)
  print("Welcome to my console RSS reader!")
  print("="*120)
  print("1. Enter a new feed url")
  print("2. Read RSS")
  print("3. Delete feed url")
  print("4. Exit RSS Reader")
  print("="*80)



def invokeMenu(feed_urls):
  while True:
    printMenu()
    while True:
      try:
        menu_input = int(input("Choose an option [1, 2, 3, 4]: "))
        if 1 > menu_input > 4 :
          raise ValueError
      except ValueError:
        print("No such option, please try again.")
        continue
      except KeyboardInterrupt:
        sys.exit("Goodbye!")
      break

    if menu_input == 4:
      storeToDB(feed_urls)
      sys.exit("Goodbye!")

    elif menu_input == 1:
      feed_url = str(input("Please enter the url to the RSS feed: "))
      feed_urls.append(feed_url)
      print("The Feed URL has been saved.")

    elif menu_input == 2:
      getRSS(feed_urls)

    elif menu_input == 3:
      cnt = 0
      for url in feed_urls:
        print("{0}. {1}".format(cnt+1, url))
      try:
        del_choose = int(input("Enter the number of the feed you want to delete:"))
        del feed_urls[del_choose-1]   
      except KeyboardInterrupt:
        break
      except:
        print("That record cannot be deleted/doesn't exist.")


def main(): 
  feed_urls = loadFromDB()
  if len(sys.argv) < 2:
    invokeMenu(feed_urls)
  elif sys.argv[1] == "-r":
    getRSS(feed_urls)
  elif sys.argv[1] == "-a":
    feed_urls.append(sys.argv[2])
    print("URL: {0} added to database.".format(sys.argv[2]))
    storeToDB(feed_urls)
  elif sys.argv[1] == "-d":
    print("Not available yet!")
  elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
    print("Feedzor - a CLI RSS Reader")
    print("Options:")
    print("No Arguments : Loads an interactive menu.")
    print("-r : Prints all RSS from DB")
    print("-a <url to rss> : Adds an URL to the database.")
    print("-d <url to rss> : Deletes that url from the database.")

if __name__ == "__main__":
  main()
