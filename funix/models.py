from django.db import models
from judge.models.problem_data import ProblemTestCase
from judge.models.problem import Problem
from judge.models.submission import Submission
from judge.models.profile  import Profile
from zipfile import ZipFile
from judge.models.runtime import Language
from datetime import date
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime


# Create your models here.
class ProblemTestCaseData(models.Model):
    problem_test_case = models.OneToOneField(ProblemTestCase, on_delete=models.CASCADE, related_name='data')
    input_data = models.TextField(verbose_name='input', blank=True)
    output_data = models.TextField(verbose_name='expected output', blank=True)

def save(self, *args, **kwargs):
    super(ProblemTestCase, self).save(*args, **kwargs)
    
    if self.is_pretest == True and ((self.input_file != '' and self.input_file is not None) or (self.output_file != '' and self.output_file is not None)):
        problem = Problem.objects.get(cases=self)
        archive = ZipFile(problem.data_files.zipfile.path, 'r')
        try:
            test_case_data = ProblemTestCaseData.objects.get(problem_test_case=self)
        except ProblemTestCaseData.DoesNotExist:
            test_case_data = ProblemTestCaseData.objects.create(problem_test_case=self)
    
        if self.input_file != '':
            test_case_data.input_data = archive.read(self.input_file).decode('utf-8')
        if self.output_file != '':
            test_case_data.output_data = archive.read(self.output_file).decode('utf-8')
        test_case_data.save()

ProblemTestCase.save = save
del save


class SuspiciousSubmissionBehavior(models.Model):
    submission = models.ForeignKey(Submission, verbose_name="Suspicious Submission Behavior", related_name="suspicous_behaviors", on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name="Suspicious Behavior Time")
    
    def __str__(self): 
        return f"{self.submission.user.username} - {self.submission.problem.name} - {self.submission.id} - {self.time}"
    
class ProblemInitialSource(models.Model): 
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="initial_codes")
    source = models.TextField(verbose_name="Problem Initial Source", max_length=65536, default="", blank=True)
    language = models.ForeignKey(Language, verbose_name="Initial Source Language", on_delete=models.CASCADE, related_name="initial_codes",  null=True)
    
    class Meta:
        unique_together = ('problem', 'language')
        
class SubmissionWPM(models.Model): 
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name="wpm")
    wpm = models.IntegerField(verbose_name="Words Per Minutes", default=-1, null=True)
    
    def __str__(self): 
        return "{} wpm".format(str(self.wpm))
    
# course category
class CourseCategory(models.Model):
    name = models.CharField(verbose_name="Course Category", max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self): 
        return self.name

# course
class Course(models.Model):
    author = models.ForeignKey(Profile,verbose_name="Author", related_name="courses", on_delete=models.DO_NOTHING)
    goals = models.TextField(verbose_name="Goals")
    free = models.BooleanField(verbose_name="Is Free", default=False)
    name = models.CharField(verbose_name="Course Name", max_length=255, unique=True)
    description = models.TextField(verbose_name="Course Description", max_length=1000)
    certificate = models.CharField(verbose_name="Course Certificate", max_length=225,blank=True, default="")
    og_image = models.CharField(verbose_name="Og Image", max_length=255, blank=True)
    summary = models.TextField(verbose_name="Course Summary", blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(blank=True)
    slug = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(CourseCategory, related_name="courses", on_delete=models.CASCADE, null=True)
    thumbnail = models.ImageField(default='default.jpg')
    
    def save(self, *args, **kwargs) -> None:
        self.updated_at = date.today()
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# CourseSection
class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(verbose_name="Section Name", max_length=255, unique=True)
    number = models.IntegerField()

    class Meta:
        unique_together = ['name', 'number', 'course']
        
    def __str__(self):
        return self.course.name + " - " + self.name + " - " + str(self.number)
    

# course problem
class CourseProblem(models.Model):
    problem = models.ForeignKey(Problem, related_name="course_problems", on_delete=models.CASCADE)
    section = models.ForeignKey(CourseSection, related_name="problems", on_delete=models.CASCADE)
    number = models.IntegerField()
    time = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['problem', 'section', 'number']
        permissions = [("view_course_problem", "User can view the problem if enrolled"),]        

    def has_permission(self, user):
        if user.is_authenticated and user.funix:
            return self.section.course in user.funix.courses.all()
            
        return False

    def __str__(self):
        return f"{self.section.course.name} - {self.section.name} - {self.problem.name} - {self.number}"

# funix profile
class FunixProfile(models.Model):
    profile = models.OneToOneField(Profile,verbose_name="Funix Profile", related_name="funix", on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    
# course rating
def validate_rating(value):
    if not 1 <= value <= 5:
        raise ValidationError("Rating must be between 1 and 5")
    
class CourseRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[validate_rating])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('course', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.course.name} - {self.rating}"

# course comment
class CourseComment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.username} - {self.text[:50]}"

    def approve(self):
        self.is_approved = True
        self.save()

    def unapprove(self):
        self.is_approved = False
        self.save()
    
    def has_parent(self):
        return self.parent is not None
