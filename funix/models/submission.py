from django.db import models
from judge.models.submission import Submission

class SuspiciousSubmissionBehavior(models.Model):
    submission = models.ForeignKey(Submission, verbose_name="Suspicious Submission Behavior", related_name="suspicous_behaviors", on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name="Suspicious Behavior Time")
    
    def __str__(self): 
        return f"{self.submission.user.username} - {self.submission.problem.name} - {self.submission.id} - {self.time}"

class SubmissionWPM(models.Model): 
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name="wpm")
    wpm = models.IntegerField(verbose_name="Words Per Minutes", default=-1, null=True)
    
    def __str__(self): 
        return "{} wpm".format(str(self.wpm))
    
