from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    publication_date = StringField('Publication Date')
    description = TextAreaField('Description')
    cover_image = StringField('Cover Image')
    submit = SubmitField()