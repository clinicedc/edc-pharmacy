from django.views.generic.base import TemplateView
from django.shortcuts import render

from edc_base.views.edc_base_view_mixin import EdcBaseViewMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(EdcBaseViewMixin, TemplateView):

    template_name = 'edc_pharma/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
    
    #def search_form(request):
     #   return render(request, 'home.html')
    
    #def search(request):
     #   if 'q' in request.GET:
     #       message = 'You searched for: %r' % request.GET['q']
     #   else:
     #       message = 'You submitted an empty form.'
      #  return HttpResponse(message)
