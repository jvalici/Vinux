from PIL import Image
#from PIL import ImageEnhance, ImageFilter
import pytesseract
import numpy
from scipy import ndimage
from math import floor

################################################################################
def in_range(one_label, do_first_dim, ranges, other_dim_size):
    along_the_do_first_dim = one_label[0 if do_first_dim else 1]
    is_not_in_range = not(any( lower <= (along_the_do_first_dim.stop - along_the_do_first_dim.start) & (along_the_do_first_dim.stop - along_the_do_first_dim.start)<= upper  for (lower, upper) in ranges))
    along_the_other_dim = one_label[1 if do_first_dim else 0]
    is_thiner_than_other_dim_size = ( along_the_other_dim.stop - along_the_other_dim.start ) < other_dim_size
    return is_not_in_range and is_thiner_than_other_dim_size

################################################################################
# this get rid of the highest columns (the 0.01% highest and thiner than 1/20 of the picture) and the longest
# lines (the 0.01% longest and thiner than 1/20 of the picture) 
def get_mask_for_tall_objects_along_this_dim(label_im, do_first_dim):
    # width_or_length is 1 or 0
    # get the histogram
    list_of_objects = ndimage.find_objects(label_im)
    index = 0 if do_first_dim else 1
    object_widths_or_heights = [ o[index].stop - o[index].start for o in list_of_objects ]
    last_bucket = numpy.percentile(object_widths_or_heights, 98)
    equally_spaced = numpy.linspace(3, last_bucket, 100)
    buckets = numpy.append([1], equally_spaced)
    hist, bin_edges = numpy.histogram(object_widths_or_heights, bins=buckets)
    bin_left_hedges = bin_edges[:len(bin_edges)-1]
    # get the bucket with more than 1% of the objects
    fullHisto = zip(bin_left_hedges[1:], hist[1:])
    fullHistoFiltered = [(x, y) for x, y in fullHisto if y > 0.01 * len(object_widths_or_heights)]
    bin_left_hedges, hist = zip(*fullHistoFiltered)
    ranges = [(x,x+bin_edges[1]-bin_edges[0]) for x in bin_left_hedges]
    # get the a twentieth of the size on the other dimension
    a_twentieth = label_im.shape[1 if do_first_dim else 0]/20
    mask = [in_range(o, not(do_first_dim), ranges, a_twentieth) for o in list_of_objects]
    mask = numpy.append([True], mask)
    return mask

################################################################################
def get_image_as_monochrome_Numpy_array(image_path):
    """Binarise the image."""
    image_file = Image.open(image_path)
    # convert image to monochrome
    monochromeImage = image_file.convert('L') 
    return numpy.array(monochromeImage)
    
################################################################################
def get_image_as_array_of_bools(monochrome_image, threshold_percentage):
    
    # get the bit darker than the median
    threshold = numpy.percentile(monochrome_image, threshold_percentage)
    
    """Apply threshold and then erosion and propagation to clean it up"""
    mask = monochrome_image < threshold
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
    mask_width = get_mask_for_tall_objects_along_this_dim(label_im, True)
    remove_pixel = numpy.logical_or( remove_pixel, mask_width[label_im] )
    
    """mask_height= get_mask_for_tall_objects_along_this_dim(label_im, False)
    remove_pixel = numpy.logical_or( remove_pixel,mask_height[label_im] )"""
   
    # trim the image
    label_im[remove_pixel] = 0
    image = label_im == 0
    return image

################################################################################
def get_mean_around_point(array, x, y, half_size):
    x_max = array.shape[0]-1
    y_max = array.shape[1]-1
    return numpy.mean(array[max(0,x-half_size):min(x+half_size,x_max),max(0,y-half_size):min(y+half_size,y_max),]) 

