import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import transaction
from django.db.models import Prefetch
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _, gettext_lazy
import json
from funix.models import SuspiciousSubmissionBehavior
import datetime

from funix.forms import BetaProblemSubmitForm as ProblemSubmitForm
from judge.models import ContestSubmission, Judge, Language, Problem,  RuntimeVersion, Submission, SubmissionSource
from judge.utils.problems import contest_attempted_ids, contest_completed_ids,  user_attempted_ids, \
    user_completed_ids
from judge.utils.views import SingleObjectFormView, TitleMixin, generic_message
from django.views.generic import View
from judge.models.runtime import Language
from funix.models import ProblemInitialSource, SubmissionWPM

def get_contest_problem(problem, profile):
    try:
        return problem.contests.get(contest_id=profile.current_contest.contest_id)
    except ObjectDoesNotExist:
        return None


def get_contest_submission_count(problem, profile, virtual):
    return profile.current_contest.submissions.exclude(submission__status__in=['IE']) \
                  .filter(problem__problem=problem, participation__virtual=virtual).count()


class ProblemMixin(object):
    model = Problem
    slug_url_kwarg = 'problem'
    slug_field = 'code'

    def get_object(self, queryset=None):
        problem = super(ProblemMixin, self).get_object(queryset)
        if not problem.is_accessible_by(self.request.user):
            raise Http404()
        return problem

    def no_such_problem(self):
        code = self.kwargs.get(self.slug_url_kwarg, None)
        return generic_message(self.request, _('No such problem'),
                               _('Could not find a problem with the code "%s".') % code, status=404)

    def get(self, request, *args, **kwargs):
        try:
            return super(ProblemMixin, self).get(request, *args, **kwargs)
        except Http404:
            return self.no_such_problem()


class SolvedProblemMixin(object):
    def get_completed_problems(self):
        if self.in_contest:
            return contest_completed_ids(self.profile.current_contest)
        else:
            return user_completed_ids(self.profile) if self.profile is not None else ()

    def get_attempted_problems(self):
        if self.in_contest:
            return contest_attempted_ids(self.profile.current_contest)
        else:
            return user_attempted_ids(self.profile) if self.profile is not None else ()

    @cached_property
    def in_contest(self):
        return self.profile is not None and self.profile.current_contest is not None

    @cached_property
    def contest(self):
        return self.request.profile.current_contest.contest

    @cached_property
    def profile(self):
        if not self.request.user.is_authenticated:
            return None
        return self.request.profile

user_logger = logging.getLogger('judge.user')

from judge import event_poster as event
from operator import attrgetter
from collections import namedtuple
from itertools import groupby

# these function were copied from views/submission.py
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

# uuuuvcomment 
def is_anonymous(self):
    return self.request.user.is_anonymous


