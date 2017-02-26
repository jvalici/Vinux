from PIL import Image
#from PIL import ImageEnhance, ImageFilter
import pytesseract
import os
from scipy.misc import imsave
import numpy
from scipy import ndimage


def in_range(the_slice, ranges):
    return not(any( lower <= (the_slice.stop - the_slice.start) & (the_slice.stop - the_slice.start)<= upper  for (lower, upper) in ranges))

def get_width_or_height_mask(label_im, width_or_heigh):
    # width_or_length is 1 or 0
    list_of_objects = ndimage.find_objects(label_im)
    object_widths_or_heights = [ o[width_or_heigh].stop - o[width_or_heigh].start for o in list_of_objects ]
    last_bucket = numpy.percentile(object_widths_or_heights, 98)
    equally_spaced = numpy.linspace(3, last_bucket, 100)
    buckets = numpy.append([1], equally_spaced)
    hist, bin_edges = numpy.histogram(object_widths_or_heights, bins=buckets)
    bin_left_hedges = bin_edges[:len(bin_edges)-1]
    fullHisto = zip(bin_left_hedges[1:], hist[1:])
    fullHistoFiltered = [(x, y) for x, y in fullHisto if y > 0.01 * len(object_widths_or_heights)]
    bin_left_hedges, hist = zip(*fullHistoFiltered)
    ranges = [(x,x+bin_edges[1]-bin_edges[0]) for x in bin_left_hedges]
    mask = [in_range(o[width_or_heigh], ranges) for o in list_of_objects]
    mask = numpy.append([True], mask)
    return mask

def apply_threshold_on_monochrome(imageName):
    
    """Binarise the image."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imageFileIn = os.path.join(dir_path, imageName)
    image_file = Image.open(imageFileIn)
    image = image_file.convert('L')  # convert image to monochrome
    image = numpy.array(image)
    # get the bit darker than the median
    threshold = numpy.percentile(image, 70)
    
    """Apply threshold and then erosion and propagation to clean it up"""
    mask = image < threshold
    eroded_mask = ndimage.binary_erosion(mask)
    mask = ndimage.binary_propagation(eroded_mask, mask=mask)
    label_im, nb_labels = ndimage.label(mask,[[1,1,1], [1,1,1], [1,1,1]])

    # remove small and big elements
    sizes = ndimage.sum(mask, label_im, range(nb_labels + 1))
    small_size_threshold= max( numpy.percentile(sizes, 50), 100)
    large_size_threshold= min( numpy.percentile(sizes, 100), 10000 )
    mask_size = (sizes<=small_size_threshold) | (sizes>=large_size_threshold)
    remove_pixel = mask_size[label_im]
    
    # remove elements with out-layer width and length
    mask_width = get_width_or_height_mask(label_im, 0)
    remove_pixel = numpy.logical_or( remove_pixel, mask_width[label_im] )
    
    """mask_height= get_width_or_height_mask(label_im, 1)
    remove_pixel = numpy.logical_or( remove_pixel,mask_height[label_im] )"""

    # save the image
    imageFileOut = os.path.join(dir_path, imageName[:len(imageName)-4] + '_trimmed' + imageName[len(imageName)-4:])
    # trim the image
    label_im[remove_pixel] = 0
    image = label_im == 0
    imsave(imageFileOut, image)
    
    
def readImage( imageName ):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imageFile = os.path.join(dir_path, imageName)
    print( imageFile )
    im = Image.open( imageFile )
    tmp = pytesseract.image_to_string(im, lang='fra', config='-psm 1')
    f = open( os.path.join(dir_path, imageName + '.txt' ), 'w')
    f.write( tmp )
    f.close()
    print( tmp.encode('utf-8') )
    print( '\n\n' )


def readImages():
    readImage( 'etiquette_3.jpg')
    readImage( 'testWineLabel_flatEasy.gif')
    readImage( 'testWineLabel_flat.jpg')
    readImage( 'testWineLabel.jpg')


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

    apply_threshold_on_monochrome('testWineLabel_flatEasy.gif')
    readImage( 'testWineLabel_flatEasy_trimmed.gif')
    apply_threshold_on_monochrome('testWineLabel.jpg')
    readImage( 'testWineLabel_trimmed.jpg')


