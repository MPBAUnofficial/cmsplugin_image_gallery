import threading

from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from inline_ordering.models import Orderable
from filer.fields.image import FilerImageField
from django.core.exceptions import ValidationError

import utils

localdata = threading.local()
localdata.TEMPLATE_CHOICES = utils.autodiscover_templates()
TEMPLATE_CHOICES = localdata.TEMPLATE_CHOICES


class GalleryPlugin(CMSPlugin):

    def copy_relations(self, oldinstance):
        for img in oldinstance.image_set.all():
            new_img = Image()
            new_img.gallery=self
            new_img.inline_ordering_position = img.inline_ordering_position
            new_img.src = img.src
            new_img.image_url = img.image_url
            new_img.title = img.title
            new_img.alt = img.alt
            new_img.save()

    template = models.CharField(max_length=255,
                                choices=TEMPLATE_CHOICES,
                                default='cmsplugin_gallery/gallery.html',
                                editable=len(TEMPLATE_CHOICES) > 1)

    def __unicode__(self):
        return _(u'%(count)d image(s) in gallery') % {'count': self.image_set.count()}


class Image(Orderable):    
    def get_media_path(self, filename):
        pages = self.gallery.placeholder.page_set.all()
        return pages[0].get_media_path(filename)

    gallery = models.ForeignKey(
                                  GalleryPlugin, 
                                  verbose_name=_("gallery")
                               )
    
    src = FilerImageField(  
                            null=True, 
                            blank=True,
                            verbose_name=_("image") 
                         )
    
    image_url = models.URLField(
                                  _("alternative image url"), 
                                  verify_exists=True,
                                  null=True, 
                                  blank=True, 
                                  default=None
                               )
    
    link_url = models.URLField(
                                  _("link url"),
                                  verify_exists=True,
                                  null=True,
                                  blank=True,
                                  default=None,
                                  help_text=_("url used when user click on the image")
                                )
    
    src_height = models.PositiveSmallIntegerField(
                                                    _("image height"), 
                                                    editable=False, 
                                                    null=True
                                                 )

    src_width = models.PositiveSmallIntegerField(
                                                   _("image width"), 
                                                   editable=False, 
                                                   null=True
                                                )

    title = models.CharField(
                               _("title"),
                               max_length=255, 
                               blank=True
                            )

    alt = models.CharField(
                             _("alt text"), 
                             max_length=80, 
                             blank=True
                          )
    def clean(self):
        if not self.src and not self.image_url:
            raise ValidationError(_("Image not specified, use image or alternative url to specify the image source"))

    def __unicode__(self):
        return self.title or self.alt or str(self.pk)


#I don't know why, but insert class Meta in Image cause Orderable class field to doesn't work
#but this small hack solve the problem
Image._meta.get_field('inline_ordering_position').verbose_name = _("Inline ordering position")
Image._meta.verbose_name = _("Image")
Image._meta.verbose_name_plural = _("Images")
