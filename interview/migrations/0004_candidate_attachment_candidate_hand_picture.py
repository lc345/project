# Generated by Django 4.2.14 on 2024-08-22 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interview", "0003_alter_candidate_first_interviewer_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidate",
            name="attachment",
            field=models.FileField(blank=True, upload_to="file/", verbose_name="简历附件"),
        ),
        migrations.AddField(
            model_name="candidate",
            name="hand_picture",
            field=models.ImageField(
                blank=True, upload_to="images/", verbose_name="手势结果"
            ),
        ),
    ]
