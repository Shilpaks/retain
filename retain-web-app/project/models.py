#!/usr/bin/env python

from flask import Flask

from wtforms import Form, BooleanField, IntegerField, StringField, PasswordField, validators, SelectField

from project import config

app = Flask(__name__)

# Create models from tables here

# Form models 

class ConceptSubmissionForm(Form):
    concept = StringField('Concept', [validators.Length(min=1, max=100), validators.required()])
    R_score = IntegerField('Retention Score', [validators.required()])
    C_score = IntegerField('Comprehension Score', [validators.required()])

class AddConceptSubmissionForm(Form):
    concept = StringField('Concept', [validators.required()])
    C_score = IntegerField('Comprehension Score', [validators.required()])


