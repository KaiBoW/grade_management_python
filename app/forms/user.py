from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class UserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1, 120)])
    password = PasswordField('密码', validators=[
        DataRequired(),
        Length(6, 20),
        EqualTo('password2', message='两次输入的密码不匹配')
    ])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    role = SelectField('角色', choices=[('admin', '管理员'), ('teacher', '教师')])
    submit = SubmitField('提交') 