# Generated by Django 3.1.2 on 2021-03-30 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0006_auto_20210330_0529'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='notification',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
