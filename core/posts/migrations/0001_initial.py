# Generated by Django 5.0.6 on 2025-05-25 20:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ('title',),
                'permissions': [('can_edit_post', 'Can Edit Post'), ('can_create_post', 'Can Create Post'), ('can_view_post', 'Can View Post'), ('can_publish', 'Can Publish Post'), ('can_delete_post', 'Can Delete Ppost'), ('can_share_post', 'Can Share Post'), ('can_report_post', 'Can Report Post'), ('can_comment_on_post', 'Can Comment On Post')],
            },
        ),
    ]
