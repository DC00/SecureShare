import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from django.conf import settings



from django.utils import timezone
from secureshare.models import Report, Reporter, Group, Message, Membership

import string
import random

def random_text(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def random_digits(size=6, digits=string.digits):
    return ''.join(random.choice(digits) for _ in range(size))

def random_sentence(words=3):
    sentence = ""
    for i in range(words):
        sentence += random_text(random.randint(4, 10)) + " "
    return sentence

def random_paragraph(sentences=4):
    paragraph = ""
    for i in range(sentences):
        paragraph += random_sentence(random.randint(3, 8)) + " "
    return paragraph


# Make Reporters. In this loop, each reporter has one report
for i in range(25):
    _reporter = Reporter(created_at=timezone.now(), first_name=random_text(), last_name=random_text())
    _reporter.save()
    _report = Report(created_at=timezone.now(), description=random_sentence(), full_description=random_paragraph(), reporter_it_belongs_to=_reporter, is_private=True)
    _report.save()


# Make three groups
g1 = Group(name="Vox Media")
g2 = Group(name="Politico")
g3 = Group(name="Hacker News")
g1.save()
g2.save()
g3.save()


# Assign 5 random reporters to each group
for i in range(5):
    m1 = Membership(reporter=Reporter.objects.order_by('?').first(), group=g1)
    m2 = Membership(reporter=Reporter.objects.order_by('?').first(), group=g2)
    m3 = Membership(reporter=Reporter.objects.order_by('?').first(), group=g3)
    m1.save()
    m2.save()
    m3.save()

    