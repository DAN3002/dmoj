from django.db import models
from judge.models.problem_data import ProblemTestCase
from judge.models.problem import Problem
from judge.models.submission import Submission
from zipfile import ZipFile
from judge.models.runtime import Language

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