from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]


class Wish(models.Model):
    text = models.TextField(max_length=1000)
    link = models.URLField(verbose_name="Link", null=True, blank=True)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    owner = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    wish_for = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wish_of")
    reserved_by = models.ManyToManyField(
        User, related_name="reserved_wishes", through="Reservation"
    )

    def is_reservation_possible(self):
        reserved = (Reservation.objects.filter(wish=self).aggregate(Sum("quantity")))[
            "quantity__sum"
        ]
        if reserved:
            return reserved < self.quantity
        return True


class Group(models.Model):
    name = models.TextField(max_length=100)
    users = models.ManyToManyField(User, related_name="wish_groups")

    def __str__(self):
        return "<Group {}>".format(self.name)


class Reservation(models.Model):
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
