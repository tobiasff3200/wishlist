import django.forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms import modelform_factory
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView

from mixins import IsWishOwnerMixin
from wishlist.models import Wish, Reservation, Group


@login_required
def home_view(request):
    return HttpResponseRedirect(
        reverse("wishList", kwargs={"list_owner": request.user.id})
    )


def get_all_users_filtered(request: HttpRequest) -> list[User]:
    """
    Returns a list of users within the same groups as the current user. If there are no groups, all users in the User table are returned.
    @param request: The current incoming http request
    @return: list[User]: A list of User objects that match the specified filter criteria.
    """
    if Group.objects.count() > 0:
        groups = request.user.wish_groups.all()
        user_set = set()  # set only allows unique values
        for group in groups:
            user_set.update(list(group.users.all()))
        users = list(user_set)
    else:
        users = User.objects.all()
    return users


@login_required
def wishListView(request: HttpRequest, list_owner):
    users = get_all_users_filtered(request)
    list_owner = get_object_or_404(User, pk=list_owner)
    # Check if the user is allowed to see the list
    if not (list_owner in users or list_owner == request.user):
        raise PermissionDenied()
    # Get all requests except those that are from others for the user
    if list_owner == request.user:
        wishes = Wish.objects.filter(wish_for=list_owner).filter(owner=request.user).filter(depends_on__isnull=True)
    else:
        wishes = Wish.objects.filter(wish_for=list_owner).filter(depends_on__isnull=True)

    return render(
        request,
        "wishlist/own-wish-list.html",
        context={"wishes": wishes, "list_owner": list_owner, "all_users": users},
    )


class CreateWishView(LoginRequiredMixin, CreateView):
    model = Wish
    template_name = "wishlist/create-wish.html"
    form_class = modelform_factory(
        Wish,
        fields=("text", "link", "quantity", "depends_on"),
        labels={"text": "Wunsch", "link": "Link", "quantity": "Anzahl"},
        widgets={
            "text": django.forms.TextInput(
                attrs={"class": "input input-bordered w-full max-w-xs"}
            ),
            "link": django.forms.URLInput(
                attrs={"class": "input input-bordered w-full max-w-xs"}
            ),
            "quantity": django.forms.NumberInput(
                attrs={"class": "input input-bordered w-full max-w-xs", "min": 1}
            ),
            "depends_on": django.forms.Select(attrs={"class": "select select-bordered w-full max-w-xs"})
        },
    )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['depends_on'].queryset = Wish.objects.filter(wish_for_id=self.kwargs.get("list_owner"))
        return form

    def form_valid(self, form):
        if form.is_valid():
            list_owner = get_object_or_404(User, pk=self.kwargs["list_owner"])
            print(form.cleaned_data)
            data = form.cleaned_data
            wish = Wish(
                text=data.get("text"),
                link=data.get("link"),
                quantity=data.get("quantity"),
                owner=self.request.user,
                wish_for=list_owner,
                depends_on=data.get("depends_on")
            )
            wish.save()
            if self.request.user != list_owner:
                reservation = Reservation(user=self.request.user, wish=wish)
                reservation.save()
                wish.save()
            return HttpResponseRedirect(
                reverse("wishList", kwargs={"list_owner": list_owner.id})
            )
        else:
            return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_users"] = get_all_users_filtered(self.request)
        context["list_owner"] = get_object_or_404(User, pk=self.kwargs["list_owner"])
        return context


@login_required
def deleteWishView(request, wish_id):
    wish = get_object_or_404(Wish, pk=wish_id)
    if wish.owner == request.user:
        wish.delete()
    return HttpResponseRedirect(
        reverse("wishList", kwargs={"list_owner": request.GET["list_owner"]})
    )


@login_required
def toggleFavoriteView(request, wish_id):
    wish = get_object_or_404(Wish, pk=wish_id)
    if wish.wish_for_id == request.user.id:
        wish.favorite = not wish.favorite
        wish.save()
    return HttpResponseRedirect(
        reverse("wishList", kwargs={"list_owner": request.user.id})
    )


@login_required
def reserveWishView(request, wish_id):
    wish: Wish = get_object_or_404(Wish, pk=wish_id)
    if wish.wish_for != request.user and wish.is_reservation_possible():
        reservation = Reservation.objects.all().filter(user=request.user, wish=wish)
        if reservation:
            if len(reservation) > 1:
                raise Exception("More than one reservation")
            reservation[0].quantity = reservation[0].quantity + 1
            reservation[0].save()
        else:
            reservation = Reservation(user=request.user, wish=wish)
            reservation.save()
        wish.save()
    return HttpResponseRedirect(
        reverse("wishList", kwargs={"list_owner": request.GET["list_owner"]})
    )


@login_required
def cancelReserveWishView(request, wish_id):
    wish = get_object_or_404(Wish, pk=wish_id)
    reservation = Reservation.objects.all().filter(user=request.user, wish=wish)
    if len(reservation) > 1:
        raise Exception("More than one reservation")
    if reservation[0].quantity > 1:
        reservation[0].quantity = reservation[0].quantity - 1
        reservation[0].save()
    else:
        reservation[0].delete()
    return HttpResponseRedirect(
        reverse("wishList", kwargs={"list_owner": request.GET["list_owner"]})
    )


def getManifest(request):
    return render(request, "wishlist/manifest.json", content_type="application/json")


class EditWishView(LoginRequiredMixin, IsWishOwnerMixin, UpdateView):
    model = Wish
    template_name = "wishlist/edit-wish.html"
    form_class = modelform_factory(
        Wish,
        fields=("text", "link", "quantity", "depends_on"),
        labels={"text": "Wunsch", "link": "Link", "quantity": "Anzahl"},
        widgets={
            "text": django.forms.TextInput(
                attrs={"class": "input input-bordered w-full max-w-xs"}
            ),
            "link": django.forms.URLInput(
                attrs={"class": "input input-bordered w-full max-w-xs"}
            ),
            "quantity": django.forms.NumberInput(
                attrs={"class": "input input-bordered w-full max-w-xs", "min": 1}
            ),
            "depends_on": django.forms.Select(attrs={"class": "select select-bordered w-full max-w-xs"})
        },
    )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['depends_on'].queryset = Wish.objects.filter(wish_for_id=self.get_object().wish_for)
        return form

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_users"] = get_all_users_filtered(self.request)
        return context

    def get_success_url(self):
        return reverse(
            "wishList", kwargs={"list_owner": self.request.GET.get("list_owner")}
        )


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation

    def get_queryset(self, *args, **kwargs):
        qs = super(ReservationListView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["all_users"] = get_all_users_filtered(self.request)
        return context
