from django.contrib import admin
from funix.models import ProblemTestCaseData, SuspiciousSubmissionBehavior, ProblemInitialSource, SubmissionWPM
from judge.admin.problem import ProblemAdmin
from django.forms import ModelForm
    
class ProblemInitialSourceForm(ModelForm):
    fields = ('source', 'language')
        
class ProblemInitialSourceInline(admin.StackedInline):
    model = ProblemInitialSource
    form = ProblemInitialSourceForm
    extra = 0

ProblemAdmin.inlines = ProblemAdmin.inlines + [ProblemInitialSourceInline]

# Register your models here.
admin.site.register(ProblemTestCaseData)
admin.site.register(SuspiciousSubmissionBehavior)
admin.site.register(ProblemInitialSource)
admin.site.register(SubmissionWPM)