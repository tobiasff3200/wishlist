from django.urls import path

from app import views

urlpatterns = [
	path('', views.homeView, name="homeView"),
	path('wish/<int:list_owner>', views.wishListView, name="wishList"),
	path('wish', views.newWishView, name="newOwnWish"),
	path('wish/delete/<int:wish_id>', views.deleteWishView, name="deleteWish"),
	path('wish/reserve/<int:wish_id>', views.reserveWishView, name="reserveWish"),
	path('wish/unreserve/<int:wish_id>', views.cancelReserveWishView, name="cancelReserveWish"),
	path('wish/edit/<int:wish_id>', views.editWishView, name="editWish"),
]
