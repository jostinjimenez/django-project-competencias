# custom_tags.py
from django import template
from django.apps import apps

register = template.Library()


@register.filter
def get_items_from_queryset(queryset, pks):
    model = queryset.model
    try:
        pks_list = [int(pk) for pk in pks.split(',')]
        return model.objects.filter(pk__in=pks_list)
    except (model.DoesNotExist, ValueError):
        return None
