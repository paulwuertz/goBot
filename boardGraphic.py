from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

def drawBoard(string, size, lastXY=None):
    woodColor, whiteStone, blackStone = (255,202,40), (0xec,0xef,0xf1), (0x00,0x00,0x00)
    im = Image.new('RGB', (60*size+1,60*size+1), woodColor)
    dr = ImageDraw.Draw(im)
    fnt = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeMonoBold.otf", 24)
    fnt.size=30
    for i in range(size**2):
        x, y, xPix, yPix =  (i%size), (i//size), (i%size)*60+30, (i//size)*60+30
        if x!=size-1 and y!=size-1:
            dr.rectangle(((xPix, yPix),(xPix+60,yPix+60)), fill=woodColor, outline = "black")
        if x==0: dr.text((1,yPix-10), "%2d" % y, (0, 0, 0, 0), font=fnt)
        if y==0: dr.text((xPix-10,60*size-30), str("ABCDEFGHIJKLMNOPQRS"[x]), (0, 0, 0, 0), font=fnt)
        if lastXY and lastXY[0]==x and lastXY[1]==y:
            dr.ellipse( ((xPix-35, yPix-35),(xPix+35,yPix+35)), fill=(40,192,92), outline = "black")
        if string[i]!='0':
            dr.ellipse( ((xPix-30, yPix-30),(xPix+30,yPix+30)), fill=whiteStone if string[i]=='1' else blackStone, outline = "black")
    return im

def goBoardPicture(boardString, lastXY=None):
    bio = BytesIO()
    drawBoard(boardString, 19, lastXY).save(bio, 'JPEG')
    bio.seek(0)
    return bio
