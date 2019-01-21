import json
import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin


params = {
    "postal":11206,
    "search_distance":4,
    "s":0
}

base_url = "https://newyork.craigslist.org/search/zip?"
paramstr = urlencode(params)
full_url = base_url + paramstr

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

print(r.content)

links_html = soup.find_all('a',{'class':"result-title hdrlnk"})
links = [link.get('href') for link in links_html]
for link in links:
    print(link)







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