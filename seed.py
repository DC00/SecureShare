import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from django.conf import settings



from django.utils import timezone
from secureshare.models import Report

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

for i in range(25):
    r = Report(created_at=timezone.now(), description=random_sentence(), full_description=random_paragraph())
    r.save()
