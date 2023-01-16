import openai
import tweepy
import datetime
import time
import config

openai.api_key = config.OPENAI_API_KEY

prompt = """
Make a tweet about a blazing fast javascript framework with a random name that doesn't exists made by someone or something famous, that may or may not exists, that has just been created in a funny way, add totally random, fun and useless details, the total length must be less than 280 characters, don't use quotation marks.
"""

completion = openai.Completion.create(
    engine="text-davinci-003", prompt=prompt, max_tokens=1000)
text = completion.choices[0].text.strip()

print(len(text))
print(text)
