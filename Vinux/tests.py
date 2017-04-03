from django.test import TestCase
from Vinux.testFiles.TestObjectsLoader import load_example_objects
from Vinux.testFiles.TestImageReader import read_images
from DataCollecting.InfoGreffeDotFr import browse_infogreffe_dot_fr
from DataCollecting.InaoDotGouvDotFr import browse_inao_dot_gouv_dot_fr, clean_denominations
from DataCollecting.Appelations import complete_appelations

# Create your tests here.
class SetupExampleDataBase(TestCase):

    def test_loading_objects(self):
        load_example_objects()
            
    def test_read_image(self):
        read_images()
        
#     # only to collect the data  
#    def test_read_urls(self):
#       browse_infogreffe_dot_fr()
#       browse_inao_dot_gouv_dot_fr()
#       clean_denominations()
#       complete_appelations()