from django.test import TestCase
from Vinux.testFiles.TestObjectsLoader import loadExampleObjects
from Vinux.testFiles.TestImageReader import readImages

# Create your tests here.
class SetupExampleDataBase(TestCase):

    def test_loading_objects(self):
        loadExampleObjects()
        
    def test_read_image(self):
        readImages()
