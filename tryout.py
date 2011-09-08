#!/usr/bin/python3


#Forcing feedparser module in path
__file__ = "feedparser/feedparser.py"
import os, sys
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
  sys.path.insert(0, cmd_folder)

import feedparser #Importing feedparser
import pickle     #Importing pickle


def storeRecords(feeds):
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
  feed_results = {}
  for url in feed_urls: #for each url in urls that were read from the DB
    tmp = feedparser.parse(url) #create a tmp dictionary that contains all data from the RSSFeed
    results_for_url = [] #creating an array that will hold the name and the link to the story
    for entry in tmp.entries: 
      results_for_url.append([entry.title, entry.link]) #append the story title and story link to as an array to the results array
    feed_results[tmp.feed.title] = results_for_url #feed_results[title_of_the_feed] = all the results for that site feed
  return feed_results #returning all the results for a feed


def printMenu():
  print("="*80)
  print("Welcome to my console RSS reader!")
  print("="*80)
  print("1. Enter a new feed url")
  print("2. Read RSS")
  print("3. Delete feed url")
  print("4. Exit RSS Reader")
  print("="*80)


try:
  feed_urls = loadFromDB()
except EOFError:
  feed_urls = []
  print("No RSS Feed entries. Please add some first.")

results = {}
while True:

  printMenu()
  menu_input = int(input("Choose an option [1, 2, 3, 4]:"))

  if menu_input == 4:
    storeRecords(feed_urls)
    sys.exit("Goodbye!")
  elif menu_input == 1:
    feed_url = str(input("Please enter the url to the RSS feed: "))
    feed_urls.append(feed_url)
    print("The Feed URL has been saved.")
  elif menu_input == 2:
    results = getRSS(feed_urls)
    for feed_name, entries in results.items():
      print(80*"=")
      print("Feed for: ",feed_name)
      print(80*"=")
      for entry in entries:
        print("Title: {0}\t|\tLink to story: {1}".format(entry[0], entry[1]))
