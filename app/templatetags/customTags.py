from django import template

from wishlist.settings import ERROR_REPORTING

register = template.Library()


@register.filter
def error_tracking(arg):
	print("Test")
	if ERROR_REPORTING:
		return "Fehlerberichterstattung aktiviert"
	else:
		return ""
