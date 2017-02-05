from PIL import Image
#from PIL import ImageEnhance, ImageFilter
import pytesseract
import os 

def readImage( imageName ):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imageFile = os.path.join(dir_path, imageName)
    print( imageFile )
    im = Image.open( imageFile )
    #im = im.filter(ImageFilter.MedianFilter())
    #enhancer = ImageEnhance.Contrast(im)
    #im = enhancer.enhance(2)
    #im = im.convert('1')
    tmp = pytesseract.image_to_string(im, lang='fra',config='0')
    print( tmp.encode('utf-8') )
    

def readImages():
    readImage( 'testWineLabel_short.jpg')
    readImage( 'testWineLabel.jpg')
    
    