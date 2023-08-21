from collections import namedtuple
from itertools import groupby
from operator import attrgetter
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import  ObjectDoesNotExist, PermissionDenied
from django.http import  HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _, gettext_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from judge import event_poster as event
from judge.models import Problem,  Submission
from judge.models.problem import SubmissionSourceAccess
from judge.utils.raw_sql import join_sql_subquery
from judge.utils.views import  TitleMixin, generic_message

from funix.models.course import Course, CourseProblem


def submission_related(queryset):
    return queryset.select_related('user__user', 'problem', 'language') \
        .only('id', 'user__user__username', 'user__display_rank', 'user__rating', 'problem__name',
              'problem__code', 'problem__is_public', 'language__short_name', 'language__key', 'date', 'time', 'memory',
              'points', 'result', 'status', 'case_points', 'case_total', 'current_testcase', 'contest_object',
              'locked_after', 'problem__submission_source_visibility_mode', 'user__username_display_override') \
        .prefetch_related('contest_object__authors', 'contest_object__curators')


class SubmissionPermissionDenied(PermissionDenied):
    def __init__(self, submission):
        self.submission = submission


class SubmissionMixin(object):
    model = Submission
    context_object_name = 'submission'
    pk_url_kwarg = 'submission'


class SubmissionDetailBase(LoginRequiredMixin, TitleMixin, SubmissionMixin, DetailView):
    def get_object(self, queryset=None):
        submission = super(SubmissionDetailBase, self).get_object(queryset)
        if not submission.can_see_detail(self.request.user):
            raise SubmissionPermissionDenied(submission)
        return submission

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except SubmissionPermissionDenied as e:
            return self.no_permission(e.submission)

    def no_permission(self, submission):
        problem = submission.problem
        if problem.is_accessible_by(self.request.user) and \
                problem.submission_source_visibility == SubmissionSourceAccess.SOLVED:

            message = escape(_('Permission denied. Solve %(problem)s in order to view it.')) % {
                'problem': format_html('<a href="{0}">{1}</a>',
                                       reverse('problem_detail', args=[problem.code]),
                                       problem.translated_name(self.request.LANGUAGE_CODE)),
            }
            return generic_message(self.request, _("Can't access submission"), mark_safe(message), status=403)
        else:
            return generic_message(self.request, _("Can't access submission"), _('Permission denied.'), status=403)

    def get_title(self):
        submission = self.object
        return _('Submission of %(problem)s by %(user)s') % {
            'problem': submission.problem.translated_name(self.request.LANGUAGE_CODE),
            'user': submission.user.display_name,
        }

    def get_content_title(self):
        submission = self.object
        return mark_safe(escape(_('Submission of %(problem)s by %(user)s')) % {
            'problem': format_html('<a href="{0}">{1}</a>',
                                   reverse('problem_detail', args=[submission.problem.code]),
                                   submission.problem.translated_name(self.request.LANGUAGE_CODE)),
            'user': format_html('<a href="{0}">{1}</a>',
                                reverse('user_page', args=[submission.user.user.username]),
                                submission.user.display_name),
        })


def make_batch(batch, cases):
    result = {'id': batch, 'cases': cases}
    if batch:
        result['points'] = min(map(attrgetter('points'), cases))
        result['total'] = max(map(attrgetter('total'), cases))
    return result


TestCase = namedtuple('TestCase', 'id status batch num_combined')


def get_statuses(batch, cases):
    cases = [TestCase(id=case.id, status=case.status, batch=batch, num_combined=1) for case in cases]
    if batch:
        # Get the first non-AC case if it exists.
        return [next((case for case in cases if case.status != 'AC'), cases[0])]
    else:
        return cases


def combine_statuses(status_cases, submission):
    ret = []
    # If the submission is not graded and the final case is a batch,
    # we don't actually know if it is completed or not, so just remove it.
    if not submission.is_graded and len(status_cases) > 0 and status_cases[-1].batch is not None:
        status_cases.pop()

    for key, group in groupby(status_cases, key=attrgetter('status')):
        group = list(group)
        if len(group) > 10:
            # Grab the first case's id so the user can jump to that case, and combine the rest.
            ret.append(TestCase(id=group[0].id, status=key, batch=None, num_combined=len(group)))
        else:
            ret.extend(group)
    return ret


def group_test_cases(cases):
    result = []
    status = []
    buf = []
    max_execution_time = 0.0
    last = None
    for case in cases:
        if case.time:
            max_execution_time = max(max_execution_time, case.time)
        if case.batch != last and buf:
            result.append(make_batch(last, buf))
            status.extend(get_statuses(last, buf))
            buf = []
        buf.append(case)
        last = case.batch
    if buf:
        result.append(make_batch(last, buf))
        status.extend(get_statuses(last, buf))
    return result, status, max_execution_time


class SubmissionStatus(SubmissionDetailBase):
    template_name = 'submission/status.html'

    def get_context_data(self, **kwargs):
        context = super(SubmissionStatus, self).get_context_data(**kwargs)
        submission = self.object
        context['last_msg'] = event.last()

        context['batches'], statuses, context['max_execution_time'] = group_test_cases(submission.test_cases.all())
        context['statuses'] = combine_statuses(statuses, submission)

        context['time_limit'] = submission.problem.time_limit
        try:
            lang_limit = submission.problem.language_limits.get(language=submission.language)
        except ObjectDoesNotExist:
            pass
        else:
            context['time_limit'] = lang_limit.time_limit
        return context


from funix.utils.problem import map_test_cases
class SubmissionTestCaseQueryBeta(SubmissionStatus):
    template_name = 'funix/submission/event-update-content.html'

    def get(self, request, *args, **kwargs):
        if 'id' not in request.GET or not request.GET['id'].isdigit():
            return HttpResponseBadRequest()
        self.kwargs[self.pk_url_kwarg] = kwargs[self.pk_url_kwarg] = int(request.GET['id'])
        return super(SubmissionTestCaseQueryBeta, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission = self.object
        problem = submission.problem
        context['problem'] = problem
        context['testcases_map'] = map_test_cases(problem.cases.all())
        context['is_html'] = problem.allowed_languages.first().short_name in ['HTML', 'CSS']
        context['just_judged'] = True
        
        # course
        context['course'] = None
        context['course_problem'] = None
        context['next_course_problem'] = None
        
        course_slug = self.kwargs.get("course")

        if course_slug:
            
            course = get_object_or_404(Course, slug=course_slug)
            
            course_problem = get_object_or_404(CourseProblem, course=course, problem=problem)
            
            next_course_problem = CourseProblem.objects.filter(course=course, number=course_problem.number + 1)
            
            context['next_course_problem'] = next_course_problem.first()
            
            context['course'] = course
            context['course_problem'] = course_problem
            
            
        return context

@require_POST
def abort_submission_beta(request, submission):
    submission = get_object_or_404(Submission, id=int(submission))
    if (not request.user.has_perm('judge.abort_any_submission') and
       (submission.rejudged_date is not None or request.profile != submission.user)):
        raise PermissionDenied()
    submission.abort()
    query = ''
    if request.GET.get('iframe') == '1':
        query = '?iframe=1'
    return HttpResponseRedirect(reverse('beta_problem', args=(submission.problem.code,)) + query)


def filter_submissions_by_visible_problems(queryset, user):
    join_sql_subquery(
        queryset,
        subquery=str(Problem.get_visible_problems(user).only('id').query),
        params=[],
        join_fields=[('problem_id', 'id')],
        alias='visible_problems',
        related_model=Problem,
    )




