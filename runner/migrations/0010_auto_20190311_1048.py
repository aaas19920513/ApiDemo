# Generated by Django 2.1.7 on 2019-03-11 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0009_auto_20190307_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casestep',
            name='method',
            field=models.IntegerField(choices=[(1, 'post'), (2, 'get'), (3, 'put'), (4, 'delete')], default=1, verbose_name='请求方式'),
        ),
        migrations.AlterField(
            model_name='config',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='环境名称'),
        ),
        migrations.AlterField(
            model_name='variables',
            name='key',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]