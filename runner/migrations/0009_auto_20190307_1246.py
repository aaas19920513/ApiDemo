# Generated by Django 2.1.7 on 2019-03-07 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0008_auto_20190307_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='config', to='runner.Project'),
        ),
        migrations.AlterField(
            model_name='variables',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variables', to='runner.Project'),
        ),
    ]
