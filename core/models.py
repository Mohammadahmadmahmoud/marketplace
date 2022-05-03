from django.db import models

from re import T
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from customer.models import *
import vendor
from vendor.models import *
from pathlib import Path
from django.core.validators import FileExtensionValidator


class CategoryAds(models.Model):

    title=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255)
    ordering=models.IntegerField(default=0)

    class Meta:
        ordering= ['ordering']
        verbose_name = "CategoryAd"

    def __str__(self):
        return self.title

class SilverPart(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2 ,default=5.00)
    customer = models.ForeignKey(Customer, related_name='silverparts',
                                 blank=True, null= True, on_delete= models.CASCADE)
    user = models.ForeignKey(User, related_name='silverparts',
                                 blank=True, null= True, on_delete= models.CASCADE)
    vat=models.DecimalField(max_digits=5, decimal_places=2, default=0.05)
    amount_vat = models.DecimalField(max_digits=6,decimal_places=2, null=True,blank=True,default=1)
    
    @property
    def get_price(self):
        self.amount_vat = self.price*self.vat
        return self.amount_vat +self.price
        
        
    
   



class FreePart(models.Model):
    free = models.DecimalField(max_digits=6, decimal_places=2)




class Ads(models.Model):
    category=models.ForeignKey(CategoryAds,related_name='ads', on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    titlear = models.CharField(max_length=100)
    url =  models.URLField( blank=True, null=True)
    description = models.TextField(max_length=255)
    descriptionar = models.TextField(max_length=255)
    name=models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,related_name='ads',on_delete=models.CASCADE, blank=True, null=True)
    vendor=models.ForeignKey(Vendor,related_name='ads',on_delete=models.CASCADE, null=True, blank=True )
    customer=models.ForeignKey(Customer,related_name='ads', on_delete=models.CASCADE, blank=True, null=True)
    image=models.ImageField(upload_to='uploadsone/',blank=True,null=True)
    image2=models.ImageField(upload_to='uploadstow/',blank=True,null=True)
    image3=models.ImageField(upload_to='uploadsthree/',blank=True,null=True)
    slug=models.SlugField(max_length=255)
    # price=models.DecimalField(max_digits=6,decimal_places=2)
    thumbnailOne=models.ImageField(upload_to='uploadsone/',blank=True,null=True)
    thumbnailTow=models.ImageField(upload_to='uploadstow/',blank=True,null=True)
    thumbnailThree=models.ImageField(upload_to='uploadsthree/',blank=True,null=True)
    approved = models.BooleanField("Approved", default=False)
    video = models.FileField(upload_to='videos_uploaded',null=True, blank=True,
            validators=[FileExtensionValidator
                        (allowed_extensions=['MOV','avi','mp4','webm','mkv'])])

    class Meta:
        ordering=['-date_added']
        verbose_name = "Ad"
        
    def __str__(self):
        return '%s' % self.user
    
    
    def image_tag(self):
        from django.utils.html import escape
        return u'<img src="%s" />' 
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def get_thumbnailOne(self):
 
        if self.thumbnailOne:
            return self.thumbnailOne.url 

        else:
            if self.image:
                self.thumbnailOne=self.make_thumbnailOne(self.image)
                self.save()

                return self.thumbnailOne.url

            else:
                return 'https://via.placeholder.com/240x180.jpg'


    def get_thumbnailTow(self):
        if self.thumbnailTow:
            return self.thumbnailTow.url

        else:
            if self.image2:
                self.thumbnailTow=self.make_thumbnailTow(self.image2)
                self.save()

                return self.thumbnailTow.url

            else:
                return 'https://via.placeholder.com/240x180.jpg'
    def get_thumbnailThree(self):
        if self.thumbnailThree:
            return self.thumbnailThree.url

        else:
            if self.image3:
                self.thumbnailThree=self.make_thumbnailThree(self.image3)
                self.save()

                return self.thumbnailThree.url

            else:
                return 'https://via.placeholder.com/240x180.jpg'
            
            
    def make_thumbnailOne(self, image,size=(300,200)):
        img=Image.open(image)
        img=img.convert('RGB')
        img.thumbnail(size)

        thumb_io=BytesIO()
        img.save(thumb_io,'JPEG',quality=85)

        thumbnail1=File(thumb_io,name=image.name)

        return thumbnail1

    def make_thumbnailTow(self, image2,size=(300,200)):
        img=Image.open(image2)
        img=img.convert('RGB')
        img.thumbnail(size)

        thumb_io=BytesIO()
        img.save(thumb_io,'JPEG',quality=85)

        thumbnail2=File(thumb_io,name=image2.name)

        return thumbnail2

    def make_thumbnailThree(self, image3,size=(300,200)):
        img=Image.open(image3)
        img=img.convert('RGB')
        img.thumbnail(size)

        thumb_io=BytesIO()
        img.save(thumb_io,'JPEG',quality=85)

        thumbnail3=File(thumb_io,name=image3.name)

        return thumbnail3

