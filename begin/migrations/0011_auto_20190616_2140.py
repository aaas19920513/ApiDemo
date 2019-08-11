# Generated by Django 2.1.7 on 2019-06-16 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('begin', '0010_auto_20190616_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='step',
            name='step_info',
        ),
        migrations.AddField(
            model_name='step',
            name='extract',
            field=models.TextField(default=1, verbose_name='提取变量表达式'),
        ),
        migrations.AddField(
            model_name='step',
            name='validate',
            field=models.TextField(default=1, max_length=256, verbose_name='断言'),
        ),
        migrations.AddField(
            model_name='step',
            name='variables',
            field=models.TextField(default=1, verbose_name='变量'),
        ),
    ]
