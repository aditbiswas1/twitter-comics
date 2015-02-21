'''
Helper functions for making a Comic Strips
Author: Tushar Makkar <tusharmakkar08[at]gmail.com>
Date: 21.02.2015
'''
import os
from PIL import Image


def imageResize(imageName, height):
    '''
    Returns the image of comic strip
    Args:
        imageName : Name of the image
        height : Desired height of a comic 
    Returns:
        Nothing [Same Height image]
    '''
    os.system("convert "+imageName+" -resize 600x"+str(height)+" "+imageName)
    
def makeComicStrips(comics):
    '''
    Returns the image of comic strip
    Args:
        comics : Array of individaul comic picture
    Returns:
        output.jpg is written as Comic Strip
    '''
    newIm = Image.new('RGB',(500,500))
    steps = 500/len(comics)
    x_cord = 0
    for im in comics:
        im.thumbnail((200,200))
        newIm.paste(im,(x_cord,0))
        x_cord += im.size[0]
    return newIm

if __name__ == '__main__':
    #im1 = '8.jpg'
    #im2 = '9.jpg'
    #im3 = '10.jpg'
    #imageResize(im1, height)
    #imageResize(im2, height)
    #imageResize(im3, height)
    #im11 = Image.open(im1)
    #im21 = Image.open(im2)
    #im31 = Image.open(im3)
    #comics = [im11, im21, im31]
    makeComicStrips(comics)
