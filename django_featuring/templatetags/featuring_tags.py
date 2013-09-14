from django import template
from django.conf import settings
from ..models import Dashboard

register = template.Library()


@register.assignment_tag
def get_featured_dashboard(slug):
    """
    Grab a dashboard of featured things.

    {% get_featured_dashboard 'homepage' as featured_stuff %}

    """
    try:
        return Dashboard.objects.get(slug=slug)
    except Dashboard.DoesNotExist:
        msg = "Dashboard `{}` probably doesn't exist.".format(slug)
        if settings.TEMPLATE_DEBUG:
            raise template.TemplateSyntaxError(msg)
        return "<!-- {} -->".format(msg)
