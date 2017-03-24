from PIL import Image
#from PIL import ImageEnhance, ImageFilter
import pytesseract
import numpy
from scipy import ndimage
from math import floor
from skimage import filters


################################################################################
import os
from scipy.misc import imsave
# for tests only
def save_im(image, name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    improved_image_file = os.path.join(dir_path, name )
    imsave(improved_image_file, image)

################################################################################
def filter_small_objects(list_of_objects, do_first_dim, percentage_threshold):
    index = 0 if do_first_dim else 1
    sizes = [ o[index].stop - o[index].start for o in list_of_objects ]
    size_threshold = numpy.percentile(sizes, percentage_threshold)
    return sizes < size_threshold
    
################################################################################
def improve_mask_and_inverse(mask):
    # Apply threshold and then erosion and propagation to clean it up
    eroded_mask  = ndimage.binary_erosion(mask, iterations = 1)
    mask = ndimage.binary_propagation(eroded_mask, mask = mask)
    
    
    monochrome_image = numpy.where( mask, 255, 0 )
    monochrome_image = ndimage.filters.gaussian_filter(monochrome_image, sigma = 1)
    mask = monochrome_image > 100
    
    
    # make everything a bit thicker
    mask = ndimage.binary_dilation(mask, iterations = 1)

    # get label
    struct = [[0,1,0], [1,1,1], [0,1,0]]
    mask_labels, nb_labels = ndimage.label(mask,struct)
       
#     import matplotlib.pyplot as plt
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     improved_image_file = os.path.join(dir_path,'blobs.png' )
#     plt.imsave(improved_image_file, mask_labels)
    
    # if there are few item, return them all, else filer those which are either long or large
    target_number = 100
    if nb_labels > target_number:
        list_of_objects = ndimage.find_objects(mask_labels)
        percentile_to_keep_target = 100 * ( 1 - target_number / nb_labels )
        narrow_objects = filter_small_objects(list_of_objects, True, percentile_to_keep_target )
        short_objects = filter_small_objects(list_of_objects, False, percentile_to_keep_target )
        object_to_remove = numpy.logical_and(narrow_objects, short_objects)
        very_larges_objects = numpy.logical_not(filter_small_objects(list_of_objects, True, 99.5 ))
        object_to_remove = numpy.logical_or(object_to_remove, very_larges_objects)
        very_long_objects = numpy.logical_not(filter_small_objects(list_of_objects, False, 99.5 ))
        object_to_remove = numpy.logical_or(object_to_remove, very_long_objects)

        # append False for the label zero 
        object_to_remove = numpy.append([False], object_to_remove)
        remove_pixel = object_to_remove[mask_labels]
        mask_labels[remove_pixel] = 0
        #inverse
        image = mask_labels == 0
    else:   
        image = numpy.logical_not(mask)
    return image

################################################################################
def get_mean_around_point(array, x, y, half_size):
    x_max = array.shape[0]-1
    y_max = array.shape[1]-1
    return numpy.mean(array[max(0,x-half_size):min(x+half_size,x_max),max(0,y-half_size):min(y+half_size,y_max)]) 

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
def identify_border_of_the_pale_area(monochrome_image, do_first_dim, do_dim_start):
    # get the size of the main dimension and the size of the other dimension
    main_dim_size = monochrome_image.shape[0 if do_first_dim else 1]
    other_dim_size = monochrome_image.shape[1 if do_first_dim else 0]
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
    while any_middle_is_lighter_than_average_of_sides(monochrome_image, line1, line2, line3, do_first_dim, do_dim_start, inner_end ):
        inner_end = inner_end + increment

    # return the last valid value of the middle
    inner_end = inner_end - increment
    if do_dim_start:
        return floor( inner_end / 2 )
    else:
        return floor( ( main_dim_size - 1 + inner_end ) / 2 )

                 
################################################################################

def get_mask_by_pieces(array, treat_array, number_of_units, diff_max):
    mask = numpy.ndarray( array.shape, dtype='bool_')
    dim1_unit_size = floor(array.shape[0]/ number_of_units)
    dim2_unit_size = floor(array.shape[1]/ number_of_units)
    threshold = floor(numpy.mean(array))
    for i in range(number_of_units):
        for j in range(number_of_units):
            dim1_start =  i * dim1_unit_size
            dim1_end = ( i + 1 ) * dim1_unit_size if i < (number_of_units - 1) else array.shape[0]
            dim2_start = j * dim2_unit_size
            dim2_end = ( j + 1 ) * dim2_unit_size if j < (number_of_units - 1) else array.shape[1]
            sub_array = array[dim1_start:dim1_end,dim2_start:dim2_end]
            min_sub_array = numpy.min(sub_array)
            max_sub_array = numpy.max(sub_array)
            diff = max_sub_array - min_sub_array
            if diff < diff_max:
                sub_mask = True if max_sub_array < threshold else False
            else:
                if treat_array:
                    sub_mask = get_mask_by_pieces(sub_array, False, 8, floor(0.5*diff_max ) )
                else:
                    if dim1_unit_size * dim2_unit_size < 20:
                        val = min_sub_array + 0.5* diff
                    else:
                        val = filters.threshold_otsu(sub_array)
                    sub_mask = sub_array <= val + 1
            mask[dim1_start:dim1_end,dim2_start:dim2_end] = sub_mask
            
    return mask


################################################################################
def improve_monochrome_image_by_pieces(image_path):
    
    # get image as monochrome (open and convert)
    image_file = Image.open(image_path)
    monochrome_image = numpy.array( image_file.convert('L') )
    # save_im( monochrome_image,'monochrom.jpg' )
    if monochrome_image.shape[0] * monochrome_image.shape[1] < 100000:
        return image_file
    
    # identify the label based on the assumption that it is pale with darker writing
    first_dim_start_index = identify_border_of_the_pale_area(monochrome_image, True, True)
    first_dim_end_index = identify_border_of_the_pale_area(monochrome_image, True, False )
    second_dim_start_index = identify_border_of_the_pale_area(monochrome_image, False, True)
    second_dim_end_index = identify_border_of_the_pale_area(monochrome_image, False, False)
    
    # crop the array
    monochrome_image = monochrome_image[first_dim_start_index:first_dim_end_index, second_dim_start_index:second_dim_end_index]
    # save_im( monochrome_image,'croped.jpg' )
    
    # apply a smoothing filter
    monochrome_image = ndimage.filters.gaussian_filter(monochrome_image, sigma = 1)
    # save_im( monochrome_image,'filtered.jpg' )
    
    # try to improve the contrast
    mask = get_mask_by_pieces(monochrome_image, True, 10, 60)
    # save_im( mask,'mask.jpg' )
    
    # try to improve the mask
    image = improve_mask_and_inverse(mask)
    # save_im( image,'improved_image.jpg' )
    
    return image


################################################################################
def readImage(image_path):
    
    im = Image.open( image_path )
    res = pytesseract.image_to_string(im, lang='fra', config='-psm 1')
    res = res.replace('\\', 'I')
    res = res.replace('lL', 'IL')
    res = res.replace('\'', '')
    # case sensitive stuff
    res = res.lower()
    res = res.replace('appellanon', 'appellation')
    return res


