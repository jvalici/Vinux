from django.test import TestCase
from Vinux.testFiles.TestObjectsLoader import loadExampleObjects


# Create your tests here.
class SetupExampleDataBase(TestCase):

    def test_loading_objects(self):
        loadExampleObjects()
        
        