from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    """
    用户表，新增字段如下
    """
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )
    # 用户注册时我们要新建user_profile 但是我们只有手机号
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话", help_text="电话号码")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class UserInfo(models.Model):

    right_chioce = (
        (1, "member"),
        (2, "vip"),
        (3, "svip")
    )
    username = models.CharField(max_length=30, null=False, blank=False, verbose_name="姓名")
    password = models.CharField(max_length=30, null=False, blank=False, verbose_name="密码")
    type = models.SmallIntegerField(choices=right_chioce, default=1, verbose_name="会员等级")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class UserToken(models.Model):

    user = models.OneToOneField(to=UserInfo, on_delete=models.CASCADE, related_name='用户')
    token = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = "token表"
        verbose_name_plural = verbose_name
