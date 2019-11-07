from django.db import models
from django.contrib.auth.models import User
from partner.models import Menu


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name  = models.CharField(max_length=50, verbose_name='고객이름')

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    address  = models.CharField(max_length=100, verbose_name='고객주소')
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(
        Menu,
        through='OrderItem', #''string으로 모델이름을 적용한이유는 밑에서 불러왔기때문이다.
        through_fields=('order', 'menu'), # through:~를통하여
    )

    def __str__(self):
        return '{}님의 주문내용:{}'.format(self.client, self.items)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu =  models.ForeignKey(Menu, on_delete=models.CASCADE)
    count =  models.PositiveSmallIntegerField(verbose_name='선택갯수')
