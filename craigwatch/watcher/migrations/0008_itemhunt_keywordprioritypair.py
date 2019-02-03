# Generated by Django 2.1.5 on 2019-01-31 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0007_remove_listing_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemHunt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipcode', models.CharField(max_length=5)),
                ('radius', models.IntegerField(null=True)),
                ('section', models.CharField(default='free', max_length=160)),
                ('minprice', models.FloatField(default=0.0)),
                ('maxprice', models.FloatField(default=float("inf"))),
                ('listing_age', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='KeywordPriorityPair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=220)),
                ('priority', models.IntegerField()),
                ('itemhunt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watcher.ItemHunt')),
            ],
        ),
    ]