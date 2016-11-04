from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_label.view_mixins import EdcLabelViewMixin

from edc_pharma.forms.patient_form import PatientForm

from edc_pharma.models.dispense import Patient


class HomeView(EdcBaseViewMixin, EdcLabelViewMixin, FormView):

    template_name = 'edc_pharma/home.html'
    form_class = PatientForm
    paginate_by = 2
    paginator_template = 'edc_pharma/paginator_row.html'
    number_of_copies = 1

    def __init__(self, **kwargs):
        self.patient = Patient.objects.all().order_by('-consent_date')
        super(HomeView, self).__init__(**kwargs)

    def get_success_url(self):
        return reverse('home_url')

    def form_valid(self, form):
        if form.is_valid():
            subject_identifier = form.cleaned_data['subject_identifier']
            try:
                self.patient = Patient.objects.filter(subject_identifier__contains=subject_identifier)
            except Patient.DoesNotExist:
                form.add_error('subject_identifier', 'Patient not found. Please search again or add a new patient.')
            context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'patients': self.patient})
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
