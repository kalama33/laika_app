# Generated by Django 4.2.7 on 2024-01-15 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laika', '0006_alter_laikaprofileuser_image_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pet',
            name='neutered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pet',
            name='sex',
            field=models.CharField(choices=[('Female', 'Female'), ('Male', 'Male'), ('Other', 'Other')], default='None', max_length=10),
        ),
        migrations.AddField(
            model_name='pet',
            name='special_needs',
            field=models.TextField(blank=True, default='None', null=True),
        ),
        migrations.AddField(
            model_name='pet',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
