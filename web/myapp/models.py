from sqlite3 import IntegrityError
from unicodedata import name
from django.db import models
from datetime import datetime

from django.forms import EmailField

class myrecipe(models.Model):
    Ingredients = models.CharField(max_length=32)
    addtime=models.DateTimeField(default=datetime.now)

# class Meta:
#     db_table = "myrecipe"  # 指定真实表名
# Create your models here.
class therecipes(models.Model):
    Dname = models.CharField(max_length=32)
    gongyi = models.CharField(max_length=32)
    flavor = models.CharField(max_length=32)
    zuofa = models.TextField()
    Ingre = models.TextField(default=None)
    

    class Meta:
        db_table = "therecipes"

class filterrecipe(models.Model):
    Dname = models.CharField(max_length=32)
    gongyi = models.CharField(max_length=32)
    flavor = models.CharField(max_length=32)
    zuofa = models.TextField()
    Ingre = models.TextField(default=None)
    class Meta:
        db_table = "filterrecipes"

class filterrecipe2(models.Model):
    Dname = models.CharField(max_length=32)
    gongyi = models.CharField(max_length=32)
    flavor = models.CharField(max_length=32)
    zuofa = models.TextField()
    Ingre = models.TextField(default=None)
    class Meta:
        db_table = "filterrecipes2"

class flavor(models.Model):
    
    flavor = models.CharField(max_length=32)
    
    class Meta:
        db_table = "flavor"

class user(models.Model):
    Uname = models.CharField(max_length=32)
    Email = models.CharField(max_length=32)
    password_hash = models.CharField(max_length=100)#密码
    password_salt = models.CharField(max_length=50)    #密码干扰值
    status = models.IntegerField(default=1)
    signdate = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)
    class Meta:
        db_table = "user"

    def toDict(self):
        return {'id':self.id,'Uname':self.Uname,'Email':self.Email, 'password_hash':self.password_hash,'password_salt':self.password_salt,'status':self.status,'signdate':self.signdate.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

class Post(models.Model):
    name = models.CharField(max_length=32)
    time = models.DateTimeField()
    comment = models.TextField()

    class Meta:
        db_table = 'pinglun'


class coments(models.Model):
    name = models.CharField('name', max_length=100)
    com = models.TextField('留言')
    To = models.ForeignKey(to=therecipes, on_delete=models.NOT_PROVIDED, related_name='comen')
    tim = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.name

class det(models.Model):
    Dname = models.CharField(max_length=32)
    gongyi = models.CharField(max_length=32)
    flavor = models.CharField(max_length=32)
    zuofa = models.TextField()
    Ingre = models.TextField(default=None)
    class Meta:
        db_table = "filterrecipes2"
    
    class Meta:
        db_table = "det"