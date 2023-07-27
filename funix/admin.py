from django.contrib import admin
from funix.models import ProblemTestCaseData, SuspiciousSubmissionBehavior, ProblemInitialSource, SubmissionWPM
from judge.admin.problem import ProblemAdmin
from judge.admin.submission import SubmissionAdmin
from django.forms import ModelForm

# problem initial source inline
class ProblemInitialSourceForm(ModelForm):
    fields = ('source', 'language')
        
class ProblemInitialSourceInline(admin.StackedInline):
    model = ProblemInitialSource
    form = ProblemInitialSourceForm
    extra = 0
    
ProblemAdmin.inlines += [ProblemInitialSourceInline]

# submission wpm inline
class SubmissionWPMInline(admin.TabularInline):
    model = SubmissionWPM

SubmissionAdmin.inlines += [SubmissionWPMInline]
def wpm_column(self, obj):
    if obj.wpm:
        return obj.wpm.wpm
    else: 
        return -1
wpm_column.admin_order_field = 'wpm__wpm'
wpm_column.short_description = "WPM"
SubmissionAdmin.wpm_column = wpm_column
del wpm_column

submission_admin_list_display = list(SubmissionAdmin.list_display)
submission_admin_list_display.insert(-2, "wpm_column")
SubmissionAdmin.list_display = submission_admin_list_display


# Register your models here.
admin.site.register(ProblemTestCaseData)
admin.site.register(SuspiciousSubmissionBehavior)
admin.site.register(ProblemInitialSource)
admin.site.register(SubmissionWPM)