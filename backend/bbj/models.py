from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class product_item(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=128)
    category = models.CharField(max_length=128)
    specification = models.CharField(max_length=128)
    img = models.ImageField
    code = models.CharField(max_length=128)



class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    user_tb_token = models.TextField(null=True, blank=True)
    user_jd_token = models.TextField(null=True, blank=True)


class collect_record(models.Model):
    user_profile = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    product_item = models.ForeignKey(product_item, on_delete=models.CASCADE)

