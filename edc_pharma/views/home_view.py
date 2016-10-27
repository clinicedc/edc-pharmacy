from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from edc_base.model.constants import DEFAULT_BASE_FIELDS
from edc_base.views.edc_base_view_mixin import EdcBaseViewMixin
from edc_label.view_mixins import EdcLabelViewMixin

from edc_pharma.forms.patient_form import PatientForm
from edc_pharma.choices import TABLET, SYRUP, IV, IM, SUPPOSITORY
from edc_pharma.models.dispense import Dispense, Patient


class HomeView(EdcBaseViewMixin, EdcLabelViewMixin, FormView):

    template_name = 'edc_pharma/home.html'
    form_class = PatientForm
    paginate_by = 2
    paginator_template = 'edc_pharma/paginator_row.html'
    number_of_copies = 1

    def __init__(self, **kwargs):
        self.patient = None
        super(HomeView, self).__init__(**kwargs)

    def get_success_url(self):
        return reverse('home_url')

    def form_valid(self, form):
        if form.is_valid():
            subject_identifier = form.cleaned_data['subject_identifier']
            try:
                self.patient = Patient.objects.get(subject_identifier=subject_identifier)
            except Patient.DoesNotExist:
                form.add_error('subject_identifier', 'Patient not found. Please search again or add a new patient.')
            context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.kwargs.get('dispense_pk'):
            self.print_label()
        if not self.patient:
            try:
                self.patient = Patient.objects.get(subject_identifier=self.kwargs.get('subject_identifier'))
            except Patient.DoesNotExist:
                pass
        dispenses = Dispense.objects.filter(patient=self.patient).order_by('-prepared_datetime')
        if dispenses:
            context.update({'dispenses': self.dispenses})
        context.update({
            'recent_dispense_querystring': self.refill_query_string,
            'patient': self.patient})
        return context

    def print_label(self):
        dispense = Dispense.objects.get(pk=self.kwargs.get('dispense_pk'))
        label_name = self.label_name(dispense.dispense_type)
        super(HomeView, self).print_label(
            label_name, copies=self.number_of_copies, context=dispense.label_context)

    def label_name(self, name):
        if name == TABLET:
            return 'dispense_label_tablet'
        elif name == SYRUP:
            return 'dispense_label_syrup'
        elif name == IV:
            return 'dispense_label_iv'
        elif name == IM:
            return 'dispense_label_im'
        elif name == SUPPOSITORY:
            return 'dispense_label_suppository'

    @property
    def refill_query_string(self):
        try:
            last = {}
            dispense = Dispense.objects.filter(patient=self.patient).last()
            for field in Dispense._meta.fields:
                if field.name not in DEFAULT_BASE_FIELDS + ['prepared_datetime', 'medication_id', 'patient_id']:
                    value = getattr(dispense, field.name)
                    if value:
                        last.update({field.name: value})
            last['medication'] = last['medication'].id
            last['patient'] = last['patient'].id
            query_string = urlencode(last)
        except AttributeError:
            query_string = ''
        return query_string

    @property
    def dispenses(self):
        """Returns a dispense queryset after pagination."""
        dispenses = Dispense.objects.filter(patient=self.patient).order_by('-prepared_datetime')
        paginator = Paginator(dispenses, self.paginate_by)
        try:
            dispenses = paginator.page(self.kwargs.get('page', 1))
        except EmptyPage:
            dispenses = paginator.page(paginator.num_pages)
        return dispenses

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
