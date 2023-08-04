from django.db import models
from judge.models.problem import Problem
from datetime import date
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

class CourseCategory(models.Model):
    name = models.CharField(verbose_name="Course Category", max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self): 
        return self.name

class Course(models.Model):
    author = models.ForeignKey(User,verbose_name="Author", related_name="courses", on_delete=models.DO_NOTHING)
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

class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(verbose_name="Section Name", max_length=255, unique=True)
    number = models.IntegerField()

    class Meta:
        unique_together = ['name', 'number', 'course']
        
    def __str__(self):
        return f'{self.course.name} - {self.name}'
    

class CourseProblem(models.Model):
    problem = models.ForeignKey(Problem, related_name="course_problems", on_delete=models.CASCADE)
    section = models.ForeignKey(CourseSection, related_name="problems", on_delete=models.CASCADE)
    number = models.IntegerField()
    time = models.IntegerField(default=0)
    course = models.ForeignKey(Course, related_name="course_problems", on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['problem', 'course', 'number']
        permissions = [("view_course_problem", "User can view the problem if enrolled"),]        

    def has_permission(self, user):
        if user.is_authenticated and user.funix:
            return self.section.course in user.funix.courses.all()
            
        return False
    
    def save(self, *args, **kwargs):
        self.problem.is_public = False
        self.problem.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.section.course.name} - {self.section.name} - {self.problem.name} - {self.number}"

def validate_rating(value):
        if not 1 <= value <= 5:
            raise ValidationError("Rating must be between 1 and 5")
    
class CourseRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[validate_rating], default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('course', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.course.name} - {self.rating}"

class CourseTranslation(models.Model):
    course = models.ForeignKey(Course, verbose_name='course', related_name='translations', on_delete=models.CASCADE)
    language = models.CharField(verbose_name='language', max_length=7, choices=settings.LANGUAGES)
    name = models.CharField(verbose_name='translated name', max_length=100, db_index=True)
    description = models.TextField(verbose_name='translated description')
    goals = models.TextField(verbose_name="translated goals")
    
    class Meta:
        unique_together = ('course', 'language')
        verbose_name = 'course translation'
        verbose_name_plural = 'course translations'
        
class CourseSectionTranslation(models.Model):
    course_section = models.ForeignKey(CourseSection, verbose_name='course section', related_name='translations', on_delete=models.CASCADE)
    language = models.CharField(verbose_name='language', max_length=7, choices=settings.LANGUAGES)
    name = models.CharField(verbose_name='translated name', max_length=255, db_index=True)
    
    class Meta:
        unique_together = ('course_section', 'language')
        verbose_name = 'course section translation'
        verbose_name_plural = 'course section translations'
        
class CourseCategoryTranslation(models.Model):
    course_category = models.ForeignKey(CourseCategory, verbose_name='course category', related_name='translations', on_delete=models.CASCADE)
    language = models.CharField(verbose_name='language', max_length=7, choices=settings.LANGUAGES)
    name = models.CharField(verbose_name='translated name', max_length=255, db_index=True)
    
    class Meta:
        unique_together = ('course_category', 'language')
        verbose_name = 'course category translation'
        verbose_name_plural = 'course category translations'
        
