from django.contrib import admin
from django.forms import ModelForm, ModelChoiceField

from .models import *


class ModFormAdmin(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('instance'):
            instance = kwargs.get('instance')
            if not instance.accum:
                self.fields['accum_capacity'].widget.attrs.update({
                    'readonly': True, 'style': 'background: lightgray;'
                })
            else:
                self.fields['accum_type'].widget.attrs.update({
                    'readonly': True, 'style': 'background: lightgray;'
                })

    def clean(self):
        if not self.cleaned_data['accum']:
            self.cleaned_data['accum_capacity'] = None
        else:
            self.cleaned_data['accum_type'] = None
        return self.cleaned_data



class ModAdmin(admin.ModelAdmin):
    form = ModFormAdmin

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(category_name='Электронные моды'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MechModAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(category_name='Механические моды'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Category)
admin.site.register(Mod, ModAdmin)
admin.site.register(MechMod,MechModAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
