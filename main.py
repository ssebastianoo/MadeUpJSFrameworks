import tweepy
import datetime
import time
import config
import requests
import json

client = tweepy.Client(config.TWITTER_API["bearer"], config.TWITTER_API["consumer_key"],
                       config.TWITTER_API["consumer_secret"], config.TWITTER_API["access_token"], config.TWITTER_API["access_secret"])

# openai.api_key = config.OPENAI_API_KEY

ses = requests.Session()

def prompt():
    prompt = """
        Make a tweet about a blazing fast javascript framework with a random name that doesn't exists made by someone or something famous, that may or may not exists, that has just been created in a funny way, add totally random, fun and useless details, the total length must be less than 280 characters, don't use quotation marks.
    """
    res = ses.post(config.AI['url'], data=json.dumps({
        'question': prompt,
        'secret': config.AI['secret']
    }))

    if res.status_code != 200:
        return {
            'success': False
        }

    return {
        'result': res.json()['answer']['content'],
        'success': True
    }

def tweet():
    ai = prompt()

    if not ai['success']:
        print("couldn't generate")
        return
    
    text = ai['result']

    print(text)
    posted = False

    while not posted:
        try:
            client.create_tweet(text=text)
            posted = True
        except Exception as e:
            print(e)
            posted = False

    print("Tweeted!")

    r = ses.post("https://botsin.space/api/v1/statuses", data=json.dumps({"status": text}), headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + config.MASTODON_SECRET
    })
    if r.status_code == 200:
        print("Tooted!")
    else:
        print("couldn't toot")


try:
    f = open("published.txt", "r")
    f.close()
except:
    with open("published.txt", "w") as f:
        f.write("0")

resetted = False

while True:
    if datetime.datetime.now().hour >= config.POST_HOUR:
        f = open("published.txt", "r")
        published = f.read()
        f.close()

        if str(published).strip() == "0":
            tweet()
            with open("published.txt", "w") as f:
                f.write("1")
                resetted = False
    else:
        if not resetted:
            with open("published.txt", "w") as f:
                f.write("0")
            resetted = True

    time.sleep(60 * 30)
