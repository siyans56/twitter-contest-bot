from TwitterAPI import TwitterAPI
import threading
import time
import json
import os.path
import sys

# TODO:
# - Add location filter
# - Add user prompt
# - Add a GUI
# - Turn into an exe appli

# US_GEOBOX = [24.825716, 49.064126, -66.987401, -125.540986]
#  {'locations':'-74,40,-73,41'})
#     top right: 41, -73 MINE: 48.814831, -66.193620
#     bottom left: 40, -74 MINE: 24.662450, -127.928023

# Load our configuration from the JSON file.
with open('config.json') as data_file: #get file object and alias as data_file
        data = json.load(data_file) #load json data into a dict

# These vars are loaded in from config.
consumer_key = data["consumer-key"] #Copy in data from JSON
consumer_secret = data["consumer-secret"] #Copy in data from JSON
access_token_key = data["access-token-key"] #Copy in data from JSON
access_token_secret = data["access-token-secret"] #Copy in data from JSON
retweet_update_time = data["retweet-update-time"] #Copy in data from JSON
scan_update_time = data["scan-update-time"] #Copy in data from JSON
rate_limit_update_time = data["rate-limit-update-time"] #Copy in data from JSON
min_ratelimit = data["min-ratelimit"] #Copy in data from JSON
min_ratelimit_retweet = data["min-ratelimit-retweet"] #Copy in data from JSON
min_ratelimit_search = data["min-ratelimit-search"] #Copy in data from JSON
search_queries = data["search-queries"] #Copy in data from JSON
follow_keywords = data["follow-keywords"] #Copy in data from JSON
fav_keywords = data["fav-keywords"] #Copy in data from JSON

# Don't edit these unless you know what you're doing.
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret) #Auth account with TwitterAPI using provided data
post_list = list() #Define empty list for successful posts
ignore_list = list() #Define empty list for posts to ignore
ratelimit=[999,999,100] #Define values for the ratelimit
ratelimit_search=[999,999,100] #Define values for search ratelimit

if os.path.isfile('ignorelist'): #Check if file ignorlist exists
        print("Loading ignore list") #Progress print
        with open('ignorelist') as f: #opens file stream as long as it is needed
                ignore_list = f.read().splitlines() #Reads current ignore list and stores in ignore_list list
        f.close() #close filestream


# Print and log the text
def LogAndPrint( text ):
        tmp = str(text) #Convert text to string
        tmp = text.replace("\n","") #Removes newlines with commas
        print(tmp) #Print to console
        f_log = open('log', 'a') #Open file with name log, in appending mode
        f_log.write(tmp + "\n") #Write to file the given text with newline
        f_log.close() #Close filestream

def CheckError( r ):
        r = r.json() #Create a json object? Convert file to json and check if valid
        if 'errors' in r: #If errors are written in dimensional list
                LogAndPrint("We got an error message: " + r['errors'][0]['message'] + " Code: " + str(r['errors'][0]['code']) )
                #Print out the error message and then the code

def CheckRateLimit(): #Check the rate we are interacting?
        c = threading.Timer(rate_limit_update_time, CheckRateLimit) # Executes the CheckRateLimit func at the rate_limit_update_time interval in seconds
        c.daemon = True; # Makes this unix program run in the background
        c.start() #beings running the program

        global ratelimit #variable for
        global ratelimit_search #variabel for

        if ratelimit[2] < min_ratelimit: #check if the rate we set is too low
                print("Ratelimit too low -> Cooldown (" + str(ratelimit[2]) + "%)") #Print error
                time.sleep(200) #Wait for next try 200 seconds

        r = api.request('application/rate_limit_status').json() #Requests appli

        #Current Rate limits
        # Liking a post: 1000 / day
        # Retweeting: 300 / 3 hours = 2400 / day
        # Following: 1000 / day
        # Searching: 450 / 15 min

        if 'resources' in r:
                for res_family in r['resources']:
                        for res in r['resources'][res_family]:
                                limit = r['resources'][res_family][res]['limit']
                                remaining = r['resources'][res_family][res]['remaining']
                                percent = float(remaining)/float(limit)*100

                                if res == "/search/tweets":
                                        ratelimit_search=[limit,remaining,percent]

                                if res == "/application/rate_limit_status":
                                        ratelimit=[limit,remaining,percent]

                                #print(res_family + " -> " + res + ": " + str(percent))
                                if percent < 5.0:
                                        LogAndPrint(res_family + " -> " + res + ": " + str(percent) + "  !!! <5% Emergency exit !!!")
                                        sys.exit(res_family + " -> " + res + ": " + str(percent) + "  !!! <5% Emergency exit !!!")
                                elif percent < 30.0:
                                        LogAndPrint(res_family + " -> " + res + ": " + str(percent) + "  !!! <30% alert !!!")
                                elif percent < 70.0:
                                        print(res_family + " -> " + res + ": " + str(percent))


