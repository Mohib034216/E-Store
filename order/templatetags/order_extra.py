from django import template


register = template.Library()


@register.filter(name="hasattr")
def hasattr(obj, attr):
    hasattr(obj,attr)


@register.filter(name="ship_default")
def ship_default(obj):
    return obj.filter(ship_default=True)

@register.filter(name="bill_default")
def bill_default(obj):
    obj = obj.filter(bill_default=True,ship_default=True)
    if obj.exists():
        return True
    else:
        return False
   