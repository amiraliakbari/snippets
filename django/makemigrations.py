""" Replacement for manage.py makemigrations command,
     modified to ignore changes in fields like help_text.
     
     Note: for full discussion of why this is not the default behavior
      in Django, see: https://code.djangoproject.com/ticket/21498
     
    source: http://stackoverflow.com/a/39801321/462865
"""
from django.core.management.commands.makemigrations import Command
from django.db import models

__all__ = ['Command']

IGNORED_ATTRS = ['verbose_name', 'help_text', 'related_name', 'choices']

original_deconstruct = models.Field.deconstruct

def new_deconstruct(self):
    name, path, args, kwargs = original_deconstruct(self)
    for attr in IGNORED_ATTRS:
        kwargs.pop(attr, None)
    return name, path, args, kwargs

models.Field.deconstruct = new_deconstruct
