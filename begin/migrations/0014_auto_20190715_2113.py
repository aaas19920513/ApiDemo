# Generated by Django 2.1.7 on 2019-07-15 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('begin', '0013_classify'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='api',
            options={'ordering': ['id'], 'verbose_name': '接口表', 'verbose_name_plural': '接口表'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='label',
        ),
        migrations.AlterField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, help_text='父目录', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='begin.Category', verbose_name='父类目级别'),
        ),
    ]