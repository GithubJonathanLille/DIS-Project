from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import Optional

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class MovieSearchForm(FlaskForm):
    title = StringField('Title Contains', validators=[Optional()])
    actor = StringField('Actor Name Contains', validators=[Optional()])
    # For genres, we'll populate choices from the DB in the route
    genres = MultiCheckboxField('Genres', choices=[], coerce=int, validators=[Optional()])
    min_runtime = IntegerField('Min Runtime (mins)', validators=[Optional()])
    max_runtime = IntegerField('Max Runtime (mins)', validators=[Optional()])
    min_release_year = IntegerField('Min Release Year', validators=[Optional()])
    max_release_year = IntegerField('Max Release Year', validators=[Optional()])
    min_rank = IntegerField('Min Rank', validators=[Optional()])
    max_rank = IntegerField('Max Rank', validators=[Optional()])
    submit = SubmitField('Search Movies')