# Generated by Django 4.2.9 on 2024-05-08 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_update_on_article_updated_on_article_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='header',
            field=models.ImageField(upload_to='images/'),
        ),
    ]