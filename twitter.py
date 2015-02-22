from application_only_auth import Client
import json

class Twitter:
  def __init(self):
    self.client  = None

  def auth(self, consumer_key, consumer_secret):
    self.client = Client(consumer_key, consumer_secret)

  def getTweets(self, ids):
    param = ",".join(ids)
    tweets = self.client.request('https://api.twitter.com/1.1/statuses/lookup.json?id=' + param)
    obj = []
    for tweet in tweets:
      obj.append({
        "text": tweet["text"],
        "profilePictureURL": tweet["user"]["profile_image_url_https"],
        "id": tweet["id"]
      })
    return obj

if __name__ == "__main__":
  auth("", "")

