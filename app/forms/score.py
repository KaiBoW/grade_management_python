from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from app.models.student import Student
from app.models.subject import Subject

class ScoreForm(FlaskForm):
    student_id = SelectField('学生', coerce=int)
    subject_id = SelectField('科目', coerce=int)
    score = FloatField('分数', validators=[DataRequired(), NumberRange(min=0, max=100)])
    exam_date = DateField('考试日期', validators=[DataRequired()])
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.student_id.choices = [(s.id, f'{s.name} ({s.student_id})') 
                                 for s in Student.query.all()]
        self.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()] 