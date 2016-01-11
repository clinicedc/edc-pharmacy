from django.contrib import admin
from edc_base.modeladmin.admin import BaseModelAdmin
from ..actions import print_dispensing_label
from ..models import Dispensing


class DispensingAdmin(BaseModelAdmin):

    list_display = ('identifier', 'subject_identifier', 'sid', 'copies', 'dispense_date', 'user_created', 'created')
    actions = [print_dispensing_label]
    list_per_page = 25
    search_fields = ('subject_identifier', 'sid', 'identifier')
    list_filter = ('dispense_date', 'user_created', 'created')

admin.site.register(Dispensing, DispensingAdmin)
