from multiprocessing.dummy import current_process
from app import app, login
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Survey 
from app.classes.forms import SurveyForm
from flask_login import login_required
import datetime as dt

@app.route('/survey/new', methods=['GET', 'POST'])
@login_required
def surveyNew():
    form = SurveyForm() 

    if form.validate_on_submit():
        newSurvey = Survey(
            User = current_user.id,
            Quest1 = form.Quest1.data,
            Quest2 = form.Quest2.data,
            Quest3 = form.Quest3.data,
            Quest4 = form.Quest4.data,
            Quest5 = form.Quest5.data,
            Quest6 = form.Quest6.data
        )
        newSurvey.save()
        return redirect(url_for('survey',surveyId=newSurvey.id))

    return render_template('survey.html', form=form)

@app.route('/survey/edit/<surveyId>', methods=['GET', 'POST'])
@login_required
def surveyEdit(surveyId):
    form = SurveyForm()
    editSurvey = Survey.objects.get(id=surveyId) 

    if form.validate_on_submit():
        editSurvey.update(
            User = current_user.id,
            Quest1 = form.Quest1.data,
            Quest2 = form.Quest2.data,
            Quest3 = form.Quest3.data,
            Quest4 = form.Quest4.data,
            Quest5 = form.Quest5.data,
            Quest6 = form.Quest6.data
        )
        return redirect(url_for('survey',surveyId=editSurvey.id))

    form.Quest1.data = editSurvey.Quest1
    form.Quest2.data = editSurvey.Quest2
    form.Quest3.data = editSurvey.Quest3
    form.Quest4.data = editSurvey.Quest4
    form.Quest5.data = editSurvey.Quest5
    form.Quest6.data = editSurvey.Quest6

    return render_template('survey.html', form=form)


@app.route('/survey/<surveyId>')
@login_required 
def survey(surveyId):
    thisSurvey = Survey.objects.get(id = surveyId)
    return render_template('surveySubmit.html', survey = thisSurvey)

@app.route('/survey/delete/<surveyId>')
@login_required
def surveyDelete(surveyId):
    delSurvey = Survey.objects.get(id = surveyId)
    flash(f"Deleting results named {delSurvey.id}.")
    delSurvey.delete()
    return redirect(url_for('surveyList'))

@app.route('/survey/list')
@login_required
def surveyList():
    survey = Survey.objects()
    return render_template('surveySubmits.html', survey = survey)