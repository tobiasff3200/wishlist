# Generated by Django 4.0.6 on 2022-08-21 08:40

import wishlist.models
from django.conf import settings
from django.db import migrations, models


def migrate_reservations(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Wish = apps.get_model("wishlist", "Wish")
    for wish in Wish.objects.using(db_alias).all():
        wish.reserved_by.add(wish.reserved_by_old)
        wish.save()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wishlist", "0003_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="wish",
            name="quantity",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="wish",
            name="owner",
            field=models.ForeignKey(
                on_delete=models.SET(wishlist.models.get_sentinel_user),
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RenameField(
            model_name="wish", old_name="reserved_by", new_name="reserved_by_old"
        ),
        migrations.AddField(
            model_name="wish",
            name="reserved_by",
            field=models.ManyToManyField(
                related_name="reserved_wishes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.RunPython(migrate_reservations),
        migrations.RemoveField(
            model_name="wish",
            name="reserved_by_old",
        ),
    ]