from funix.utils.problem import map_test_cases
class ProblemBeta(ProblemMixin, TitleMixin, SingleObjectFormView):
    template_name = 'funix/problem/problem.html'
    form_class = ProblemSubmitForm

    @cached_property
    def contest_problem(self):
        if (is_anonymous(self)):
            return None
        
        if self.request.profile.current_contest is None:
            return None
        return get_contest_problem(self.object, self.request.profile)

    @cached_property
    def remaining_submission_count(self):
        if (is_anonymous(self)):
            return None

        max_subs = self.contest_problem and self.contest_problem.max_submissions
        if max_subs is None:
            return None
        # When an IE submission is rejudged into a non-IE status, it will count towards the
        # submission limit. We max with 0 to ensure that `remaining_submission_count` returns
        # a non-negative integer, which is required for future checks in this view.
        return max(
            0,
            max_subs - get_contest_submission_count(
                self.object, self.request.profile, self.request.profile.current_contest.virtual,
            ),
        )

    @cached_property
    def default_language(self):
        # If the old submission exists, use its language, otherwise use the user's default language.
        if self.old_submission is not None:
            return self.old_submission.language
        
        if not self.request.user.is_anonymous:
            return self.request.profile.language

    def get_content_title(self):
        return mark_safe(
            escape(_('Submit to %s')) % format_html(
                '<a href="{0}">{1}</a>',
                reverse('problem_detail', args=[self.object.code]),
                self.object.translated_name(self.request.LANGUAGE_CODE),
            ),
        )

    def get_title(self):
        return _('Submit to %s') % self.object.translated_name(self.request.LANGUAGE_CODE)

    def get_initial(self):
        initial = {'language': self.default_language}
        if self.old_submission is not None:
            initial['source'] = self.old_submission.source.source
        self.initial = initial
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Submission(user=self.request.profile, problem=self.object)

        if self.object.is_editable_by(self.request.user):
            kwargs['judge_choices'] = tuple(
                Judge.objects.filter(online=True, problems=self.object).values_list('name', 'name'),
            )
        else:
            kwargs['judge_choices'] = ()

        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_anonymous:
            form.fields['language'].queryset = (
                self.object.usable_languages.order_by('name', 'key')
                .prefetch_related(Prefetch('runtimeversion_set', RuntimeVersion.objects.order_by('priority')))
            )

            form_data = getattr(form, 'cleaned_data', form.initial)
            if 'language' in form_data:
                form.fields['source'].widget.mode = form_data['language'].ace
            form.fields['source'].widget.theme = self.request.profile.resolved_ace_theme

        return form

    def get_success_url(self):
        return reverse('beta_problem', kwargs=({
            "problem": self.new_submission.problem.code,
            "submission": self.new_submission.id,
        })) + "?iframe={}".format(self.request.GET.get('iframe'))

    def form_valid(self, form):
        if (is_anonymous(self)):
            return super().form_valid(form)

        if (
            not self.request.user.has_perm('judge.spam_submission') and
            Submission.objects.filter(user=self.request.profile, rejudged_date__isnull=True)
                              .exclude(status__in=['D', 'IE', 'CE', 'AB']).count() >= settings.DMOJ_SUBMISSION_LIMIT
        ):
            return HttpResponse(format_html('<h1>{0}</h1>', _('You submitted too many submissions.')), status=429)
        if not self.object.allowed_languages.filter(id=form.cleaned_data['language'].id).exists():
            raise PermissionDenied()
        if not self.request.user.is_superuser and self.object.banned_users.filter(id=self.request.profile.id).exists():
            return generic_message(self.request, _('Banned from submitting'),
                                   _('You have been declared persona non grata for this problem. '
                                     'You are permanently barred from submitting to this problem.'))
        # Must check for zero and not None. None means infinite submissions remaining.
        if self.remaining_submission_count == 0:
            return generic_message(self.request, _('Too many submissions'),
                                   _('You have exceeded the submission limit for this problem.'))

        with transaction.atomic():
            self.new_submission = form.save(commit=False)

            contest_problem = self.contest_problem
            if contest_problem is not None:
                # Use the contest object from current_contest.contest because we already use it
                # in profile.update_contest().
                self.new_submission.contest_object = self.request.profile.current_contest.contest
                if self.request.profile.current_contest.live:
                    self.new_submission.locked_after = self.new_submission.contest_object.locked_after
                self.new_submission.save()
                ContestSubmission(
                    submission=self.new_submission,
                    problem=contest_problem,
                    participation=self.request.profile.current_contest,
                ).save()
            else:
                self.new_submission.save()

            source = SubmissionSource(submission=self.new_submission, source=form.cleaned_data['source'])
            source.save()

        # Save a query.
        self.new_submission.source = source
        self.new_submission.judge(force_judge=True, judge_id=form.cleaned_data['judge'])

        # uuuuvcomment suspicious behaviors
        suspicious_behaviors = json.loads(form.cleaned_data['suspicious_behaviors'])
        if len(suspicious_behaviors) > 0:
            for timestamp in suspicious_behaviors: 
                SuspiciousSubmissionBehavior.objects.create(submission= self.new_submission, time=datetime.datetime.fromtimestamp(timestamp))


        # uuuuvcomment wpm
        wpm = int(json.loads(form.cleaned_data['wpm']))
        SubmissionWPM.objects.create(submission=self.new_submission, wpm=wpm)
        
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Http404:
            # Is this really necessary? This entire post() method could be removed if we don't log this.
            user_logger.info(
                'Naughty user %s wants to submit to %s without permission',
                request.user.username,
                kwargs.get(self.slug_url_kwarg),
            )
            return HttpResponseForbidden(format_html('<h1>{0}</h1>', _('Do you want me to ban you?')))

    def dispatch(self, request, *args, **kwargs):
        submission_id = kwargs.get('submission')
        problem_code = kwargs.get('problem')
        problem = get_object_or_404(Problem, code=problem_code)
        self.old_submission = None

        if submission_id is not None:
            self.old_submission = get_object_or_404(
                Submission.objects.select_related('source', 'language'),
                id=submission_id,
            )

            if not self.old_submission.can_see_detail(request.user):
                # raise SubmissionPermissionDenied(submission) # uuuuvcomment
                raise PermissionDenied()
            
            if not request.user.has_perm('judge.resubmit_other') and self.old_submission.user != request.profile:
                raise PermissionDenied()
        else:
            if not self.request.user.is_anonymous:
                submissions = Submission.objects.filter(user=self.request.user.profile,problem=problem).order_by('-date')
                if submissions.count() > 0:
                    self.old_submission = submissions[0]

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['langs'] = Language.objects.all()
        context['no_judges'] = not context['form'].fields['language'].queryset
        context['submission_limit'] = self.contest_problem and self.contest_problem.max_submissions
        context['submissions_left'] = self.remaining_submission_count
        context['ACE_URL'] = settings.ACE_URL
        context['default_lang'] = self.default_language
        problem = context['problem']
        
        context['testcases_map'] = map_test_cases(problem.cases.all())

        context['iframe'] = self.request.GET.get('iframe')
        submission = self.old_submission
        context['old_submission'] = self.initial

        if submission is not None:
            context['submission'] = submission

            # submission status 
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
    

