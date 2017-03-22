from Vinux.ImageHandling.ImageReader import get_image_as_monochrome_Numpy_array, get_image_as_array_of_bools, readImage, improve_monochrome_image_by_pieces
import os
from scipy.misc import imsave

################################################################################
def read_image_and_write(image_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imageFile = os.path.join(dir_path, 'testImageData', image_name)
    print( imageFile )
    tmp = readImage(imageFile)
    f = open(os.path.join(dir_path, 'testImageData' , image_name + '.txt'), 'w')
    f.write( tmp )
    f.close()
    print( tmp.encode('utf-8') )
    print( '\n\n' )
    

################################################################################
def get_monochrome_image(image_name):
    # open the image
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(dir_path, 'testImageData' , image_name)
    # get as monochrome Numpy array
    return get_image_as_monochrome_Numpy_array(image_path)

################################################################################
def save_monochrome_image_and_read(improvedimage_name,ImprovedImage):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    improved_image_file = os.path.join(dir_path, 'testImageData' , improvedimage_name)
    imsave(improved_image_file, ImprovedImage)
    # call the read function
    read_image_and_write(improvedimage_name)    
    
################################################################################
def read_image_as_monochrome_and_write(image_name): 
    monochrome_image = get_monochrome_image(image_name)
    # improve the image
    improved_image = get_image_as_array_of_bools(monochrome_image, 70 )
    # save the improved image and read
    improved_image_name = image_name[:len(image_name)-4] + '_monochrome' + image_name[len(image_name)-4:]
    save_monochrome_image_and_read(improved_image_name, improved_image)
    
    
################################################################################
def read_images():
    read_image_and_write( 'etiquette_3.jpg')
    read_image_and_write( 'testWineLabel_flatEasy.gif')
    read_image_and_write( 'testWineLabel_flat.jpg')
    read_image_and_write( 'testWineLabel.jpg')

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
    read_image_as_monochrome_and_write('testWineLabel_flatEasy.gif')
    read_image_as_monochrome_and_write('testWineLabel.jpg')
    
################################################################################
def read_image_crop_improve_and_write(image_name): 
    monochrome_image = get_monochrome_image(image_name)
    # improve the image
    improved_image = improve_monochrome_image_by_pieces(monochrome_image)
    improved_image = get_image_as_array_of_bools(improved_image, 50)
    # save the improved image and read
    improved_image_name = image_name[:len(image_name)-4] + '_impoved_monochrome' + image_name[len(image_name)-4:]
    save_monochrome_image_and_read(improved_image_name, improved_image)

    
################################################################################
def crop_and_read_images(): 
    read_image_crop_improve_and_write( 'testWineLabel.jpg')
