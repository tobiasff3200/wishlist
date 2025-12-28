from django.urls import path

from wishlist import views

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path('health/', views.health_check, name='health_check'),
    path("wish/<int:list_owner>", views.wishListView, name="wishList"),
    path("wish2/<int:pk>", views.wishListView, name="wishList2"),
    path("wish/add/<int:list_owner>", views.CreateWishView.as_view(), name="createWish"),
    path("wish/delete/<int:pk>", views.DeleteWishView.as_view(), name="deleteWish"),
    path("wish/favorite/<int:wish_id>", views.toggleFavoriteView, name="toggleFavorite"),
    path("wish/reserve/<int:wish_id>", views.reserveWishView, name="reserveWish"),
    path("wish/unreserve/<int:wish_id>", views.cancelReserveWishView, name="cancelReserveWish", ),
    path("wish/edit/<int:pk>", views.EditWishView.as_view(), name="editWish"),
    path("reservations", views.ReservationListView.as_view(), name="reservationListView"),
    path("manifest.json", views.getManifest, name="manifest")
]