# Update the Retweet queue (this prevents too many retweets happening at once.)
def UpdateQueue():
        u = threading.Timer(retweet_update_time, UpdateQueue)
        u.daemon = True;
        u.start()

        print("=== CHECKING RETWEET QUEUE ===")

        print("Queue length: " + str(len(post_list)))

        if len(post_list) > 0:

                if not ratelimit[2] < min_ratelimit_retweet:

                        post = post_list[0]
                        LogAndPrint("Retweeting: " + str(post['id']) + " " + str(post['text'].encode('utf8')))

                        CheckForFollowRequest(post)
                        CheckForFavoriteRequest(post)

                        r = api.request('statuses/retweet/:' + str(post['id']))
                        CheckError(r)
                        post_list.pop(0)

                else:

                        print("Ratelimit at " + str(ratelimit[2]) + "% -> pausing retweets")


# Check if a post requires you to follow the user.
# Be careful with this function! Twitter may write ban your application for following too aggressively
def CheckForFollowRequest(item):
        text = item['text']
        if any(x in text.lower() for x in follow_keywords):
                try:
                        r = api.request('friendships/create', {'screen_name': item['retweeted_status']['user']['screen_name']})
                        CheckError(r)
                        LogAndPrint("Follow: " + item['retweeted_status']['user']['screen_name'])
                except:
                        user = item['user']
                        screen_name = user['screen_name']
                        r = api.request('friendships/create', {'screen_name': screen_name})
                        CheckError(r)
                        LogAndPrint("Follow: " + screen_name)


# Check if a post requires you to favorite the tweet.
# Be careful with this function! Twitter may write ban your application for favoriting too aggressively
def CheckForFavoriteRequest(item):
        text = item['text']

        if any(x in text.lower() for x in fav_keywords):
                try:
                        r = api.request('favorites/create', {'id': item['retweeted_status']['id']})
                        CheckError(r)
                        LogAndPrint("Favorite: " + str(item['retweeted_status']['id']))
                except:
                        r = api.request('favorites/create', {'id': item['id']})
                        CheckError(r)
                        LogAndPrint("Favorite: " + str(item['id']))


# Scan for new contests, but not too often because of the rate limit.
def ScanForContests():
        t = threading.Timer(scan_update_time, ScanForContests)
        t.daemon = True;
        t.start()

        global ratelimit_search

        if not ratelimit_search[2] < min_ratelimit_search:

                print("=== SCANNING FOR NEW CONTESTS ===")


                for search_query in search_queries:

                        print("Getting new results for: " + search_query)

                        try:
                                # Search for tweets matching query WITHIN approximate US area
                                r = api.request('search/tweets', {'q':search_query, 'result_type':"recent", 'count':100, 'locations':'-127.928023, 24.662450, -66.193620, 48.814831'})
                                CheckError(r)
                                c=0

                                for item in r:

                                        c=c+1
                                        user_item = item['user']
                                        screen_name = user_item['screen_name']
                                        text = item['text']
                                        text = text.replace("\n","")
                                        id = str(item['id'])
                                        original_screen_name = screen_name
                                        original_id=id
                                        is_retweet = 0

                                        if 'retweeted_status' in item:

                                                is_retweet = 1
                                                original_item = item['retweeted_status']
                                                original_id = str(original_item['id'])
                                                original_user_item = original_item['user']
                                                original_screen_name = original_user_item['screen_name']

                                        if not original_id in ignore_list:

                                                if not original_screen_name in ignore_list:

                                                        if not screen_name in ignore_list:

                                                                if item ['retweet_count'] > 50:

                                                                        post_list.append(item)
                                                                        f_ign = open('ignorelist', 'a')

                                                                        if is_retweet:
                                                                                print(id + " - " + screen_name + " retweeting " + original_id + " - " + original_screen_name + ": " )
                                                                                ignore_list.append(original_id)
                                                                                f_ign.write(original_id + "\n")
                                                                        else:
                                                                                print(id + " - " + screen_name + ": " )
                                                                                ignore_list.append(id)
                                                                                f_ign.write(id + "\n")

                                                                        f_ign.close()

                                                else:

                                                        if is_retweet:
                                                                print(id + " ignored: " + screen_name + " on ignore list")
                                                        else:
                                                                print(screen_name + " in ignore list")

                                        else:

                                                if is_retweet:
                                                        print(id + " ignored: " + original_id + " on ignore list")
                                                else:
                                                        print(id + " in ignore list")

                                print("Got " + str(c) + " results")

                        except Exception as e:
                                print("Could not connect to TwitterAPI - are your credentials correct?")
                                print("Exception: " + str(e))

        else:

                print("Search skipped! Queue: " + str(len(post_list)) + " Ratelimit: " + str(ratelimit_search[1]) + "/" + str(ratelimit_search[0]) + " (" + str(ratelimit_search[2]) + "%)")


CheckRateLimit()
ScanForContests()
UpdateQueue()

while (True):
    time.sleep(100)
