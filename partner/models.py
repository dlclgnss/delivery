from django.db import models
from django.contrib.auth.models import User


class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name  = models.CharField(max_length=50, verbose_name='업체명')
    contact = models.CharField(max_length=50, verbose_name='연락처')
    address = models.CharField(max_length=200, verbose_name='주소')
    description = models.TextField(verbose_name='상세소개')

    def __str__(self):
        return self.name


class Menu(models.Model):
    KOREANFOOD = 'KF'
    JAPANESEFOOD = 'JF'
    CHINESFOOD = 'CF'
    ITALIANFOOD ='IF'
    FRENCHFOOD ='FF'
    THAIFOOD ='TF'
    VIETNAMESEFOOD ='VF'

    CATEGORY_CHOICES = (
        (KOREANFOOD, "Korean_Food"),
        (JAPANESEFOOD, "Japanese_Food"),
        (CHINESFOOD, "Chines_Food "),
        (ITALIANFOOD, "Italian_Food"),
        (FRENCHFOOD, "French_Food"),
        (THAIFOOD, "Thai_Food"),
        (VIETNAMESEFOOD, "Vietnamese_Food"),
    )

    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='메뉴사진') # 이미지필드를 사용하기 위해선 pip install Pillow 설치필요
    name = models.CharField(max_length=50, verbose_name='메뉴이름')
    price = models.PositiveIntegerField(verbose_name='메뉴가격')# 가격이므로 양수값을 취득
    category = models.CharField(
        max_length=2,
        choices = CATEGORY_CHOICES,
        default= KOREANFOOD,
    )

    def __str__(self):
        return '{}:{}'.format(self.partner,self.name)
