from PIL import Image
#from PIL import ImageEnhance, ImageFilter
import pytesseract
import os
from scipy.misc import imsave
import numpy
from scipy import ndimage

def in_range(the_slice, ranges):
    return any( lower <= (the_slice.stop - the_slice.start) <= upper  for (lower, upper) in ranges)

def get_width_or_length_mask(list_of_objects, width_or_length):
    # width_or_length is 1 or 0
    object_widths_or_length = [ o[width_or_length].stop - o[width_or_length].start for o in list_of_objects ]
    equally_spaced = numpy.linspace(min(object_widths_or_length), max(object_widths_or_length), 100, endpoint=False)
    hist, bin_edges = numpy.histogram(object_widths_or_length, bins=equally_spaced, density=True)
    bin_left_hedges = bin_edges[:len(bin_edges)-1]
    fullHisto = zip(bin_left_hedges, hist)
    fullHistoFiltered = [(x, y) for x, y in fullHisto if y > 0.01]
    bin_left_hedges, hist = zip(*fullHistoFiltered)
    ranges = [(x,x+bin_edges[1]-bin_edges[0]) for x in bin_left_hedges]
    mask_ = [ in_range(o[width_or_length], ranges) for o in list_of_objects]
    mask = numpy.where(mask_,1,0)
    mask = numpy.append([1], mask)
    return mask

def apply_threshold_on_monochrome(imageName, threshold):
    
    """Binarise the image."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imageFileIn = os.path.join(dir_path, imageName)
    image_file = Image.open(imageFileIn)
    image = image_file.convert('L')  # convert image to monochrome
    image = numpy.array(image)
    
    """Apply the threshold"""
    #image = numpy.where(image<=threshold, 0, 255)
    mask = image >= threshold
    label_im, nb_labels = ndimage.label(mask)
    
    # remove small and big elements
    sizes = ndimage.sum(mask, label_im, range(nb_labels + 1))
    small_size_threshold= numpy.percentile(sizes, 10)
    large_size_threshold= numpy.percentile(sizes, 90)
    mask_size = numpy.where((sizes>small_size_threshold) & (sizes<large_size_threshold),1,0)
    remove_pixel = mask_size[label_im]
    # trim the image
    mask[remove_pixel] = False
    image[remove_pixel] = 0
    
    # remove elements with out-layer width and length
    label_im, nb_labels = ndimage.label(mask)
    list_of_objects = ndimage.find_objects(label_im)
    mask_width = get_width_or_length_mask(list_of_objects, 0)
    remove_pixel = mask_width[label_im]
    mask[remove_pixel] = False
    image[remove_pixel] = 0
    mask_length = get_width_or_length_mask(list_of_objects, 1)
    remove_pixel = mask_length[label_im]
    mask[remove_pixel] = False
    image[remove_pixel] = 0
    
    # save the image
    imageFileOut = os.path.join(dir_path, imageName[:len(imageName)-4] + '_trimmed' + imageName[len(imageName)-4:])
    imsave(imageFileOut, image)
    
    
    
    
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
    #readImage( 'etiquette_3.jpg')
    #readImage( 'testWineLabel_flatEasy.gif')
    #readImage( 'testWineLabel_flat.jpg')
    #readImage( 'testWineLabel_short.jpg')
    #readImage( 'testWineLabel.jpg')
    
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #imageFile = os.path.join(dir_path, 'testWineLabel.jpg')
    #im = Image.open( imageFile )
    #im.rotate( -90 )
    #im.save( os.path.join(dir_path, 'testWineLabel_rotated.jpg') )
    #readImage( 'testWineLabel_rotated.jpg')
    
    apply_threshold_on_monochrome('testWineLabel.jpg', 170)
    
    
    