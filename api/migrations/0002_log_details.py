# Generated by Django 2.2.4 on 2019-11-02 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='details',
            field=models.CharField(default='teste', max_length=200),
            preserve_default=False,
        ),
    ]
