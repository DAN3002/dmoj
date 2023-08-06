from django import http
from django.http import HttpResponseForbidden
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from funix.models.profile import FunixProfile
from funix.models.course import Course, CourseCategory, CourseSection,CourseProblem, CourseRating, CourseTranslation
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from django.urls import reverse
from judge.models.submission import Submission
from django.db.models import Max, Avg
from judge.utils.views import generic_message

class CourseListView(ListView):
    model = CourseCategory
    template_name = "funix/course/list.html"
    context_object_name = 'categories'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related('translations')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        for object in context[self.context_object_name]:
            translation = object.translations.filter(language=self.request.LANGUAGE_CODE).first()
            if translation:
                setattr(object, 'name', translation.name)
        
        context["title"] = "Courses"
        categories = context[self.context_object_name]
        average_points = {}
        votes = {}
        total_times={}
        student_counts = {}
        problem_counts = {}
        enrolleds ={}
        progress_percentages = {}
        course_translations = {}
        for category in categories:
            for course in category.courses.all():
                average_points[course.id] = CourseRating.objects.filter(course=course).aggregate(Avg('rating'))['rating__avg'] or 0
                votes[course.id] =  CourseRating.objects.filter(course=course).count()
                student_counts[course.id] = course.funixprofile_set.all().count()
                problem_counts[course.id] = course.sections.annotate(problem_count=models.Count('problems')).aggregate(models.Sum('problem_count'))['problem_count__sum'] or 0
                total_times[course.id] = 0 if problem_counts[course.id] == 0 else course.sections.aggregate(models.Sum('problems__time'))['problems__time__sum']
                if self.request.user.is_authenticated:
                    if hasattr(self.request.user, "funix"):
                        funix_profile = self.request.user.funix
                        if course in funix_profile.courses.all():
                            enrolleds[course.id] = True
                        else: 
                            enrolleds[course.id] = False
                        
                # progress 
                sections = CourseSection.objects.filter(course=course)
                course_problems = CourseProblem.objects.filter(section__in=sections)
                correct_problems_count = 0
                for course_problem in course_problems:
                    problem = course_problem.problem
                    latest_submission = Submission.objects.filter(problem=problem).aggregate(Max('id'))
                    if latest_submission["id__max"]:
                        latest_submission = Submission.objects.get(id=latest_submission["id__max"])
                        if latest_submission.result == "AC":
                            correct_problems_count += 1
                progress_percentages[course.id] = 0 if problem_counts[course.id] == 0 else round(correct_problems_count / problem_counts[course.id] * 100)

                # course translation
                try:
                    course_translation = course.translations.get(language=self.request.LANGUAGE_CODE)
                except CourseTranslation.DoesNotExist:
                    course_translations[course.id] = {
                        "name": course.name,
                        "description": course.description,
                    }
                else:
                    course_translations[course.id] = {
                        "name": course_translation.name,
                        "description": course_translation.description,
                    }
                
        context["average_points"] = average_points
        context["votes"] = votes
        context["student_counts"] = student_counts
        context["problem_counts"] = problem_counts
        context["total_times"] = total_times
        context["enrolleds"] = enrolleds
        context["progress_percentages"] = progress_percentages
        context["course_translations"] = course_translations
        
        return context
        
class CourseSectionView(ListView):
    pass

