# Generated by Django 3.2.5 on 2021-07-19 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210719_0400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='bot',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='discrimination',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='inappropriate',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='message',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='sexual',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
