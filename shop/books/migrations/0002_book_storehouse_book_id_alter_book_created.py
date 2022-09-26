# Generated by Django 4.1.1 on 2022-09-24 19:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='storehouse_book_id',
            field=models.CharField(help_text='Book id from storehouse', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='created',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