class CourseDetailView(DetailView):
    model = Course
    slug_url_kwarg = 'course'
    template_name = "funix/course/detail.html"
    
    def get(self, request, *args, **kwargs):
        try:
            return super(CourseDetailView, self).get(request, *args, **kwargs)
        except http.Http404:
            return generic_message(self.request, "Course Not Found", f"Could not found the course with slug {self.kwargs.get('course')}", status=404)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        
        # get total problem count
        context["problem_count"] = self.object.sections.annotate(problem_count=models.Count('problems')).aggregate(models.Sum('problem_count'))['problem_count__sum'] or 0
        context["total_users"] = self.object.funixprofile_set.all().count()
        total_time = 0 if context["problem_count"] == 0 else self.object.sections.aggregate(models.Sum('problems__time'))['problems__time__sum']
        if total_time < 60:
            total_time = str(total_time) + 'm'
        else:
            total_time = str(round(total_time * 10 / 60) / 10) + "hr"
        context["total_time"] = total_time

        # get all problem with latest submission
        latest_submissions = {}
        course = self.object
        sections = CourseSection.objects.filter(course=course)
        course_problems = CourseProblem.objects.filter(section__in=sections)
        
        correct_problems_count = 0
        
        if self.request.user.is_authenticated:
            for course_problem in course_problems:
                problem = course_problem.problem
                latest_submission = Submission.objects.filter(problem=problem, user=self.request.user.profile).aggregate(Max('id'))
                if latest_submission["id__max"]:
                    latest_submission = Submission.objects.get(id=latest_submission["id__max"], user=self.request.user.profile)
                    if latest_submission.result == "AC":
                        correct_problems_count += 1
                else: 
                    latest_submission = None
                latest_submissions[problem.id] = latest_submission

        context["latest_submissions"] = latest_submissions
        context["process_percentage"] = 0 if context["problem_count"] == 0 else round(correct_problems_count / context["problem_count"] * 100)
        
        # enroll
        context["enrolled"] = False
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, "funix"):
                funix_profile = self.request.user.funix
                if self.object in funix_profile.courses.all():
                    context["enrolled"] = True
                
                
        # rating
        context["average_rating"] = round(CourseRating.objects.filter(course=self.object).aggregate(Avg('rating'))['rating__avg'] or 0)
        
        # course translations
        course_translation = self.object.translations.filter(language=self.request.LANGUAGE_CODE).first()
        if course_translation:
            setattr(self.object, 'name', course_translation.name)
            setattr(self.object, 'description', course_translation.description)
            setattr(self.object, 'goals', course_translation.goals)
        
        # section translations
        section_translations = {}
        for section in self.object.sections.all():
            section_translations[section.id] = {
                "name": section.name
            }
            section_translation = section.translations.filter(language=self.request.LANGUAGE_CODE).first()

            if section_translation:
                section_translations[section.id]["name"] = section_translation.name
        
        context["section_translations"] = section_translations
        
        # seo
        context["og_image"] = self.object.og_image if self.object.og_image else self.object.thumbnail.url
        context["meta_description"] = self.object.description
        return context

class CourseEnrollView(RedirectView):
    def post(self, request, *args, **kwargs):
        user = request.user

        # not authenticated => 404
        if not user.is_authenticated:
            return http.Http404()
        
        funix_profile, created = FunixProfile.objects.get_or_create(user=user)
        course = get_object_or_404(Course, slug=self.kwargs.get("course"))

        # already enrolled but still enroll again => hack => warn
        if course in funix_profile.courses.all(): 
            return HttpResponseForbidden(format_html('<h1>You have already enrolled. Do you want me to ban you?</h1>'))
        else:
            funix_profile.courses.add(course)
        return super().post(request, *args, **kwargs)
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse("beta_course_detail", args=[self.kwargs.get("course")])
    

class CourseRatingView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("beta_course_detail", args=[self.kwargs.get("course")])

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return HttpResponseForbidden()
        
        course = get_object_or_404(Course, slug=request.POST.get("course"))
        sections = CourseSection.objects.filter(course=course)
        course_problems = CourseProblem.objects.filter(section__in=sections)

        problem_count = course.sections.annotate(problem_count=models.Count('problems')).aggregate(models.Sum('problem_count'))['problem_count__sum'] or 0
        correct_problems_count = 0
        
        if self.request.user.is_authenticated:
            for course_problem in course_problems:
                problem = course_problem.problem
                latest_submission = Submission.objects.filter(problem=problem, user=self.request.user.profile).aggregate(Max('id'))
                if latest_submission["id__max"]:
                    latest_submission = Submission.objects.get(id=latest_submission["id__max"], user=self.request.user.profile)
                    if latest_submission.result == "AC":
                        correct_problems_count += 1
                
        progress_percentage = 0 if problem_count == 0 else round(correct_problems_count / problem_count * 100)
        if progress_percentage < 70: 
            pass
            # return HttpResponseForbidden()
        
        star = request.POST.get("star")
        
        

        
        try:
            rating = CourseRating.objects.get(user=user, course=course)
            rating.rating = int(star)
        except CourseRating.DoesNotExist:
            rating = CourseRating.objects.create(user=user, course=course, rating=int(star))
        rating.save()
        return super().post(request, *args, **kwargs)
    

