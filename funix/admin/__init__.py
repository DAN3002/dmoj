from django.contrib import admin

from funix.models.problem import ProblemTestCaseData, ProblemInitialSource
from funix.models.course import CourseCategory, CourseRating, Course
from funix.admin.course import CourseAdmin
from funix.models.profile import FunixProfile
from funix.models.submission import SuspiciousSubmissionBehavior, SubmissionWPM
from funix.admin.submission import SubmissionWPMInline, wpm_column

from judge.admin.problem import ProblemAdmin
from judge.admin.submission import SubmissionAdmin


# Override judge.admin.ProblemAdmin
from funix.admin.problem import ProblemInitialSourceInline
ProblemAdmin.inlines += [ProblemInitialSourceInline]

# Override judge.admin.SubmissionAdmin
SubmissionAdmin.inlines += [SubmissionWPMInline]
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
admin.site.register(CourseCategory)
admin.site.register(Course, CourseAdmin)
admin.site.register(FunixProfile)
admin.site.register(CourseRating)