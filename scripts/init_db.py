import os
import sys
from datetime import datetime, date

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from app.models.class_ import Class
from app.models.student import Student
from app.models.subject import Subject
from app.models.score import Score

def init_db():
    app = create_app()
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 创建管理员账户
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # 创建教师账户
            teacher = User(
                username='teacher',
                email='teacher@example.com',
                role='teacher'
            )
            teacher.set_password('teacher123')
            db.session.add(teacher)
        
        # 创建示例科目
        subjects = [
            {'name': '语文', 'code': 'CHN'},
            {'name': '数学', 'code': 'MATH'},
            {'name': '英语', 'code': 'ENG'},
            {'name': '物理', 'code': 'PHY'},
            {'name': '化学', 'code': 'CHEM'},
        ]
        
        subject_objs = []
        for subject_data in subjects:
            subject = Subject.query.filter_by(code=subject_data['code']).first()
            if not subject:
                subject = Subject(**subject_data)
                db.session.add(subject)
            subject_objs.append(subject)
        
        # 创建示例班级
        classes = [
            {'name': '高一(1)班', 'grade': '高一'},
            {'name': '高一(2)班', 'grade': '高一'},
            {'name': '高二(1)班', 'grade': '高二'},
            {'name': '高二(2)班', 'grade': '高二'},
        ]
        
        class_objs = []
        for class_data in classes:
            class_ = Class.query.filter_by(name=class_data['name']).first()
            if not class_:
                class_ = Class(**class_data)
                db.session.add(class_)
            class_objs.append(class_)
        
        db.session.commit()  # 提交以获取ID
        
        # 创建示例学生
        students_data = []
        for class_ in class_objs:
            for i in range(1, 11):  # 每个班级10个学生
                student_id = f"{class_.grade[:2]}{class_.name[2:4]}{i:02d}"
                students_data.append({
                    'student_id': student_id,
                    'name': f'学生{student_id}',
                    'gender': '男' if i % 2 == 0 else '女',
                    'date_of_birth': date(2005, i % 12 + 1, i % 28 + 1),
                    'class_id': class_.id
                })
        
        student_objs = []
        for student_data in students_data:
            student = Student.query.filter_by(student_id=student_data['student_id']).first()
            if not student:
                student = Student(**student_data)
                db.session.add(student)
            student_objs.append(student)
        
        db.session.commit()  # 提交以获取ID
        
        # 创建示例成绩
        scores_data = []
        for student in student_objs:
            for subject in subject_objs:
                scores_data.append({
                    'student_id': student.id,
                    'subject_id': subject.id,
                    'score': float(70 + (hash(f"{student.id}{subject.id}") % 30)),  # 随机分数
                    'exam_date': date(2024, 1, 15)  # 期末考试
                })
                scores_data.append({
                    'student_id': student.id,
                    'subject_id': subject.id,
                    'score': float(70 + (hash(f"{student.id}{subject.id}2") % 30)),  # 随机分数
                    'exam_date': date(2023, 9, 15)  # 期中考试
                })
        
        for score_data in scores_data:
            score = Score.query.filter_by(
                student_id=score_data['student_id'],
                subject_id=score_data['subject_id'],
                exam_date=score_data['exam_date']
            ).first()
            if not score:
                score = Score(**score_data)
                db.session.add(score)
        
        db.session.commit()
        print("示例数据创建成功！")
        print("管理员账号: admin/admin123")
        print("教师账号: teacher/teacher123")

if __name__ == '__main__':
    init_db() 