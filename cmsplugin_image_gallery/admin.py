from inline_ordering.admin import OrderableStackedInline
import forms
import models
from django.utils.translation import ugettext_lazy as _


class ImageInline(OrderableStackedInline):

    model = models.Image
    name = _('image')
    fieldsets =  (
        ( None, {
            'fields': ('inline_ordering_position',('src', 'image_url'), 'link_url', 'title','alt')
         }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'src':
            kwargs.pop('request', None)
            kwargs['widget'] = forms.AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(ImageInline, self).\
            formfield_for_dbfield(db_field, **kwargs)
