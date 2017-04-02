#!/usr/bin/env python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField

from project import config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "%s://%s:%s@%s/%s" % (config.DBTYPE, config.DBUSER, config.DBPASS, config.DBHOST, config.DBNAME)
db = SQLAlchemy(app)

# Create models from tables here
class Tablename(db.Model):
    column_one = db.Column(db.Integer, primary_key=True)
    column_two = db.Column(db.String(80))

    def __init__(self, column_one, column_two):
        self.column_one = column_one
        self.column_two = column_two

    def __repr__(self):
        return '<Table %r>' % self.column_one

class ConceptSubmissionForm(Form):
    # concept = SelectField(u'', choices=())
    concept = StringField('Concept', [validators.Length(min=1, max=100)])
    R_score = StringField('Retention Score', [validators.Length(min=1, max=1)])
    C_score = StringField('Comprehension Score', [validators.Length(min=1, max=1)])

class AddConceptSubmissionForm(Form):
    # concept = SelectField(u'', choices=())
    concept = StringField('Concept', [validators.Length(min=1, max=100)])
    C_score = StringField('Comprehension Score', [validators.Length(min=1, max=1)])