from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.user import User
from app.models.class_ import Class
from app.models.student import Student
from app.models.subject import Subject
from app.utils.decorators import admin_required
from app import db
from flask_login import current_user
from app.forms.user import UserForm  # 需要创建这个表单类

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users')
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.id.asc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/users.html', pagination=pagination)

@bp.route('/user/<int:id>/delete', methods=['POST'])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('不能删除自己的账号', 'error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('用户已删除', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/subjects')
@admin_required
def subjects():
    subjects = Subject.query.all()
    return render_template('admin/subjects.html', subjects=subjects)

@bp.route('/subject/add', methods=['GET', 'POST'])
@admin_required
def add_subject():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        full_score = request.form.get('full_score', type=int)
        
        if Subject.query.filter_by(code=code).first():
            flash('科目代码已存在', 'error')
        else:
            subject = Subject(name=name, code=code, full_score=full_score)
            db.session.add(subject)
            db.session.commit()
            flash('科目添加成功', 'success')
            return redirect(url_for('admin.subjects'))
            
    return render_template('admin/subject_form.html')

@bp.route('/user/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('用户添加成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/user_form.html', form=form) 