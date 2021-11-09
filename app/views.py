from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from app.models import Wish


def homeView(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('wishList', kwargs={'list_user': request.user.id}))
	else:
		return HttpResponseRedirect(reverse('login'))


def wishListView(request, list_user):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('homeView'))
	wishes = []
	if request.user.is_authenticated:
		list_owner = get_object_or_404(User, pk=list_user)
		users = User.objects.all()
		if list_owner == request.user:
			wishes = Wish.objects.filter(wish_for=list_owner).filter(owner=request.user)
		else:
			wishes = Wish.objects.filter(wish_for=list_owner)
	return render(request, "app/own-wish-list.html",
	              context={'wishes': wishes, 'list_owner': list_owner, 'all_users': users})


def newWishView(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('ownList'), status=401)
	text = request.POST['wish-text']
	link = request.POST['wish-link']
	list_owner = get_object_or_404(User, pk=request.POST['list_owner'])
	newWish = Wish(text=text, link=link, owner=request.user, wish_for=list_owner)
	if request.user != list_owner:
		newWish.reserved_by = request.user
	newWish.save()
	return HttpResponseRedirect(reverse('wishList', kwargs={'list_user': request.POST['list_owner']}))


def deleteWishView(request, wish_id):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('ownList'), status=401)
	wish = get_object_or_404(Wish, pk=wish_id)
	if wish.owner == request.user:
		wish.delete()
	return HttpResponseRedirect(reverse('wishList', kwargs={'list_user': request.GET['list_owner']}))


def reserveWishView(request, wish_id):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('ownList'), status=401)
	wish = get_object_or_404(Wish, pk=wish_id)
	if wish.wish_for != request.user and not wish.reserved_by:
		wish.reserved_by = request.user
		wish.save()
	return HttpResponseRedirect(reverse('wishList', kwargs={'list_user': request.GET['list_owner']}))


def cancelReserveWishView(request, wish_id):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('ownList'), status=401)
	wish = get_object_or_404(Wish, pk=wish_id)
	if wish.reserved_by == request.user:
		wish.reserved_by = None
		wish.save()
	return HttpResponseRedirect(reverse('wishList', kwargs={'list_user': request.GET['list_owner']}))
