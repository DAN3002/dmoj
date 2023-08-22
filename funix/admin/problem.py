from django.contrib import admin
from funix.models.problem import ProblemInitialSource, ProblemTestCaseDataTranslation
from django.forms import ModelForm
from judge.models.problem_data import ProblemTestCase

# problem initial source inline
class ProblemInitialSourceForm(ModelForm):
    fields = ('source', 'language')
        
class ProblemInitialSourceInline(admin.StackedInline):
    model = ProblemInitialSource
    form = ProblemInitialSourceForm
    extra = 0
    
# ProblemTestCase inline
class ProblemTestCaseInline(admin.StackedInline):
    model = ProblemTestCase
    extra = 0
    show_change_link = True
    fields = ['order']
    readonly_fields = fields
    can_delete = False
    fk_name = "dataset"
    
    def has_add_permission(self, request, obj):
        return False

class ProblemTestCaseAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        all_fields = [field.name for field in self.model._meta.get_fields()]
        return all_fields

class ProblemTestCaseDataTranslationInline(admin.StackedInline):
    model = ProblemTestCaseDataTranslation
    extra = 0

class ProblemTestCaseDataAdmin(admin.ModelAdmin):
    fields = ["input_data"]
    readonly_fields = fields
    inlines = [ProblemTestCaseDataTranslationInline]

