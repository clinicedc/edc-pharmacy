from django.contrib.admin import AdminSite


class EdcPharmaAdminSite(AdminSite):
    site_header = 'Edc Pharmacy'
    site_title = 'Edc Pharmacy'
    index_title = 'Edc Pharmacy Administration'
    site_url = '/'
edc_pharma_admin = EdcPharmaAdminSite(name='edc_pharma_admin')
