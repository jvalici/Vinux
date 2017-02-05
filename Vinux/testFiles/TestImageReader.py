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
    tmp = pytesseract.image_to_string(im, lang='fra',config='-psm 3')
    f = open( os.path.join(dir_path, imageName + '.txt' ), 'w')
    f.write( tmp )
    f.close()
    print( tmp.encode('utf-8') )
    print( '\n\n' )
    

def readImages():
    readImage( 'etiquette_3.jpg')
    readImage( 'testWineLabel_flatEasy.gif')
    readImage( 'testWineLabel_flat.jpg')
    readImage( 'testWineLabel_short.jpg')
    readImage( 'testWineLabel.jpg')
    
    