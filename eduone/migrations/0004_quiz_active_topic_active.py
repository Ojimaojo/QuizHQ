# Generated by Django 4.1.3 on 2022-12-16 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduone', '0003_alter_option_question_withdraw_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='topic',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
