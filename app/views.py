from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from app.models import Wish, Group, Reservation


@login_required
def homeView(request):
    return HttpResponseRedirect(reverse('wishList', kwargs={'list_owner': request.user.id}))


@login_required
def wishListView(request, list_owner):
    # Get all user which are in one of the users groups
    print(Group.objects.count())
    if Group.objects.count() > 0:
        groups = request.user.wish_groups.all()
        userSet = set()  # set only allows unique values
        for group in groups:
            userSet.update(list(group.users.all()))
        users = list(userSet)
    else:
        users = User.objects.all()
    # Get all requests except those that are from others for the user
    list_owner = get_object_or_404(User, pk=list_owner)
    if list_owner == request.user:
        wishes = Wish.objects.filter(wish_for=list_owner).filter(owner=request.user)
    else:
        wishes = Wish.objects.filter(wish_for=list_owner)

    return render(request, "app/own-wish-list.html",
                  context={'wishes': wishes, 'list_owner': list_owner, 'all_users': users})


@login_required
def newWishView(request):
    text = request.POST['wish-text']
    link = request.POST['wish-link']
    quantity = request.POST['wish-quantity']
    list_owner = get_object_or_404(User, pk=request.POST['list_owner'])
    newWish = Wish(text=text, link=link, quantity=quantity, owner=request.user, wish_for=list_owner)
    newWish.save()
    if request.user != list_owner:
        reservation = Reservation(user=request.user, wish=newWish)
        reservation.save()
        newWish.save()
    return HttpResponseRedirect(reverse('wishList', kwargs={'list_owner': request.POST['list_owner']}))


@login_required
def deleteWishView(request, wish_id):
    wish = get_object_or_404(Wish, pk=wish_id)
    if wish.owner == request.user:
        wish.delete()
    return HttpResponseRedirect(reverse('wishList', kwargs={'list_owner': request.GET['list_owner']}))


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
    return HttpResponseRedirect(reverse('wishList', kwargs={'list_owner': request.GET['list_owner']}))


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
    return HttpResponseRedirect(reverse('wishList', kwargs={'list_owner': request.GET['list_owner']}))


@login_required
def editWishView(request, wish_id):
    wish = get_object_or_404(Wish, pk=wish_id)
    if request.method == 'POST':
        text = request.POST['wish-text']
        link = request.POST['wish-link']
        quantity = request.POST['wish-quantity']
        wish.text = text
        wish.link = link
        wish.quantity = quantity
        wish.save()
        return HttpResponseRedirect(reverse('wishList', kwargs={'list_owner': request.POST['list_owner']}))
    else:
        return render(request, 'app/edit-wish.html', {'list_owner': request.GET['list_owner'], 'wish': wish})
