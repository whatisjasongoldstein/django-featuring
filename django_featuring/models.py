from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.loader import render_to_string, find_template
from django.template import TemplateDoesNotExist


class Dashboard(models.Model):
    """ A group of featured stuff. """
    slug = models.SlugField(unique=True)
    sites = models.ManyToManyField(Site, blank=True)

    def __unicode__(self):
        return self.slug


class Thing(models.Model):
    """ An item to feature. """
    dashboard = models.ForeignKey(Dashboard, related_name="things")
    order = models.IntegerField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    source = generic.GenericForeignKey('content_type', 'object_id')
    template = models.CharField(max_length=255, default="", blank=True, help_text="Use a custom template for this item.")

    class Meta:
        ordering = ['order',]

    def __unicode__(self):
        return self.source.__unicode__()

    def get_template(self):
        if self.template:
            try: # Idiot-proofing
                find_template(self.template)
                return self.template
            except TemplateDoesNotExist:
                pass
        return "featured/{app}.{model}.html".format(app=self.content_type.app_label, model=self.content_type.model)

    def render(self):
        try:
            return render_to_string(self.get_template(), {'object': self.source})
        except TemplateDoesNotExist:
            template = getattr(settings, 'DEFAULT_FEATURED_TEMPLATE', "featured/default.html")
            return render_to_string(template, {'object': self.source})

