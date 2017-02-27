from Vinux.ImageHandling.ImageReader import get_image_as_ndarray_of_true_or_false, readImage
import os
from scipy.misc import imsave

def readImageAndWrite(imageName):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imageFile = os.path.join(dir_path, imageName)
    print( imageFile )
    tmp = readImage(imageFile)
    f = open(os.path.join(dir_path, imageName + '.txt'), 'w')
    f.write( tmp )
    f.close()
    print( tmp.encode('utf-8') )
    print( '\n\n' )
    
def readImprovedImageAndWrite(imageName):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imageFileIn = os.path.join(dir_path, imageName)
    improved_image = get_image_as_ndarray_of_true_or_false(imageFileIn)
    # save the image
    improved_image_name = imageName[:len(imageName)-4] + '_trimmed' + imageName[len(imageName)-4:]
    improved_image_file = os.path.join(dir_path, improved_image_name)
    imsave(improved_image_file, improved_image)
    readImageAndWrite(improved_image_name)    
    
def readImages():
    readImageAndWrite( 'etiquette_3.jpg')
    readImageAndWrite( 'testWineLabel_flatEasy.gif')
    readImageAndWrite( 'testWineLabel_flat.jpg')
    readImageAndWrite( 'testWineLabel.jpg')


    # The following is just an easy example of the ndimage.label, ndimage.sum calls and the use of a mask to remove some elements of the picture 
    # based on their size
    """a = numpy.zeros((6,6), dtype=numpy.int)
    a[2:4, 2:4] = 1
    a[4, 4] = 1
    a[5, 4] = 1
    a[:2, :3] = 1
    a[0, 5] = 1
    label_im, nb_labels = ndimage.label(a)
    sizes = ndimage.sum(a, label_im, range(nb_labels + 1))
    mask_size = sizes < 2
    remove_pixel = mask_size[label_im]
    label_im[remove_pixel] = 0
    a = label_im > 0"""
    readImprovedImageAndWrite('testWineLabel_flatEasy.gif')
    readImprovedImageAndWrite('testWineLabel.jpg')
