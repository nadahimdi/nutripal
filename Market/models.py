from django.db import models
from django.conf import settings
# Create your models here.
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)
class Category(models.Model):
    name= models.CharField(max_length=50,db_index=True)
    slug = models.SlugField(max_length=50,db_index=True)

    class Meta :
        verbose_name_plural="Categories"

    def __str__(self):
          return self.name
    

class Product(models.Model):
     category=models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)
     created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='product_creator')
     title=models.CharField(max_length=80)
     author=models.CharField(max_length=255,default='admin')
     description=models.TextField(blank=True)
     image=models.ImageField(upload_to='images/', default='images/default.jpg')
     slug=models.SlugField(max_length=89)
     price=models.DecimalField(max_digits=4,decimal_places=2)
     in_stock=models.BooleanField(default=True)
     is_active=models.BooleanField(default=True)
     created= models.DateTimeField(auto_now_add=True)
     updated= models.DateTimeField(auto_now_add=True)
     products = ProductManager()
     objects = models.Manager()

    
    
    
     class Meta:
          verbose_name_plural='Products'
          ordering =('-created',)


     def __str__(self):
          return self.title

