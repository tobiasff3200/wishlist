from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from app.models import Wish


@login_required
def homeView(request):
	return HttpResponseRedirect(reverse('wishList', kwargs={'list_owner': request.user.id}))


@login_required
def wishListView(request, list_owner):
	wishes = []
	list_owner = get_object_or_404(User, pk=list_owner)
	users = User.objects.all()
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
	list_owner = get_object_or_404(User, pk=request.POST['list_owner'])
	newWish = Wish(text=text, link=link, owner=request.user, wish_for=list_owner)
	if request.user != list_owner:
		newWish.reserved_by = request.user
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
	wish = get_object_or_404(Wish, pk=wish_id)
	if wish.wish_for != request.user and not wish.reserved_by:
		wish.reserved_by = request.user
		wish.save()
	return HttpResponseRedirect(reverse('wishList', kwargs={'list_owner': request.GET['list_owner']}))


@login_required
def cancelReserveWishView(request, wish_id):
	wish = get_object_or_404(Wish, pk=wish_id)
	if wish.reserved_by == request.user:
		wish.reserved_by = None
		wish.save()
	return HttpResponseRedirect(reverse('wishList', kwargs={'list_owner': request.GET['list_owner']}))


@login_required
def editWishView(request, wish_id):
	wish = get_object_or_404(Wish, pk=wish_id)
	if request.method == 'POST':
		text = request.POST['wish-text']
		link = request.POST['wish-link']
		wish.text = text
		wish.link = link
		wish.save()
		return HttpResponseRedirect(reverse('wishList', kwargs={'list_owner': request.POST['list_owner']}))
	else:
		return render(request, 'app/edit-wish.html', {'list_owner': request.GET['list_owner'], 'wish': wish})
