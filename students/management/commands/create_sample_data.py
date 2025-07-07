from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Teacher, Classroom, Student, Subject, Score
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Create sample data for student management system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new samples',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Score.objects.all().delete()
            Student.objects.all().delete()
            Classroom.objects.all().delete()
            Subject.objects.all().delete()
            Teacher.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating sample data...')

        # Create subjects
        subjects_data = [
            {'name': 'Toán học', 'code': 'MATH'},
            {'name': 'Ngữ văn', 'code': 'LIT'},
            {'name': 'Tiếng Anh', 'code': 'ENG'},
            {'name': 'Vật lý', 'code': 'PHY'},
            {'name': 'Hóa học', 'code': 'CHEM'},
            {'name': 'Sinh học', 'code': 'BIO'},
            {'name': 'Lịch sử', 'code': 'HIST'},
            {'name': 'Địa lý', 'code': 'GEO'},
        ]

        subjects = []
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                code=subject_data['code'],
                defaults={'name': subject_data['name']}
            )
            subjects.append(subject)
            if created:
                self.stdout.write(f'Created subject: {subject.name}')

        # Create teachers
        teachers_data = [
            {'username': 'teacher1', 'full_name': 'Nguyễn Văn An', 'email': 'nva@school.edu.vn'},
            {'username': 'teacher2', 'full_name': 'Trần Thị Bình', 'email': 'ttb@school.edu.vn'},
            {'username': 'teacher3', 'full_name': 'Lê Văn Cường', 'email': 'lvc@school.edu.vn'},
            {'username': 'teacher4', 'full_name': 'Phạm Thị Dung', 'email': 'ptd@school.edu.vn'},
        ]

        teachers = []
        for teacher_data in teachers_data:
            user, created = User.objects.get_or_create(
                username=teacher_data['username'],
                defaults={
                    'email': teacher_data['email'],
                    'first_name': teacher_data['full_name'].split()[-1],
                    'last_name': ' '.join(teacher_data['full_name'].split()[:-1]),
                }
            )
            if created:
                user.set_password('password123')
                user.save()

            teacher, created = Teacher.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': teacher_data['full_name'],
                    'email': teacher_data['email'],
                    'phone': f'090{random.randint(1000000, 9999999)}'
                }
            )
            teachers.append(teacher)
            if created:
                self.stdout.write(f'Created teacher: {teacher.full_name}')

        # Create classrooms
        classrooms_data = [
            {'name': '10A1', 'grade_level': '10', 'school_year': '2024-2025'},
            {'name': '10A2', 'grade_level': '10', 'school_year': '2024-2025'},
            {'name': '11B1', 'grade_level': '11', 'school_year': '2024-2025'},
            {'name': '12C1', 'grade_level': '12', 'school_year': '2024-2025'},
        ]

        classrooms = []
        for i, classroom_data in enumerate(classrooms_data):
            classroom, created = Classroom.objects.get_or_create(
                name=classroom_data['name'],
                defaults={
                    'teacher': teachers[i % len(teachers)],
                    'grade_level': classroom_data['grade_level'],
                    'school_year': classroom_data['school_year'],
                    'description': f'Lớp {classroom_data["name"]} năm học {classroom_data["school_year"]}'
                }
            )
            classrooms.append(classroom)
            if created:
                self.stdout.write(f'Created classroom: {classroom.name}')

        # Create students
        first_names = ['An', 'Bình', 'Cường', 'Dung', 'Em', 'Phúc', 'Giang', 'Hà', 'Khánh', 'Linh',
                      'Minh', 'Nam', 'Oanh', 'Phong', 'Quang', 'Sơn', 'Thảo', 'Uyên', 'Việt', 'Yến']
        last_names = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Phan', 'Vũ', 'Võ', 'Đặng', 'Bùi']

        students = []
        for classroom in classrooms:
            for i in range(random.randint(25, 35)):
                full_name = f"{random.choice(last_names)} {random.choice(first_names)}"
                birth_date = date(2006 + int(classroom.grade_level) - 10, 
                                random.randint(1, 12), random.randint(1, 28))
                
                student = Student.objects.create(
                    full_name=full_name,
                    birth_date=birth_date,
                    gender=random.choice(['M', 'F']),
                    classroom=classroom,
                    student_id=f"{classroom.grade_level}{classroom.name[-2:]}{i+1:02d}",
                    email=f"student{len(students)+1}@student.edu.vn",
                    phone=f"098{random.randint(1000000, 9999999)}",
                    parent_name=f"{random.choice(last_names)} {random.choice(['Văn', 'Thị'])} {random.choice(first_names)}",
                    parent_phone=f"091{random.randint(1000000, 9999999)}",
                    notes=random.choice(['', '', '', 'Học sinh tích cực', 'Cần theo dõi thêm', 'Năng khiếu toán học'])
                )
                students.append(student)

        self.stdout.write(f'Created {len(students)} students')

        # Create scores
        score_types = ['quiz', 'midterm', 'final', 'assignment', 'participation']
        scores_created = 0

        for student in students:
            for subject in random.sample(subjects, random.randint(4, 6)):
                for _ in range(random.randint(3, 8)):
                    score_date = date.today() - timedelta(days=random.randint(1, 90))
                    score_value = random.uniform(4.0, 10.0)
                    
                    # Higher chance for good scores
                    if random.random() < 0.7:
                        score_value = random.uniform(7.0, 10.0)
                    
                    try:
                        Score.objects.create(
                            student=student,
                            subject=subject,
                            score=round(score_value, 2),
                            score_type=random.choice(score_types),
                            date=score_date,
                            teacher=student.classroom.teacher,
                            notes=random.choice(['', '', '', 'Bài làm tốt', 'Cần cải thiện', 'Xuất sắc'])
                        )
                        scores_created += 1
                    except:
                        # Skip if duplicate score exists
                        pass

        self.stdout.write(f'Created {scores_created} scores')
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {len(subjects)} subjects\n'
                f'- {len(teachers)} teachers\n'
                f'- {len(classrooms)} classrooms\n'
                f'- {len(students)} students\n'
                f'- {scores_created} scores'
            )
        )