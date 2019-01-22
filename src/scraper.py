import json
import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin


# import schedule
# import time

# def job():
#     print("I'm working...")

# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)


params = {
    "postal":11206,
    "search_distance":4,
    "s":0
}

base_url = "https://newyork.craigslist.org/search/zip?"
paramstr = urlencode(params)
full_url = base_url + paramstr

# some really long text that is gonna get highlighted some really long text that is gonna get highlighted some really long text that is gonna get highlighted some really long text that is gonna get highlighted


with open('user_agents.txt','r') as f:
    user_agents = set(line.strip() for line in f.readlines())


download = False

if download:
    r = requests.get(full_url,headers={'User-Agent':random.sample(user_agents,1)[0]})
    with open("cache_html.html",'w') as f:
        f.write(r.content.decode())


with open('cache_html.html','r') as f:
    content = f.read()

soup = BeautifulSoup(content,'lxml')


# pretty easy to get all of the links of the listing from a craigslist search page. 
# Scroll through the pages, adding LINK_LENGTH to s parameter until the length of the returned link list
# is zero. 

# As far as the specific searches you are interested in, repeat them approximately once every 20-30 minutes. 
# If you can develop some sophisticated proxy usage, then you can afford to do this more frequently, at perhaps
# a rate of every 5 minutes. 

# add all of these listing to a master list of urls to scrape. Keep track of already scraped URLs,
# it is almost never necessary to visit a page more than once.
# Pick from these listings at random

# print(r.content)

links_html = soup.find_all('a',{'class':"result-title hdrlnk"})
links = [(link.get('href'),link.text) for link in links_html]
for link in links:
    print(link)






# 1 Every X minutes, search the entire CL > for sale > free stuff > new york city within a specific 
# minimum distance (maybe 10 miles) of your home, for items up to 7 days old. 
#       Gather the titles and the links from these searches. 
# 2 Every poisson(Z) seconds, grab a link from  the set of unscraped listings.unscraped
    # Go to the link, get the data and update the model.


# IDEA:
# You can write a program that will let you rate as many listings as you can, and if you have about 200+ datapoints
# you could draw a basic regression, and go from there.
# data points will include distance, time posted (in relation to today), number of images, 
# possibly content of images (much more work), specific entity presence (perhaps with fuzzing) 
# e.g. guitar, desk, table (each with their own "coefficients")

# About the "specific entity presence" - handle the unusual case of a combination of keywords being present together
# e.g. giving away my guitar desk table for free! 

# When a new listing scores above a high threshold (0.9), alert via email immediately.
# When a new listing scores above a medium threshold but beneath the high threshold, put into a digest for the hour. 
# Have variable length digests, and the different length digests should have different metrics for whats pertinent.
#           e.g. in the hourly digests the timestamp difference between listings is not too significant. (maybe it is??)
#               in the weekly digests, being a day old is very different from being 6 days old!





"""
CraigsList Scanner App Idea
Scan the Craigslist Free Stuff Index for your locale approximately once every 10 minutes.
Create a DB/cache of all of the postings (keep it limited to one month of age). 
Use some heuristics to generate a score for the item, as far as how likely you are to be interested in it.
Some heuristics include:
    - baseline interest level in item. e.g., I'll take practically any guitar or keyboard, I would take some desks/tables/chairs, and I would never take a fucking staircase (they were giving away a STAIRCASE on  CL, as in come to my house with contractors and remove the staircase from the house and take it with you... ?!?!)
    - amount of pictures and quality of pictures. If there are several pictures of a high-resolution, that's way better than one pic of 320x320 or something (or than no pic).
    - distance from my house! I'm not sure right off the bat how I'll get this programmatically
    - the amount of text present on the page. This shouldn't weigh in too much, but if there's a decent amount of text then it implies that the owner is serious about the listing. If theres like 4-5 words, there's a chane that they're noncommittal and that they might even forget they made a listing.
    - if there is a phone number

Presentations of this information:
    - Get a daily digest of all the popular items that are above a certain threshold. You should be able to scroll this digest similarly to how you would scroll on CL. However, make it look a bit prettier (not at the cost of smoothness though)
    - Get instant email alerts about specific items that really high scoring.

"""