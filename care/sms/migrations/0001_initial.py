# Generated by Django 3.0.4 on 2020-05-19 18:49

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identity', models.CharField(editable=False, max_length=100, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('facility_size', models.CharField(blank=True, max_length=20, null=True)),
                ('cluster', models.BooleanField(default=False)),
                ('address', models.TextField(blank=True, null=True)),
                ('liasons', models.CharField(blank=True, max_length=255, null=True)),
                ('emails', models.TextField(blank=True, null=True)),
                ('phones', models.TextField(blank=True, null=True)),
                ('reporting_new_cases', models.BooleanField(default=False)),
                ('last_new_cases_reported', models.IntegerField(default=0)),
                ('last_upload_date', models.DateTimeField(blank=True, null=True)),
                ('last_message_date', models.DateTimeField(blank=True, null=True)),
                ('last_message_open_date', models.DateTimeField(blank=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Facility',
                'verbose_name_plural': 'Facilities',
            },
        ),
        migrations.CreateModel(
            name='TwilioConversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.CharField(max_length=200)),
                ('account_sid', models.CharField(max_length=200)),
                ('chat_service_sid', models.CharField(max_length=200)),
                ('messaging_service_sid', models.CharField(max_length=200)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TwilioMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('index', models.PositiveIntegerField()),
                ('author_sid', models.CharField(blank=True, max_length=200, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.TwilioConversation')),
                ('facility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sms.Facility')),
            ],
        ),
        migrations.CreateModel(
            name='QualtricsSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('facility_name', models.CharField(blank=True, max_length=200, null=True)),
                ('reported_new_cases', models.BooleanField(default=False)),
                ('new_cases', models.IntegerField(default=0)),
                ('facility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sms.Facility')),
            ],
        ),
        migrations.CreateModel(
            name='Binding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_sid', models.CharField(max_length=255)),
                ('binding_sid', models.CharField(max_length=255)),
                ('binding_type', models.CharField(choices=[('sms', 'Sms'), ('facebook-messenger', 'Fb'), ('apn', 'Apn'), ('fcm', 'Fcm'), ('gcm', 'Gcm')], default='sms', max_length=20)),
                ('opt_out', models.BooleanField(default=False)),
                ('address', models.CharField(help_text='Phone number, e.g. +15205551234', max_length=255)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.Facility')),
            ],
            options={
                'verbose_name': 'SMS Number',
                'verbose_name_plural': 'SMS Numbers',
            },
        ),
    ]