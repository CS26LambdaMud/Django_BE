# Generated by Django 3.0.3 on 2020-03-04 18:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0006_auto_20200303_2240'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='ITEM', max_length=50)),
                ('player_id', models.IntegerField(default=0)),
                ('room_id', models.IntegerField(default=0)),
            ],
        ),
    ]
