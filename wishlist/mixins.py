from wishlist.models import Wish


class IsWishOwnerMixin:
    """Verify that the current user is thw owner of the wish."""

    def dispatch(self, request, *args, **kwargs):
        wish: Wish = self.get_object()
        if request.user != wish.owner:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
