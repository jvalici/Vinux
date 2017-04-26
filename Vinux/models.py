from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from Vinux.modelsUtils import get_usual_name_from_compagny_name, remove_special_chars


class WineProducer(models.Model):
    
    @classmethod
    def create(cls, inputName, country, postCode, city, producerType):
        companyName = get_usual_name_from_compagny_name(inputName)
        searchName = remove_special_chars(companyName)
        producer = cls( companyName=companyName, searchName=searchName, country=country, postCode=postCode, city=city, producerType=producerType)
        return producer

    companyName = models.CharField(max_length=200)
    searchName = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    postCode = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    producerType = models.CharField(max_length=1,choices=(('v', 'Viticulteur'),('c','Cooperative'),('e','Fabrication effervescents')))
    
class WineProductionArea(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    parentArea = models.ForeignKey('self',blank=True, null=True)
    
class WineAppelation(models.Model):
    name = models.CharField(max_length=200, unique=True)
    area = models.ForeignKey(WineProductionArea)
    euStatus = models.CharField(max_length=1,choices=(('i', 'IGP'),('a','AOP')))
    isAOC = models.BooleanField()
    
class WineDenomination(models.Model):
    
    @classmethod
    def create(cls, name, appelation):
        searchName = remove_special_chars(name)
        denom = cls( name=name, searchName=searchName, appelation=appelation)
        return denom
    
    name = models.CharField(max_length=200, unique=True)
    searchName = models.CharField(max_length=200, unique=True)
    appelation = models.ForeignKey(WineAppelation)
    
class WineBottle(models.Model):
    producer = models.ForeignKey(WineProducer)
    denomination = models.ForeignKey(WineDenomination)
    name = models.CharField(max_length=200,blank=True, null=True)
    vintage = models.PositiveSmallIntegerField( validators=[MinValueValidator(1900), MaxValueValidator(2100)] )
    
class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
class CommentImage(models.Model):
    comment = models.ForeignKey(Comment)
    image = models.ImageField(upload_to='images_from_clients')
    caption = models.TextField(blank=True, null=True)

class BottleUserReview(models.Model):
    mark = models.PositiveSmallIntegerField( validators=[MinValueValidator(0), MaxValueValidator(20)] )
    pairing = models.TextField()
    comment = models.ForeignKey(Comment)
    
    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.comment.content_type.__class__.__name__ != 'WineBottle':
            raise 'BottleUserReview only comment wine bottle'
    
class BottleWebReview(models.Model):
    bottle = models.ForeignKey(WineBottle)
    link = models.URLField()

class WineCellar(models.Model):
    owner = models.ForeignKey(User)
    
class StoredWineBottle(models.Model):
    vineCellar = models.ForeignKey(WineCellar)
    bottle = models.ForeignKey(WineBottle)
    priceIn = models.DecimalField(decimal_places=2, max_digits=7,  validators=[MinValueValidator(0)])
    
