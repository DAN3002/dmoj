from django.contrib import admin
from funix.models.submission import SubmissionWPM

# submission wpm inline
class SubmissionWPMInline(admin.TabularInline):
    model = SubmissionWPM

def wpm_column(self, obj):
    if obj.wpm:
        return obj.wpm.wpm
    else: 
        return -1
wpm_column.admin_order_field = 'wpm__wpm'
wpm_column.short_description = "WPM"




