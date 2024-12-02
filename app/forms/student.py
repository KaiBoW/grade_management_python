from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models.class_ import Class

class StudentForm(FlaskForm):
    student_id = StringField('学号', validators=[DataRequired(), Length(1, 20)])
    name = StringField('姓名', validators=[DataRequired(), Length(1, 64)])
    gender = SelectField('性别', choices=[('男', '男'), ('女', '女')])
    date_of_birth = DateField('出生日期', validators=[DataRequired()])
    class_id = SelectField('班级', coerce=int)
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.class_id.choices = [(c.id, c.name) for c in Class.query.all()] 