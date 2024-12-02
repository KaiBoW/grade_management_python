from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.class_ import Class
from app.models.student import Student
from app.models.subject import Subject
from app.models.score import Score
from app.utils.decorators import teacher_required
from app import db
from app.forms.class_ import ClassForm
from app.forms.student import StudentForm
from app.forms.score import ScoreForm
from datetime import datetime

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    total_students = Student.query.count()
    total_classes = Class.query.count()
    total_subjects = Subject.query.count()
    recent_scores = Score.query.order_by(Score.created_at.desc()).limit(5).all()
    
    return render_template('dashboard/index.html',
                         total_students=total_students,
                         total_classes=total_classes,
                         total_subjects=total_subjects,
                         recent_scores=recent_scores)

@bp.route('/classes')
@login_required
@teacher_required
def classes():
    page = request.args.get('page', 1, type=int)
    pagination = Class.query.order_by(Class.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('dashboard/classes.html', pagination=pagination)

@bp.route('/students')
@login_required
@teacher_required
def students():
    page = request.args.get('page', 1, type=int)
    class_id = request.args.get('class_id', type=int)
    
    query = Student.query
    if class_id:
        query = query.filter_by(class_id=class_id)
        
    pagination = query.order_by(Student.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    classes = Class.query.all()
    
    return render_template('dashboard/students.html', 
                         pagination=pagination,
                         classes=classes,
                         current_class=class_id)

@bp.route('/scores')
@login_required
@teacher_required
def scores():
    page = request.args.get('page', 1, type=int)
    class_id = request.args.get('class_id', type=int)
    exam_date = request.args.get('exam_date')
    
    # 获取所有考试日期
    exam_dates = db.session.query(Score.exam_date)\
        .distinct()\
        .order_by(Score.exam_date.desc())\
        .all()
    exam_dates = [date[0] for date in exam_dates]
    
    # 查询学生
    query = Student.query
    if class_id:
        query = query.filter_by(class_id=class_id)
    
    # 分页获取学生
    pagination = query.order_by(Student.class_id, Student.student_id).paginate(
        page=page, per_page=10, error_out=False)
    
    # 获取所有科目
    subjects = Subject.query.order_by(Subject.id).all()
    
    # 获取选中学生的所有成绩
    if exam_date:
        exam_date = datetime.strptime(exam_date, '%Y-%m-%d').date()
    student_ids = [student.id for student in pagination.items]
    scores = Score.query.filter(
        Score.student_id.in_(student_ids),
        Score.exam_date == exam_date if exam_date else True
    ).all()
    
    # 构建成绩字典 {(student_id, subject_id): score}
    score_dict = {
        (score.student_id, score.subject_id): score.score 
        for score in scores
    }
    
    classes = Class.query.all()
    
    return render_template('dashboard/scores.html',
                         pagination=pagination,
                         subjects=subjects,
                         classes=classes,
                         current_class=class_id,
                         exam_dates=exam_dates,
                         current_exam_date=exam_date,
                         score_dict=score_dict)

@bp.route('/class/add', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_class():
    form = ClassForm()
    if form.validate_on_submit():
        class_ = Class(name=form.name.data, grade=form.grade.data)
        db.session.add(class_)
        db.session.commit()
        flash('班级添加成功', 'success')
        return redirect(url_for('dashboard.classes'))
    return render_template('dashboard/class_form.html', form=form)

@bp.route('/class/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_class(id):
    class_ = Class.query.get_or_404(id)
    form = ClassForm(obj=class_)
    if form.validate_on_submit():
        class_.name = form.name.data
        class_.grade = form.grade.data
        db.session.commit()
        flash('班级更新成功', 'success')
        return redirect(url_for('dashboard.classes'))
    return render_template('dashboard/class_form.html', form=form)

@bp.route('/class/<int:id>/delete', methods=['POST'])
@login_required
@teacher_required
def delete_class(id):
    class_ = Class.query.get_or_404(id)
    if class_.students.count() > 0:
        flash('无法删除有学生的班级', 'error')
        return redirect(url_for('dashboard.classes'))
    db.session.delete(class_)
    db.session.commit()
    flash('班级删除成功', 'success')
    return redirect(url_for('dashboard.classes'))

@bp.route('/student/add', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            student_id=form.student_id.data,
            name=form.name.data,
            gender=form.gender.data,
            date_of_birth=form.date_of_birth.data,
            class_id=form.class_id.data
        )
        db.session.add(student)
        db.session.commit()
        flash('学生添加成功', 'success')
        return redirect(url_for('dashboard.students'))
    return render_template('dashboard/student_form.html', form=form)

@bp.route('/student/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.student_id = form.student_id.data
        student.name = form.name.data
        student.gender = form.gender.data
        student.date_of_birth = form.date_of_birth.data
        student.class_id = form.class_id.data
        db.session.commit()
        flash('学生信息更新成功', 'success')
        return redirect(url_for('dashboard.students'))
    return render_template('dashboard/student_form.html', form=form)

@bp.route('/student/<int:id>/delete', methods=['POST'])
@login_required
@teacher_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('学生删除成功', 'success')
    return redirect(url_for('dashboard.students'))

@bp.route('/score/add', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_score():
    form = ScoreForm()
    if form.validate_on_submit():
        score = Score(
            student_id=form.student_id.data,
            subject_id=form.subject_id.data,
            score=form.score.data,
            exam_date=form.exam_date.data
        )
        db.session.add(score)
        db.session.commit()
        flash('成绩添加成功', 'success')
        return redirect(url_for('dashboard.scores'))
    return render_template('dashboard/score_form.html', form=form)

@bp.route('/score/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_score(id):
    score = Score.query.get_or_404(id)
    form = ScoreForm(obj=score)
    if form.validate_on_submit():
        score.student_id = form.student_id.data
        score.subject_id = form.subject_id.data
        score.score = form.score.data
        score.exam_date = form.exam_date.data
        db.session.commit()
        flash('成绩更新成功', 'success')
        return redirect(url_for('dashboard.scores'))
    return render_template('dashboard/score_form.html', form=form)

@bp.route('/score/<int:id>/delete', methods=['POST'])
@login_required
@teacher_required
def delete_score(id):
    score = Score.query.get_or_404(id)
    db.session.delete(score)
    db.session.commit()
    flash('成绩删除成功', 'success')
    return redirect(url_for('dashboard.scores')) 