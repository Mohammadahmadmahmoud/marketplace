from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models
from vendor.models import Vendor
from django.db import router, transaction


class Category(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255)
    ordering=models.IntegerField(default=0)

    class Meta:
        ordering= ['ordering']

    def __str__(self):
        return self.title

class Product(models.Model):
    category=models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE,blank=True, null=True)
    vendor=models.ForeignKey(Vendor,related_name='products',on_delete=models.CASCADE,null=True )
    title=models.CharField(max_length=255)
    slug=models.CharField(max_length=255)
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    date_added=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='uploads/',blank=True,null=True)
    thumbnail=models.ImageField(upload_to='uploads/',blank=True,null=True)
    VAT=models.DecimalField(max_digits=5, decimal_places=2, default=0.05)
    amount_vat = models.DecimalField(max_digits=6,decimal_places=2, null=True)
    aprroved = models.BooleanField(default=False)


    class Meta:
        ordering=['-date_added']

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        self.amount_vat = self.price*self.VAT
        return self.amount_vat +self.price
    

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url

        else:
            if self.image:
                self.thumbnail=self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url

            else:
                return 'https://via.placeholder.com/240x180.jpg'

    def make_thumbnail(self, image,size=(300,200)):
        img=Image.open(image)
        img=img.convert('RGB')
        img.thumbnail(size)

        thumb_io=BytesIO()
        img.save(thumb_io,'JPEG',quality=85)

        thumbnail=File(thumb_io,name=image.name)

        return thumbnail


def clear_cache(the_cache):
    the_cache.clear()
    # commit the transaction
    db = router.db_for_write(the_cache.cache_model_class)
    transaction.commit_unless_managed(using=db)




class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
