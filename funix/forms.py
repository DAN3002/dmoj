from judge.forms import ProblemSubmitForm
from django.forms import CharField, HiddenInput, IntegerField

class BetaProblemSubmitForm(ProblemSubmitForm):
    suspicious_behaviors = CharField(max_length=256, initial="[]", widget = HiddenInput())
    wpm = CharField(initial="0",widget = HiddenInput())
