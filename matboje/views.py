from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django import forms
from matboje.models import Matboj, MatbojCompetitors
import math

class IndexView(ListView):
    template_name = 'matboje/index.html'
    context_object_name = 'matboje_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return Matboj.objects.order_by('-date').all()

class MatbojDetailView(DetailView):
    model = Matboj
    template_name = 'matboje/detail.html'

    # You need to define context_object_name if you want to refer
    # to the object by a custom name and not by 'object'
    context_object_name = 'matboj'

    def get_context_data(self, **kwargs):
        context = super(MatbojDetailView, self).get_context_data(**kwargs)
        matboj = get_object_or_404(Matboj, id=self.kwargs['pk'])
        context['form']=MatchForm(matboj)
        # you need to return context here!!
        return context

# Extracting the list of the competitors from the database and then
# sorting it in python is rather uneffective - we can let the database
# do the sorting by using the proper queryset

# I don't use this method anymore, I just kept it here for your reference

# For ordering of the competitors, we set 'ordering' on the intermediate
# model of the ManyToManyField, that is MatbojCompetitors. See
# matboje/models.py

def get_competitors_list(matboj):
    competitors_list = sorted(list(matboj.matbojcompetitors_set.all()),
        key=lambda x: x.ranking, reverse=True)
    return competitors_list
 
class MatchForm(forms.Form):
    # We need to override the __init__ method to actually accept
    # the particular matboj instance
    def __init__(self, matboj, *args, **kwargs):
        # Call the __init__ from the parent
        super(MatchForm, self).__init__(self, *args, **kwargs)

        # Now do our extra stuff
        self.fields['winner'] = forms.ModelChoiceField(
            queryset=matboj.matbojcompetitors_set.all())
        self.fields['loser'] = forms.ModelChoiceField(
            queryset=matboj.matbojcompetitors_set.all())

# Note that I added *args and **kwargs to the definition of the function
def SubmitMatch(request, *args, **kwargs):
    matboj = get_object_or_404(Matboj, id=self.kwargs['pk'])

    if request.method == 'POST':
        form = MatchForm(matboj, request.POST) 
        if form.is_valid():
            winner = form.cleaned_data['winner']
            loser = form.cleaned_data['loser']

            # These equations do not make much sense,
            # do both of the competitors loose score?
            winner.rank = w.rank - math.floor(0.1*l.rank)
            loser.rank = l.rank - math.floor(0.1*l.rank)

            winner.save()
            loser.save()

    # For displaying the form you already use the MatbojDetailView form,
    # so there is some duplicity of the code now
    else:
        form = MatchForm(matboj)

    return render(request, 'detail.html', {
        'form': form,})
    #return HttpResponseRedirect(reverse('polls:detail', args=(w.matboj.id)))
    

class ResultsView(DetailView):
    model = Matboj
    template_name = 'matboje/results.html'


