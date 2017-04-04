#!/usr/bin/env python

from flask import Flask, flash, redirect, url_for
from flask import request
from flask import render_template

from project import config
from project.models import *
from project.controllers import hello

import user

app = Flask(__name__)
app.secret_key = 'some_secret'

print "start"
sr_user = user.User("shilpa", "subrahm2@illinois.edu")

# All views below
@app.route("/",  methods=['GET', 'POST'])
def index():
    form = ConceptSubmissionForm(request.form)
    if request.method == 'POST' and form.validate():
        print "before", sr_user.sr_instance.concept_next_time_dict
        revisit_status = sr_user.sr_instance.revisit_concept(form.concept.data, form.C_score.data, form.R_score.data)
        print "next_time_dict", sr_user.sr_instance.concept_next_time_dict
        print "comp dict", sr_user.sr_instance.concept_comprehension_rating_dict
        print "ret dict", sr_user.sr_instance.concept_retention_rating_dict

        flash(revisit_status)
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.route("/add",  methods=['GET', 'POST'])
def add():
    form = AddConceptSubmissionForm(request.form)
    if request.method == 'POST' and form.validate():
        add_status = sr_user.sr_instance.add_concept(form.concept.data, form.C_score.data)
        print sr_user.sr_instance.concept_next_time_dict
        flash(add_status)
        return redirect(url_for('add'))
    return render_template('add-concept.html', form=form)

# Error Pages
@app.errorhandler(500)
def error_page(e):
    return render_template('error_pages/500.html'), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('error_pages/404.html'), 404

# Lazy Views
app.add_url_rule('/hello', view_func=hello.hello_world)



