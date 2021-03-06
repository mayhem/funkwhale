# Generated by Django 2.0.6 on 2018-06-17 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0007_auto_20180524_2009")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_activity",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="permission_library",
            field=models.BooleanField(
                default=False,
                help_text="Manage library, delete files, tracks, artists, albums...",
                verbose_name="Manage library",
            ),
        ),
    ]
