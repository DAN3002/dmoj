from django.contrib import admin
from funix.models.course import Course, CourseProblem, CourseSection, CourseTranslation, CourseSectionTranslation, CourseCategoryTranslation, CourseCategory
from django.forms import ModelForm
from judge.widgets import AdminMartorWidget

# category
class CourseCategoryTranslationInline(admin.StackedInline):
    model = CourseCategoryTranslation
    extra = 0
    
class CourseCategoryAdmin(admin.ModelAdmin):
    inlines = [CourseCategoryTranslationInline]

# section
class CourseSectionTranslationInline(admin.StackedInline):
    model = CourseSectionTranslation
    extra = 0

class CourseSectionAdmin(admin.ModelAdmin):
    inlines = [CourseSectionTranslationInline]

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


# course inline
class CourseForm(ModelForm):
    class Meta: 
        model = Course
        fields = "__all__"
        widgets = {
            'goals': AdminMartorWidget(),
        }
        
class CourseTranslationForm(ModelForm):
    class Meta: 
        model = CourseTranslation
        fields = "__all__"
        widgets = {
            'goals': AdminMartorWidget(),
        }

class CourseTranslationInline(admin.StackedInline):
    form = CourseTranslationForm
    model = CourseTranslation        
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    inlines = [CourseSectionInline, CourseProblemInline, CourseTranslationInline]
    





    




