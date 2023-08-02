from django.contrib import admin
from funix.models.problem import ProblemInitialSource
from django.forms import ModelForm

# problem initial source inline
class ProblemInitialSourceForm(ModelForm):
    fields = ('source', 'language')
        
class ProblemInitialSourceInline(admin.StackedInline):
    model = ProblemInitialSource
    form = ProblemInitialSourceForm
    extra = 0
    



