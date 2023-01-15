import openai
import tweepy
import datetime
import time
import config

client = tweepy.Client(config.TWITTER_API["bearer"], config.TWITTER_API["consumer_key"],
                       config.TWITTER_API["consumer_secret"], config.TWITTER_API["access_token"], config.TWITTER_API["access_secret"])


openai.api_key = config.OPENAI_API_KEY


def tweet():
    try:
        prompt = """
Make a tweet about a blazing fast javascript framework with a random name that doesn't exists made by someone or something famous, that may or may not exists, that has just been created in a funny way, add totally random, fun and useless details, the total length must be less than 280 characters.
        """
        completion = openai.Completion.create(
            engine="text-davinci-003", prompt=prompt, max_tokens=1000)
        text = completion.choices[0].text.strip()
        if text.startswith('.'):
            text = text[1:].strip()
        client.create_tweet(text=text)
        print("Tweeted!")
    except Exception as e:
        print(e)


try:
    f = open("published.txt", "r")
    f.close()
except:
    with open("published.txt", "w") as f:
        f.write("0")

resetted = False

while True:
    if datetime.datetime.now().hour >= 14:
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
