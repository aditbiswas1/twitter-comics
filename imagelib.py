import Image
import ImageFont, ImageDraw
from random import randint
import json
import twitter
import urllib
import urlparse, os
from os.path import splitext, basename

bgImages = {
  "happy": [("8.jpg", "8.json"), ("happy1.jpg", "happy1.json"), ("happy2.jpeg", "happy2.json")],
  "sad": [("sad1.jpeg", "sad1.json"), ("sad2.jpeg", "sad2.json")]
}

avatarImage = "avatar.png"
bubbleImage = "bubble.jpg"
bubbleJSON = "bubble.json"

fontSize = 12

def makeComicStrip(comics):
    '''
    Returns the image of comic strip
    Args:
        comics : Array of individaul comic picture
    Returns:
        output.jpg is written as Comic Strip
    '''
    width = 0
    for comic in comics:
      width += comic.size[0]
    height = comics[0].size[1]
    newIm = Image.new('RGB',(width,height))
    steps = 500/len(comics)
    x_cord = 0
    for im in comics:
        newIm.paste(im,(x_cord,0))
        x_cord += im.size[0]
    return newIm

def fileNameFromURL(url):
  path = urlparse.urlparse(url).path
  return basename(path)

def getMaxLineLength(bubbleContentWidth):
  return bubbleContentWidth / fontSize

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
  bx = bx * 1.2
  bh = bh * 0.9
  font = ImageFont.truetype("font.ttf", fontSize)
  draw = ImageDraw.Draw(bg)
  lines = splitIntoLines(text, getMaxLineLength(bw))
  y = by + (bh / 2 - (len(lines) * font.getsize(text)[1]) / 2)
  for line in lines:
    draw.text((bx, y), line, (0, 0, 0), font=font)
    y += fontSize

def downloadImage(url):
  urllib.urlretrieve(url, fileNameFromURL(url))

def drawBox(text, mood):
  imagePoolSize = len(bgImages[mood]) - 2
  index = randint(0, imagePoolSize)
  bg = Image.open(bgImages[mood][index][0])
  jsonData = open(bgImages[mood][index][1])
  imageData = json.load(jsonData)
  x, y, w, h = imageData["x"], imageData["y"], imageData["w"], imageData["h"]
  bx, by, bw, bh = imageData["bx"], imageData["by"], imageData["bw"], imageData["bh"]
  avatar = Image.open(avatarImage).resize((w, h))
  bubble = Image.open(bubbleImage).resize((bw, bh))
  bg.paste(avatar, (x, y))
  bg.paste(bubble, (bx, by))
  bgWidth, bgHeight = bg.size
  draw = ImageDraw.Draw(bg)
  draw.line([(0, 1), (0, bgHeight - 1), (bgWidth - 1, bgHeight - 1), (bgWidth - 1, 1), (0, 1)], width=3, fill="black")
  drawText(bg, text, bx, by, bw, bh)
  return bg

if __name__ == "__main__":
  boxes = []
  for i in range(0, 10):
    boxes.append(drawBox("Hey. How are you doing?", "happy"))
  comic = makeComicStrip(boxes)
  comic.save("comic.jpg")
  '''tw = twitter.Twitter()
  tw.auth("", "")
  tweets = tw.getTweets(["565616594035159041", "565616718786330625"])
  for tweet in tweets:
    downloadImage(tweet["profilePictureURL"])'''
