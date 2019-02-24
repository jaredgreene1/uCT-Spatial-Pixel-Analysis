import math
import matplotlib.pyplot as plt

from PIL import Image
from itertools import permutations


PHOTO_FILE = '735.2.png'


def drawCircle(image, circlePoints, color):
    im = image.load()

    for x, y in circlePoints:
        try:
            im[x, y] = color
        except IndexError:
            pass


def getBands(im, bandWidth):
    height, width = im.size
    maxDim = min(height, width) 
    center = (width // 2, height // 2)
    allPixelCoords = permutations(range(maxDim), 2)
    
    bands = [[] for band in range(maxDim // bandWidth)]

    for x, y in allPixelCoords:
        d = math.sqrt((x - center[0])**2 + (y - center[1])**2)
        band = int(d / bandWidth)

        bands[band].append((x, y))

    return ([band for band in bands if (len(band) > 0)])



def getColorAverage(rgbIm, coords):
    '''
        Accept an image and list of pixel coordinates.
        Return (R, G, B) tuple of averages pixel value
    '''
    pixs = rgbIm.load()
    targetPixs = [
            pixs[x, y] 
            for x, y in coords 
        ]

    redAvg = sum([pix[0] for pix in targetPixs]) // len(targetPixs)
    greenAvg = sum([pix[1] for pix in targetPixs]) // len(targetPixs)
    blueAvg = sum([pix[2] for pix in targetPixs]) // len(targetPixs)
    return (redAvg, greenAvg, blueAvg)


def analyzePhoto(photoPath, bandWidth=10):

    print('loading photo')
    photo = Image.open(photoPath)  # Open image
    rgbIm = photo.convert('RGB') 

    print('getting bands')
    bands = getBands(rgbIm, bandWidth)

    print('calculating color averages')
    avgs = [getColorAverage(rgbIm, band) for band in bands]

    print('drawing circles')
    [drawCircle(rgbIm, band, avgs[i]) for i, band in enumerate(bands)]
    rgbIm.show()
    photo.show()
    return avgs


def main():
    avgs = analyzePhoto(PHOTO_FILE, 5)

    with open(PHOTO_FILE + '_analysis.csv', 'w') as fp:
        [fp.write("{}, {}, {}, {}\n".format(i, a[0], a[1], a[2])) for i, a in enumerate(avgs)]


if __name__ == '__main__':
    main()