################################################################################
# 
def indicate_when_middle_lighter_than_average_of_sides( array, line, do_first_dim, do_dim_start, inner_end ):
    dim_length = array.shape[0 if do_first_dim else 1]
    half_size_of_square_where_we_conside_the_average = max( floor( dim_length / 200 ), 10 )
    if do_dim_start:
        small_index_end = 0
        middle = floor(inner_end / 2)
        big_index_end = inner_end
    else:
        small_index_end = inner_end
        middle = floor( (dim_length - 1 + inner_end ) / 2)
        big_index_end = dim_length - 1
    if do_first_dim:
        side1_dot = get_mean_around_point( array, small_index_end, line, half_size_of_square_where_we_conside_the_average)
        middle_dot = get_mean_around_point( array, middle, line, half_size_of_square_where_we_conside_the_average)
        side2_dot = get_mean_around_point( array, big_index_end, line, half_size_of_square_where_we_conside_the_average)
    else:
        side1_dot = get_mean_around_point( array, line, small_index_end, half_size_of_square_where_we_conside_the_average)
        middle_dot = get_mean_around_point( array, line, middle, half_size_of_square_where_we_conside_the_average)
        side2_dot = get_mean_around_point( array, line, big_index_end, half_size_of_square_where_we_conside_the_average)
    average_of_average = 0.5 * ( side1_dot + side2_dot)
    safty_ = 0.8
    return middle_dot > ( safty_ * average_of_average )

################################################################################
# 
def any_middle_is_lighter_than_average_of_sides(array, line1, line2, line3, do_first_dim, do_dim_start, inner_end):
    dim_length = array.shape[0 if do_first_dim else 1]
    if not( inner_end > 0 and inner_end < dim_length - 1 ):
        return False
    tmp1 = indicate_when_middle_lighter_than_average_of_sides(array, line1, do_first_dim, do_dim_start, inner_end )
    tmp2 = indicate_when_middle_lighter_than_average_of_sides(array, line2, do_first_dim, do_dim_start, inner_end )
    tmp3 = indicate_when_middle_lighter_than_average_of_sides(array, line3, do_first_dim, do_dim_start, inner_end )
    return tmp1 or tmp2 or tmp3
        
    
################################################################################
# 
def identify_border_of_the_pale_area(monochromeArray, do_first_dim, do_dim_start):
    # get the size of the main dimension and the size of the other dimension
    main_dim_size = monochromeArray.shape[0 if do_first_dim else 1]
    other_dim_size = monochromeArray.shape[1 if do_first_dim else 0]
    # get three lines on the main dimension. Those lines are identified with index on the other dimension.
    # we take relatively central lines (1/3, 1/2n and 2/3)
    line1 = floor(other_dim_size / 3)
    line2 = floor(other_dim_size / 2)
    line3 = floor(2 * other_dim_size / 3)
    # We look at the segment on each line. Each segment has one end on the border of the array and the other end inside the array
    # The inner end is initialised at the middle of the array and progressively move it toward the border until the middle of the 
    # segment is no longer in a pale area.
    inner_end = floor( main_dim_size / 2 )
    # when the border side is at the beginning, we move the inner end toward the beginning and reversely
    if do_dim_start:
        increment = - floor(main_dim_size / 100)
    else:
        increment = floor(main_dim_size / 100)
    # loop until the middle is in the pale area
    while any_middle_is_lighter_than_average_of_sides(monochromeArray, line1, line2, line3, do_first_dim, do_dim_start, inner_end ):
        inner_end = inner_end + increment

    # return the last valid value of the middle
    inner_end = inner_end - increment
    if do_dim_start:
        return floor( inner_end / 2 )
    else:
        return floor( ( main_dim_size - 1 + inner_end ) / 2 )

################################################################################
def increase_the_contrast_by_pieces(monochrome_image):
    return monochrome_image

################################################################################
def improve_monochrome_image_by_pieces(monochrome_image):
    # identify the label based on the assumption that it is pale with darker writing
    first_dim_start_index = identify_border_of_the_pale_area(monochrome_image, True, True)
    first_dim_end_index = identify_border_of_the_pale_area(monochrome_image, True, False )
    second_dim_start_index = identify_border_of_the_pale_area(monochrome_image, False, True)
    second_dim_end_index = identify_border_of_the_pale_area(monochrome_image, False, False)
    # crop the array
    monochrome_image = monochrome_image[first_dim_start_index:first_dim_end_index, second_dim_start_index:second_dim_end_index]
    # try to improve the contrast
    monochrome_image = increase_the_contrast_by_pieces(monochrome_image)
    return monochrome_image


################################################################################
def readImage(image_path):
    im = Image.open( image_path )
    return pytesseract.image_to_string(im, lang='fra', config='-psm 1')


