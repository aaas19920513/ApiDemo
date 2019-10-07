from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class UserProfile(AbstractUser):
    """
    用户表，新增字段如下
    """
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )

    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话", help_text="电话号码", unique=True)
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱", unique=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class UserToken(models.Model):

    user = models.OneToOneField(to=UserProfile, on_delete=models.CASCADE, related_name='用户')
    token = models.CharField(max_length=128, null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now=True)

    class Meta:
        verbose_name = "token表"
        verbose_name_plural = verbose_name


class log(models.Model):

    user = models.CharField('用户', max_length=30)
    method = models.CharField('method', max_length=20)
    path = models.CharField('请求路径', max_length=256)
    body = models.TextField('请求体')
    status_code = models.CharField('状态码', max_length=10)
    reason_phrase = models.CharField(max_length=256)
    start_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'logs'

    def __str__(self):
        return '{}--{}--{}'.format(self.user, self.start_time, self.status_code)

class FileBinary(models.Model):
    """
    二进制文件流
    """

    class Meta:
        verbose_name = "二进制文件"
        db_table = "FileBinary"

    name = models.CharField("文件名称", unique=True, null=False, max_length=100)
    body = models.BinaryField("二进制流", null=False)
    size = models.CharField("大小", null=False, max_length=30)