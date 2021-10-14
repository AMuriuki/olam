from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_babel import _, lazy_gettext as _l


class BoardItemForm(FlaskForm):
    opportunity = StringField(_l('Opportunity'))
    email = StringField(_l('Email Address'))
    website = StringField(_l('Website'))
    submit1 = SubmitField(_l('Add'))


class NewRecurringPlanForm(FlaskForm):
    name = StringField(_l('New Plan'))
    submit = SubmitField(_l('Save'))


class EditStageForm(FlaskForm):
    stage_name = StringField(_l('Stage Name'))
    submit_stage_edits = SubmitField(_l('Save'))


class CreateSalesTeamForm(FlaskForm):
    name = StringField(_l('Sales Team'))
    submit = SubmitField(_l('Save'))
