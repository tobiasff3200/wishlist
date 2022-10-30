from django.urls import path

from app import views

urlpatterns = [
	path('', views.homeView, name="homeView"),
	path('wish/<int:list_owner>', views.wishListView, name="wishList"),
	path('wish/add/<int:list_owner>', views.CreateWishView.as_view(), name="createWish"),
	path('wish/delete/<int:wish_id>', views.deleteWishView, name="deleteWish"),
	path('wish/reserve/<int:wish_id>', views.reserveWishView, name="reserveWish"),
	path('wish/unreserve/<int:wish_id>', views.cancelReserveWishView, name="cancelReserveWish"),
	path('wish/edit/<int:pk>', views.EditWishView.as_view(), name="editWish"),
]
