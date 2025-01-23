from hashlib import md5

from django import template

register = template.Library()


@register.filter(name="email_hash")
def email_hash(obj):
    if obj and obj.email:
        mail = obj.email
        mail = mail.encode(encoding="UTF-8")
        return md5(mail).hexdigest()
    else:
        return ""
