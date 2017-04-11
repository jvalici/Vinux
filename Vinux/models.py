from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from Vinux.modelsUtils import get_usual_name_from_compagny_name


class WineProducer(models.Model):
    companyName = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    postCode = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    # deduce the usual name from the company name
    def _get_usual_name(self):
        return get_usual_name_from_compagny_name(self.companyName)
    usualName = property(_get_usual_name)
    type = models.CharField(max_length=1,choices=(('v', 'Viticulteur'),('c','Cooperative'),('e','Fabrication effervescents')))
    
class WineProductionArea(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    parentArea = models.ForeignKey('self',blank=True, null=True)
    
class WineAppelation(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    area = models.ForeignKey(WineProductionArea)
    euStatus = models.CharField(max_length=1,choices=(('i', 'IGP'),('a','AOP')))
    isAOC = models.BooleanField()
    
class WineDenomination(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
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
    
