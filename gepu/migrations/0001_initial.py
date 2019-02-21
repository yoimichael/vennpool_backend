# Generated by Django 2.1.7 on 2019-02-20 22:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid

def create_user(apps,schema_editor):
    User = apps.get_model('gepu_user','User')
    User(1,"Mi").save()

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=20)),
                ('to_addr', models.TextField(default='')),
                ('photo', models.TextField(blank=True, default='', null=True)),
                ('info', models.TextField(blank=True, default='', null=True)),
                ('createrID', models.CharField(default='', max_length=36)),
                ('count', models.IntegerField(default=0)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(default='', max_length=36)),
                ('admin', models.CharField(default='', max_length=36)),
                ('events', models.ManyToManyField(blank=True, default=-1, null=True, to='gepu.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventID', models.CharField(default='', max_length=36)),
                ('isRide', models.BooleanField(default=False)),
                ('third_Party', models.BooleanField(default=False)),
                ('from_addr', models.TextField(default='')),
                ('count', models.IntegerField(default=0)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('phone', models.CharField(default='', max_length=15)),
                ('name', models.CharField(default='', max_length=20)),
                ('car_info', models.CharField(blank=True, default='', max_length=25)),
                ('email', models.CharField(blank=True, default='', max_length=25)),
                ('photo', models.TextField(blank=True, default='')),
                ('groups', models.ManyToManyField(blank=True, null=True, to='gepu.Group')),
                ('posts', models.ManyToManyField(blank=True, null=True, to='gepu.Post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='users',
            field=models.ManyToManyField(default=-1, to='gepu.User'),
        ),
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(blank=True, default=-1, null=True, to='gepu.User'),
        ),
        migrations.AddField(
            model_name='event',
            name='groupID',
            field=models.OneToOneField(default=-1, on_delete=django.db.models.deletion.CASCADE, to='gepu.Group'),
        ),
        migrations.AddField(
            model_name='event',
            name='posts',
            field=models.ManyToManyField(blank=True, default=-1, to='gepu.Post'),
        ),
         migrations.RunPython(create_user),
    ]
