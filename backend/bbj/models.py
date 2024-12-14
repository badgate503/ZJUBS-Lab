from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class product_item(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.TextField()
    product_keyword = models.TextField()
    category = models.TextField()
    specification = models.TextField()
    price = models.IntegerField()
    link = models.TextField()
    fromwhich=models.CharField(max_length=10, default="none")
    img = models.TextField()

class product_keyword(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    keyword_name = models.TextField()
    update_time = models.DateTimeField(auto_now=True)
    minPrice = models.IntegerField()
    maxPrice = models.IntegerField()
    TBavgPrice = models.FloatField()
    JDavgPrice = models.FloatField()
    TBcount = models.IntegerField()
    JDcount = models.IntegerField()

class product_keyword_general(models.Model):
    keyword_name = models.TextField()
    latest_keyword_info = models.ForeignKey(product_keyword, on_delete=models.CASCADE)
    lowest = models.IntegerField()
    lowest_link = models.TextField()



class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    user_tb_token = models.TextField(null=True, blank=True)
    user_jd_token = models.TextField(null=True, blank=True)


class collect_record(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    product_keyword = models.TextField(null=False, blank=False)
    need_notify = models.BooleanField()