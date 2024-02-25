# Generated by Django 5.0.2 on 2024-02-22 09:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0003_discussion_content_discussion_created_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookclub",
            name="discussion_list_id",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="bookclub",
            name="member_list",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="book_club",
                to="base.memberlist",
            ),
        ),
        migrations.AlterField(
            model_name="bookclub",
            name="next_meeting_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="discussion",
            name="num_posts",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="memberlist",
            name="is_admin",
            field=models.BooleanField(default=False, null=True),
        ),
    ]