# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_title', models.CharField(max_length=512)),
                ('long_title', models.CharField(max_length=512)),
                ('objective_copy', models.TextField(blank=True)),
                ('collect_notes', models.BooleanField(default=False)),
                ('collect_buddy_name', models.BooleanField(default=False)),
                ('collect_referral_info', models.BooleanField(default=False)),
                ('collect_reasons_for_returning', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name=b'date modified')),
                ('game', models.CharField(blank=True, max_length=64, null=True, choices=[(b'assessmentquiz', b'Assessment Quiz Mood'), (b'assessmentquiz-audit', b'Assessment Quiz Alchohol Audit'), (b'assessmentquiz-drug-audit', b'Assessment Quiz Drug Audit'), (b'lifegoals', b'Life Goals'), (b'pills', b'Pill Game - Practice'), (b'pills-my-regimen', b'Pill Game - My Regimen'), (b'island', b'Island Before Medication'), (b'island-after-medication', b'Island After Medication'), (b'ssnmTree', b'Social Support Network Tree'), (b'video-soldiers', b'Soldiers and Snakes'), (b'video-joseph', b'Joseph and Hope'), (b'video-problem-solving', b'Problem Solving Video'), (b'problemsolving', b'Problem Solving')])),
            ],
            options={
                'verbose_name_plural': 'activities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivityVisit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('logged', models.DateTimeField(auto_now_add=True, verbose_name=b'start timestamp')),
                ('activity', models.ForeignKey(to='intervention.Activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Backup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('json_data', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('deployment', models.CharField(default=b'Clinic', max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_title', models.CharField(max_length=512)),
                ('long_title', models.CharField(max_length=512)),
                ('introductory_copy', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name=b'date modified')),
                ('defaulter', models.BooleanField(default=False, verbose_name=b'only show to defaulters')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CounselorNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(default=b'', null=True, blank=True)),
                ('counselor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Clinic', max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GamePage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512, blank=True)),
                ('subtitle', models.CharField(max_length=512, blank=True)),
                ('description', models.TextField(blank=True)),
                ('instructions', models.TextField(blank=True)),
                ('activity', models.ForeignKey(blank=True, to='intervention.Activity', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512, blank=True)),
                ('style', models.CharField(blank=True, max_length=64, null=True, choices=[(b'do', b'Do'), (b'say', b'Say')])),
                ('instruction_text', models.TextField(blank=True)),
                ('image', models.FileField(null=True, upload_to=b'intervention_images', blank=True)),
                ('help_copy', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name=b'date modified')),
                ('activity', models.ForeignKey(to='intervention.Activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('intervention_id', models.CharField(default=b'1', max_length=8)),
                ('general_instructions', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('id_number', models.CharField(max_length=256)),
                ('patient_id', models.CharField(default=b'', max_length=256, verbose_name=b'ID for linking patient to other research data')),
                ('defaulter', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('clinical_notes', models.TextField(default=b'', blank=True)),
                ('buddy_name', models.CharField(default=b'', max_length=256, blank=True)),
                ('gender', models.CharField(default=b'male', max_length=16, choices=[(b'male', b'Male'), (b'female', b'Female')])),
                ('initial_referral_mental_health', models.BooleanField(default=False)),
                ('initial_referral_alcohol', models.BooleanField(default=False)),
                ('initial_referral_drug_use', models.BooleanField(default=False)),
                ('initial_referral_other', models.BooleanField(default=False)),
                ('initial_referral_notes', models.TextField(default=b'', blank=True)),
                ('defaulter_referral_mental_health', models.BooleanField(default=False)),
                ('defaulter_referral_alcohol', models.BooleanField(default=False)),
                ('defaulter_referral_drugs', models.BooleanField(default=False)),
                ('defaulter_referral_other', models.BooleanField(default=False)),
                ('defaulter_referral_notes', models.TextField(default=b'', blank=True)),
                ('reasons_for_returning', models.TextField(default=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipantActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'incomplete', max_length=256)),
                ('activity', models.ForeignKey(to='intervention.Activity')),
                ('participant', models.ForeignKey(to='intervention.Participant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipantGameVar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=256)),
                ('value', models.TextField(default=b'', null=True, blank=True)),
                ('participant', models.ForeignKey(to='intervention.Participant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipantSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'incomplete', max_length=256)),
                ('participant', models.ForeignKey(to='intervention.Participant')),
                ('session', models.ForeignKey(to='intervention.ClientSession')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SessionVisit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('logged', models.DateTimeField(auto_now_add=True, verbose_name=b'start timestamp')),
                ('participant', models.ForeignKey(to='intervention.Participant')),
                ('session', models.ForeignKey(to='intervention.ClientSession')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterOrderWithRespectTo(
            name='instruction',
            order_with_respect_to='activity',
        ),
        migrations.AlterOrderWithRespectTo(
            name='gamepage',
            order_with_respect_to='activity',
        ),
        migrations.AddField(
            model_name='counselornote',
            name='participant',
            field=models.ForeignKey(to='intervention.Participant', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientsession',
            name='intervention',
            field=models.ForeignKey(to='intervention.Intervention'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='clientsession',
            order_with_respect_to='intervention',
        ),
        migrations.AddField(
            model_name='activityvisit',
            name='participant',
            field=models.ForeignKey(to='intervention.Participant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='clientsession',
            field=models.ForeignKey(to='intervention.ClientSession'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='activity',
            order_with_respect_to='clientsession',
        ),
    ]
