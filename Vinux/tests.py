from django.test import TestCase
from Vinux.testFiles.TestObjectsLoader import load_example_objects
from Vinux.testFiles.TestImageReader import read_images

# Create your tests here.
class SetupExampleDataBase(TestCase):

    def test_loading_objects(self):
        load_example_objects()
          
    def test_read_image(self):
        read_images()
        
