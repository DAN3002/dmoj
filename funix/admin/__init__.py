from django.contrib import admin

from funix.models.problem import ProblemTestCaseData, ProblemInitialSource
from funix.models.course import CourseCategory, CourseRating, Course, CourseSection
from funix.admin.course import CourseAdmin, CourseCategoryAdmin, CourseSectionAdmin
from funix.models.profile import FunixProfile
from funix.models.submission import SuspiciousSubmissionBehavior, SubmissionWPM
from funix.admin.submission import SubmissionWPMInline, wpm_column
from funix.admin.problem import ProblemInitialSourceInline, ProblemTestCaseInline, ProblemTestCaseAdmin, ProblemTestCaseDataAdmin

from judge.admin.problem import ProblemAdmin
from judge.admin.submission import SubmissionAdmin
from judge.models.problem_data import ProblemTestCase


# Override judge.admin.ProblemAdmin
inlines = ProblemAdmin.inlines + [ProblemInitialSourceInline]

def get_inline_instances(self, request, obj=None):
    if obj and obj.allowed_languages.first().short_name in ['HTML', 'CSS']:
        self.inlines = inlines + [ProblemTestCaseInline]
    else:
        self.inlines = inlines
    return super(ProblemAdmin, self).get_inline_instances(request, obj)
    
delattr(ProblemAdmin, 'inlines')
# ProblemAdmin.inlines = inlines
# ProblemAdmin.inlines += [ProblemInitialSourceInline, ProblemTestCaseInline]
ProblemAdmin.get_inline_instances = get_inline_instances

# Override judge.admin.SubmissionAdmin
SubmissionAdmin.inlines += [SubmissionWPMInline]
SubmissionAdmin.wpm_column = wpm_column
del wpm_column

submission_admin_list_display = list(SubmissionAdmin.list_display)
submission_admin_list_display.insert(-2, "wpm_column")
SubmissionAdmin.list_display = submission_admin_list_display

# Register your models here.
admin.site.register(ProblemTestCaseData, ProblemTestCaseDataAdmin)
admin.site.register(SuspiciousSubmissionBehavior)
admin.site.register(ProblemInitialSource)
admin.site.register(SubmissionWPM)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(CourseSection, CourseSectionAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(FunixProfile)
admin.site.register(CourseRating)

admin.site.register(ProblemTestCase, ProblemTestCaseAdmin)