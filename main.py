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
        Write a short text (Max 240 characters) about a new JavaScript framework that has just been created by a famous person in the modern culture.
    """
    res = ses.post(config.AI['url'], data=json.dumps({
        'question': prompt,
    }), headers={
        "x-secret": config.AI['secret'],
        "User-Agent": config.AI['User-Agent'],
        "Origin": config.AI['Origin'],
    })

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
            time.sleep(20)

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
