from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=128)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.book_name
