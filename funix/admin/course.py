from django.contrib import admin
from funix.models.course import Course, CourseProblem, CourseSection
from django.forms import ModelForm
from judge.widgets import AdminMartorWidget


# course problem inline
class CourseProblemForm(ModelForm):
    fields = ("problem", "number", "time")

class CourseProblemInline(admin.StackedInline):
    model = CourseProblem
    form = CourseProblemForm
    extra = 0
    
# course section inline
class CourseSectionForm(ModelForm):
    fields = ('name', 'number')
        
class CourseSectionInline(admin.StackedInline):
    model = CourseSection
    form = CourseSectionForm
    extra = 0


# course form
class CourseForm(ModelForm):
    class Meta: 
        model = Course
        fields = "__all__"
        widgets = {
            'goals': AdminMartorWidget(),
        }
        
class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    inlines = [CourseSectionInline,CourseProblemInline]
    





    