# ------------------------------------------------------------------------------
from judge.views.problem import ProblemList

class ProblemListBeta(ProblemList):
    template_name = 'funix/problem/list.html'

    def get_context_data(self, **kwargs):
        context = super(ProblemListBeta, self).get_context_data(**kwargs)
        context['iframe'] = self.request.GET.get('iframe')
        context['problem'] = None
        return context
    
# -----------------------------------------------------------------------------------
from judge.comments import CommentedDetailView
from judge.models import ContestSubmission, Judge, Language, Problem, ProblemPointsVote, \
    ProblemTranslation,  RuntimeVersion, Solution, Submission, SubmissionSource
from judge.utils.opengraph import generate_opengraph
from judge.utils.pdfoid import PDF_RENDERING_ENABLED
from judge.utils.tickets import own_ticket_filter

class ProblemCommentsBeta(ProblemMixin, SolvedProblemMixin, CommentedDetailView):
    context_object_name = 'problem'
    template_name = 'funix/comment/comments.html'

    def get_comment_page(self):
        return 'p:%s' % self.object.code

    def get_context_data(self, **kwargs):
        context = super(ProblemCommentsBeta, self).get_context_data(**kwargs)
        user = self.request.user
        authed = user.is_authenticated
        context['has_submissions'] = authed and Submission.objects.filter(user=user.profile,
                                                                          problem=self.object).exists()
        contest_problem = (None if not authed or user.profile.current_contest is None else
                           get_contest_problem(self.object, user.profile))
        context['contest_problem'] = contest_problem
        if contest_problem:
            clarifications = self.object.clarifications
            context['has_clarifications'] = clarifications.count() > 0
            context['clarifications'] = clarifications.order_by('-date')
            context['submission_limit'] = contest_problem.max_submissions
            if contest_problem.max_submissions:
                context['submissions_left'] = max(contest_problem.max_submissions -
                                                  get_contest_submission_count(self.object, user.profile,
                                                                               user.profile.current_contest.virtual), 0)

        context['available_judges'] = Judge.objects.filter(online=True, problems=self.object)
        context['show_languages'] = self.object.allowed_languages.count() != Language.objects.count()
        context['has_pdf_render'] = PDF_RENDERING_ENABLED
        context['completed_problem_ids'] = self.get_completed_problems()
        context['attempted_problems'] = self.get_attempted_problems()

        can_edit = self.object.is_editable_by(user)
        context['can_edit_problem'] = can_edit
        if user.is_authenticated:
            tickets = self.object.tickets
            if not can_edit:
                tickets = tickets.filter(own_ticket_filter(user.profile.id))
            context['has_tickets'] = tickets.exists()
            context['num_open_tickets'] = tickets.filter(is_open=True).values('id').distinct().count()

        try:
            context['editorial'] = Solution.objects.get(problem=self.object)
        except ObjectDoesNotExist:
            pass
        try:
            translation = self.object.translations.get(language=self.request.LANGUAGE_CODE)
        except ProblemTranslation.DoesNotExist:
            context['title'] = self.object.name
            context['language'] = settings.LANGUAGE_CODE
            context['description'] = self.object.description
            context['translated'] = False
        else:
            context['title'] = translation.name
            context['language'] = self.request.LANGUAGE_CODE
            context['description'] = translation.description
            context['translated'] = True

        if not self.object.og_image or not self.object.summary:
            metadata = generate_opengraph('generated-meta-problem:%s:%d' % (context['language'], self.object.id),
                                          context['description'], 'problem')
        context['meta_description'] = self.object.summary or metadata[0]
        context['og_image'] = self.object.og_image or metadata[1]

        context['vote_perm'] = self.object.vote_permission_for_user(user)
        if context['vote_perm'].can_vote():
            try:
                context['vote'] = ProblemPointsVote.objects.get(voter=user.profile, problem=self.object)
            except ObjectDoesNotExist:
                context['vote'] = None
        else:
            context['vote'] = None
        context['iframe'] = self.request.GET.get('iframe')
        return context


class BetaLanguageTemplateAjax(View):
    def get(self, request, *args, **kwargs):
        initial_source = ProblemInitialSource.objects.filter(language=int(request.GET.get('id', 0)), problem=int(request.GET.get('problem_code', -1)))
        if len(initial_source) > 0:
            return HttpResponse(initial_source[0].source, content_type='text/plain')
        else:
            try:
                language = get_object_or_404(Language, id=int(request.GET.get('id', 0)))
            except ValueError:
                raise Http404()
            return HttpResponse(language.template, content_type='text/plain')

