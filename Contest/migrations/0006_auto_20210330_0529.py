# Generated by Django 3.1.2 on 2021-03-30 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0005_contest_canjoin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='canjoin',
            field=models.BooleanField(default=True),
        ),
    ]