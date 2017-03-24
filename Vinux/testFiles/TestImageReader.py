from Vinux.ImageHandling.ImageReader import readImage, improve_monochrome_image_by_pieces
import os
import numpy
from scipy import ndimage
from scipy.misc import imsave

################################################################################
def read_image_and_write(image_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imageFile = os.path.join(dir_path, 'testImageData', image_name)
    print( imageFile )
    tmp = readImage(imageFile)
    f = open(os.path.join(dir_path, 'testImageData' , image_name + '.txt'), 'w', encoding="utf8")
    f.write( tmp )
    f.close()
    print( tmp.encode('utf-8') )
    print( '\n\n' )
    

################################################################################
def crop_improve_and_read_image(image_name): 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(dir_path, 'testImageData' , image_name)

    # improve the image
    improved_image = improve_monochrome_image_by_pieces(image_path)
    
    # save the improved image and read
    improved_image_name = image_name[:len(image_name)-4] + '_improved_monochrome' + image_name[len(image_name)-4:]
    improved_image_file = os.path.join(dir_path, 'testImageData' , improved_image_name)
    imsave(improved_image_file, improved_image)
    # call the read function
    read_image_and_write(improved_image_name) 
   
    
    
################################################################################
def read_images():
    read_image_and_write( 'etiquette_3.jpg')
    read_image_and_write( 'testWineLabel_flatEasy.gif')
    read_image_and_write( 'testWineLabel_flat.jpg')
    read_image_and_write( 'testWineLabel.jpg')

    # The following is just an easy example of the ndimage.label, ndimage.sum calls and the use of a mask to remove some elements of the picture 
    # based on their size
#     a = numpy.zeros((6,6), dtype=numpy.int)
#     a[2:4, 2:4] = 1
#     a[4, 4] = 1
#     a[5, 4] = 1
#     a[:2, :3] = 1
#     a[0, 5] = 1
#     label_im, nb_labels = ndimage.label(a)
#     sizes = ndimage.sum(a, label_im, range(nb_labels + 1))
#     mask_size = sizes < 2
#     remove_pixel = mask_size[label_im]
#     label_im[remove_pixel] = 0
#     a = label_im > 0
    
    # now do the same but improving the image
    crop_improve_and_read_image( 'etiquette_3.jpg')
    crop_improve_and_read_image( 'testWineLabel_flatEasy.gif')
    crop_improve_and_read_image( 'testWineLabel_flat.jpg')
    crop_improve_and_read_image( 'testWineLabel.jpg')
    

    
