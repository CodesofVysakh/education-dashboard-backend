# Generated by Django 4.2.2 on 2023-07-02 08:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('duration', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'subject',
                'verbose_name_plural': 'subjects',
                'db_table': 'courses_subject',
                'ordering': ('name',),
            },
        ),
    ]
