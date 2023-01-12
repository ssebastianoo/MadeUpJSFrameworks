import openai
import tweepy
import datetime
import time
import config

client = tweepy.Client(config.TWITTER_API["bearer"], config.TWITTER_API["consumer_key"],
                       config.TWITTER_API["consumer_secret"], config.TWITTER_API["access_token"], config.TWITTER_API["access_secret"])


openai.organization = "org-gyjSW9gSmSrtCqT5w4ZG3Cee"
openai.api_key = config.OPENAI_API_KEY


def tweet_():
    completion = openai.Completion.create(
        engine="text-davinci-003", prompt="Tell me about a blazing fast javascript framework that has just been created by someone from the pop culture that doesn't relate to programming, don't use more than 280 characters", max_tokens=1000)
    client.create_tweet(text=completion.choices[0].text)


def tweet():
    print('Tweeting...')


resetted = False

try:
    f = open("published.txt", "r")
    f.close()
except:
    with open("published.txt", "w") as f:
        f.write("0")

while True:
    print("checking...")
    if datetime.datetime.now().hour >= 19:
        f = open("published.txt", "r")
        published = f.read()
        f.close()

        if published == "0":
            tweet()
            with open("published.txt", "w") as f:
                f.write("1")
                resetted = False
    else:
        if not resetted:
            with open("published.txt", "w") as f:
                f.write("0")
            resetted = True

    time.sleep(5)
