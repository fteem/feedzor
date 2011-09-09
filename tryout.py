#!/usr/bin/python3


#Forcing feedparser module in path
__file__ = "feedparser/feedparser.py"
import os, sys
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
  sys.path.insert(0, cmd_folder)

import feedparser
import pickle   
import time

def storeToDB(feeds):
  '''A function that gets an argument: all the feeds urls into an array and stores it into a file on disk.'''
  with open('feedurls.data', 'wb') as data_file:
    pickle.dump(feeds, data_file)
  print("All RSS Feeds stored!")    


def loadFromDB():
  '''A function that retrieves all the feeds urls from a file on disk, and returns it.'''
  with open("feedurls.data", "rb") as data_file:
    tmp = pickle.load(data_file)
  return tmp
  
    
def getRSS(feed_urls):
  '''A function that parses all the feed results for the URLs in feed_urls array and prints the results in human readable form.'''
  feed_results = {}
  for url in feed_urls: 
    tmp = feedparser.parse(url)
    results_for_url = []
    for entry in tmp.entries:
      results_for_url.append([entry.updated_parsed, entry.title, entry.link])
    feed_results[tmp.feed.title] = results_for_url[0:10] 
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
    try:
      menu_input = int(input("Choose an option [1, 2, 3, 4]: "))
    except ValueError:
      print("No such option, please try again.")
      menu_input = int(input("Choose an option [1, 2, 3, 4]: "))
    except KeyboardInterrupt:
      sys.exit("Goodbye!")

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
        cnt += 1
      del_choose = int(input("Enter the number of the feed you want to delete:"))
      del feed_urls[del_choose-1]   

 
try:
  feed_urls = loadFromDB()
except EOFError:
  feed_urls = []
  print("No RSS Feed entries. Please add some first.")


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
