from django.contrib import admin

from edc_label.views.edc_label_view_mixin import EdcLabelViewMixin

from .models import Dispense

@admin.register(Dispense)
class DispenseAdmin(EdcLabelViewMixin, admin.ModelAdmin):
    pass
admin.site.register(Dispense, DispenseAdmin)