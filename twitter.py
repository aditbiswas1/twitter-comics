from application_only_auth import Client

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
        "profilePictureURL": tweet["user"]["profile_image_url_https"]
      })
    return obj

  def getRepliesFor(self, id):
    tweet = self.client.request('https://api.twitter.com/1.1/statuses/lookup.json?id=' + id)[0]
    userName = tweet["user"]["screen_name"]
    tweets = self.client.request('https://api.twitter.com/1.1/search/tweets.json?q=@' + userName + '&result_type=recent&count=100')
    replies = []
    while (tweets and len(tweets["statuses"]) >= 100):
      print len(tweets["statuses"])
      print tweets["statuses"][0]["id"]
      for tweet in tweets["statuses"]:
        if tweet["in_reply_to_status_id"] == id:
          replies.append(tweet["id"])
      print replies
      tweets = self.client.request('https://api.twitter.com/1.1/search/tweets.json' + tweets['search_metadata']["next_results"] + '&result_type=recent')

    print replies
    return replies
