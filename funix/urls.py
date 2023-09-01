from funix.views.problem import ProblemBeta, ProblemListBeta,ProblemCommentsBeta, BetaLanguageTemplateAjax
from funix.views.problem_data import beta_update_problem_data
from funix.views.submission import abort_submission_beta, SubmissionTestCaseQueryBeta
from django.urls import path, include
from judge.views.widgets import rejudge_submission
from funix.views.course import CourseListView, CourseDetailView, CourseEnrollView, CourseRatingView
from funix.views.auth import login_with_accesstoken


urlpatterns = [
    path('/problems', ProblemListBeta.as_view(), name='beta_problem_list'),
    path('/problem/<str:problem>', include([
        path('', ProblemBeta.as_view(), name='beta_problem'), 
        path('/comments', ProblemCommentsBeta.as_view(), name='beta_problem_comments'), 
        path('/submission/<int:submission>', ProblemBeta.as_view(), name='beta_problem'), 
        path('/data', beta_update_problem_data, name='beta_update_problem_data'), 
        
    ])),
    path('submission/<int:submission>', include([
        path('/abort', abort_submission_beta, name='beta_submission_abort'), 
    ])),
    path('widgets/', include([
        path('rejudge', rejudge_submission, name='beta_submission_rejudge'),
        path('submission_testcases', SubmissionTestCaseQueryBeta.as_view(), name='beta_submission_testcases_query'),
        path('submission_testcases/<slug:course>', SubmissionTestCaseQueryBeta.as_view(), name='beta_submission_testcases_query'),
        path('template', BetaLanguageTemplateAjax.as_view(), name="beta_language_template_ajax")
        ])
    ),
    # course
    path('/courses', CourseListView.as_view(), name="beta_course_list"),
    path('/course/<slug:course>', include([
        path('', CourseDetailView.as_view(), name="beta_course_detail"),
        path('/rating', CourseRatingView.as_view(), name="beta_course_rating"),
        path('/problem/<str:problem>', ProblemBeta.as_view(), name="beta_problem"),
        path('/problem/<str:problem>/submission/<int:submission>', ProblemBeta.as_view(), name="beta_problem"),
        path('/enroll', CourseEnrollView.as_view(), name="beta_course_enroll"),
    ])),
    path('/login', login_with_accesstoken, name="beta_login_with_accesstoken")
]