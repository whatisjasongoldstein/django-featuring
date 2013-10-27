
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.loader import select_template
from django.template import Context
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse


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
        obj_name = getattr(self.source, '__unicode__', None)
        if obj_name:
            return obj_name()

    def get_template(self):
        """
        Returns the first valid template that exists.
        1. Explicity set template
        2. featured/app_name.model.html
        3. The default template.
        """
        templates = [
            self.template,
            "featured/{app}.{model}.html".format(app=self.content_type.app_label, model=self.content_type.model),
            getattr(settings, 'DEFAULT_FEATURED_TEMPLATE', "featured/default.html")
        ]
        return select_template(templates)

    def render(self):
        """ Renders this thing against its template, falls back to the default
        template if the `featured/app.model.html` isn't available. """
        template = self.get_template()
        context = Context({"object": self.source})
        return template.render(context)

    def link_to_source(self):
        """ Get admin link to the original. """
        href = reverse("admin:{app}_{model}_change".format(
            app=self.content_type.app_label, 
            model=self.content_type.model), 
            args=[self.source.id])
        html = u"""<a href="{url}">{obj}</a>"""
        return html.format(url=href, obj=self.source.__unicode__())

    link_to_source.allow_tags = True
    link_to_source.short_description = "Admin"
