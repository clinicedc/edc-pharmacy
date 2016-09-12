#auditing-sample/auditable/models.py
from django.conf import settings
from django.db import models

class Auditable(models.Model):
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_by')

    modified_on = models.DateTimeField(auto_now = True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='modified_by')

    class Meta:
        abstract = True


#auditing-sample/auditable/views.py

class AuditableMixin(object,):
    def form_valid(self, form, ):
        if not form.instance.id:
            form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super(AuditableMixin, self).form_valid(form)
    
    
