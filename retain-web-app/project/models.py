#!/usr/bin/env python

from flask import Flask

from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField

from project import config

app = Flask(__name__)

# Create models from tables here

# Form models 

class ConceptSubmissionForm(Form):
    concept = StringField('Concept', [validators.Length(min=1, max=100)])
    R_score = StringField('Retention Score', [validators.Length(min=1, max=1)])
    C_score = StringField('Comprehension Score', [validators.Length(min=1, max=1)])

class AddConceptSubmissionForm(Form):
    concept = StringField('Concept', [validators.Length(min=1, max=100)])
    C_score = StringField('Comprehension Score', [validators.Length(min=1, max=1)])

