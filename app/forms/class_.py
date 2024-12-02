from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ClassForm(FlaskForm):
    name = StringField('班级名称', validators=[DataRequired(), Length(1, 64)])
    grade = StringField('年级', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField('提交') 