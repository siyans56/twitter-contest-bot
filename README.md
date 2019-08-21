# twitter-contest-bot
Will poll for Retweet Contests and retweet them. Forked from https://github.com/kurozael/twitter-contest-bot
------------
Disclaimer
------------

This bot is written purely for educational purposes. I hold no liability for what you do with this bot or what happens to you by using this bot. Abusing this bot *can* get you banned from Twitter, so make sure to read up on [proper usage](https://support.twitter.com/articles/76915-automation-rules-and-best-practices) of the Twitter API.

License
------------

You can fork this repository on GitHub as long as it links back to this original repository. Do not sell this script as I would like the code to remain free.


Prerequisites
------------

  * TwitterAPI
  * Python 2.7
  
  
Python 2.7: https://www.python.org/download/releases/2.7/
For information on how to install python: https://www.howtogeek.com/197947/how-to-install-python-on-windows/
  
Configuration
------------

Open up `config.json` and make the values correspond to your Twitter API credentials.

In order to recieve a consumer key, consumer secret key, access token key, and secret access token key, you will need to reigster an app at https://developer.twitter.com/ (and of course, you must have a Twitter account that you want to use as the owner of said app).

Make sure you change your Twitter Account settings to allow dm's from anybody (Settings -> Privacy and Safety -> Check both boxes under Direct Messages)

Installation
------------
1: Find and Open up Command Prompt
	
2: In Command Prompt Run: pip install TwitterAPI

	Errors: Search Google. Typically it's about python not being installed correctly.

3: Using Notepad (recommended) or your preferred editor open config.json. Fill in with your credentials. For information on how to get Twitter Creds: http://docs.inboundnow.com/guide/create-twitter-application/
	
4: Then run main.py. (Double click on file or python main.py in command prompt) 


Alternatives
-------------

If you're looking for similar projects in alternative languages, check these out:

* *(JavaScript)* https://github.com/raulrene/Twitter-ContestJS-bot


Usefull Links:

https://steemit.com/twitter/@yoghurt/my-experiences-running-a-twitter-giveaway-bot

https://rpiai.com/retweeting-to-win/

https://steemit.com/programming/@kurozael/twitter-contest-bot

https://www.vox.com/2015/10/5/9409017/hack-online-contest-win



	***Depending on how lucky you get you typically win around 0.1% of all contests entered***
