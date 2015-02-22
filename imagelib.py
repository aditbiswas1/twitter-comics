from PIL import Image
from PIL import ImageFont, ImageDraw
from random import randint
import json
import twitter
import twitterSentiment
import urllib
import urlparse, os
from os.path import splitext, basename

bgImages = {"happy": {"bg": ["happy/bg/"+str(x)+".jpg" for x in xrange(1,11)],"fg": ["happy/fg/"+str(x)+".jpg" for x in xrange(1,7)]},
  "sad": {"bg": ["sad/bg/"+str(x)+".jpg" for x in xrange(1,11)],"fg": ["sad/fg/"+str(x)+".jpg" for x in xrange(1,7)]},
  "love": {"bg": ["love/bg/"+str(x)+".jpg" for x in xrange(1,11)],"fg": ["love/fg/"+str(x)+".jpg" for x in xrange(1,6)]},
  "anger": {"bg": ["anger/bg/"+str(x)+".jpg" for x in xrange(1,11)],"fg": ["anger/fg/"+str(x)+".jpg" for x in xrange(1,7)]},
  "neutral": {"bg": ["neutral/bg/"+str(x)+".jpg" for x in xrange(1,11)],"fg": ["neutral/fg/"+str(x)+".jpg" for x in xrange(1,8)]}
}

avatarImage = "avatar.png"
bubbleImage = "bubble.jpg"

fontSize = 10

comicHeight = 200

def makeComicStrip(comics):
    width = 0
    for comic in comics:
      width += comic.size[0]
    height = comics[0].size[1]
    newIm = Image.new('RGB',(width,height))
    x_cord = 0
    for im in comics:
        newIm.paste(im,(x_cord,0))
        x_cord += im.size[0]
    return newIm

def fileNameFromURL(url):
  path = urlparse.urlparse(url).path
  return basename(path)

def getMaxLineLength(bubbleContentWidth, scaledFontSize):
  return bubbleContentWidth / scaledFontSize

def splitIntoLines(text, maxLength):
  words = text.split(" ")
  length = 0
  line = ""
  lines = []
  for word in words:
    if length + len(word) + 1 < maxLength:
      line += word + " "
      length += len(word) + 1
    else:
      lines.append(line)
      line = word + " "
      length = len(line)
  lines.append(line)
  return lines

def drawText(bg, text, bx, by, bw, bh):
  bx = bx + bw * 0.2
  bh = bh * 0.9
  scaledFontSize = fontSize * bg.size[1] / 165
  font = ImageFont.truetype("font.ttf", scaledFontSize)
  draw = ImageDraw.Draw(bg)
  lines = splitIntoLines(text, getMaxLineLength(bw, scaledFontSize))
  y = by + (bh / 2 - (len(lines) * font.getsize(text)[1]) / 2)
  for line in lines:
    draw.text((bx, y), line, (0, 0, 0), font=font)
    y += scaledFontSize

def downloadImage(url):
  urllib.urlretrieve(url, fileNameFromURL(url))
  return fileNameFromURL(url)

def drawBox(text, mood, avatarImage):
  imagePoolSize = len(bgImages[mood]["fg"]) - 1
  index = randint(0, imagePoolSize)
  character = Image.open(bgImages[mood]["fg"][index])
  jsonData = open(bgImages[mood]["fg"][index][:-3]+"json")
  imageData = json.load(jsonData)
  x, y, w, h = int(imageData["x"]), int(imageData["y"]), int(imageData["w"]), int(imageData["h"])
  bx, by, bw, bh = int(imageData["bx"]), int(imageData["by"]), int(imageData["bw"]), int(imageData["bh"])
  avatar = Image.open(avatarImage).resize((w, h))
  character.paste(avatar, (x, y))
  bgWidth, bgHeight = character.size
  draw = ImageDraw.Draw(character)
  draw.line([(0, 1), (0, bgHeight - 1), (bgWidth - 1, bgHeight - 1), (bgWidth - 1, 1), (0, 1)], width=3, fill="black")
  drawText(character, text, bx, by, bw, bh)
  character = character.resize((character.size[0] * comicHeight / character.size[1], comicHeight))
  return character

def makeComic(ids):
  def tweetID(tweet):
    return tweet["id"]
  boxes = []
  tw = twitter.Twitter()
  tw.auth("wZQDRv06h28EMGrFO7KRUo2hc", "G3QF6xxBhaGATVdIpmxE1PkVuXIVAMAkasCGeUwOc9ir1rWZ7D")
  tweets = tw.getTweets(ids)
  tweets.sort(key=tweetID)
  for tweet in tweets:
    classified = twitterSentiment.tweetClassifier(tweet["text"])
    avatarImage = downloadImage(tweet["profilePictureURL"])
    boxes.append(drawBackground(drawBox(twitterSentiment.cleanTweet(tweet["text"]), classified, avatarImage), classified))

  comic = makeComicStrip(boxes)
  comic.save("results/comic.jpg")

def drawBackground(image, mood):
  imagePoolSize = len(bgImages[mood]["bg"]) - 1
  index = randint(0, imagePoolSize)
  bg = Image.open(bgImages[mood]["bg"][index])
  bg = bg.resize((bg.size[0] * comicHeight / bg.size[1], comicHeight))
  bg.paste(image, (bg.size[0] / 2 - image.size[0] / 2, 0))
  return bg

if __name__ == "__main__":
  comic = makeComic(["569351099901046784", "569351749829464064", "569353056950681600", "569353331052642304", "569353718325358592"])
