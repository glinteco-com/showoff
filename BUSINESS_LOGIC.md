# Project: Learning Management System

A compact Django application designed for teachers to manage students and classrooms. Suitable for practicing relational models, Django admin, basic views, and APIs.

---

## 1. Main Objectives

- Allow teachers to login and manage students
- View student lists by classroom
- Record scores and view student score history
- Add personal notes for each student
- Provide comprehensive statistics and reporting
- Export data in various formats

---

## 2. Data Models

### Teacher
- `user`: Link to Django User model
- `full_name`: Teacher's full name
- `email`: Email address (unique)
- `phone`: Phone number (optional)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Classroom
- `name`: Classroom name (e.g., "10A1")
- `teacher`: Homeroom teacher (Teacher model)
- `description`: Classroom description (optional)
- `grade_level`: Grade level (e.g., "10", "11", "12")
- `school_year`: Academic year (e.g., "2024-2025")
- `is_active`: Active status
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Student
- `full_name`: Student's full name
- `birth_date`: Date of birth
- `gender`: Gender (Male/Female/Other)
- `classroom`: Link to Classroom model
- `student_id`: Unique student identifier
- `email`: Email address (optional)
- `phone`: Phone number (optional)
- `address`: Home address (optional)
- `parent_name`: Parent/guardian name (optional)
- `parent_phone`: Parent/guardian phone (optional)
- `notes`: Personal notes (optional)
- `is_active`: Active status
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Subject
- `name`: Subject name (e.g., "Mathematics", "Literature")
- `code`: Subject code (e.g., "MATH", "LIT", "ENG")
- `description`: Subject description (optional)
- `is_active`: Active status
- `created_at`: Creation timestamp

### Score
- `student`: Student being graded
- `subject`: Subject for the score
- `score`: Score value (0-10 scale with 2 decimal places)
- `score_type`: Type of assessment (quiz, midterm, final, assignment, participation)
- `date`: Date when score was recorded
- `notes`: Additional notes (optional)
- `teacher`: Teacher who recorded the score
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

---

## 3. Main Features

### A. Teacher Authentication
- Only authenticated teachers can access the system
- JWT-based authentication for API access

### B. Classroom Management
- View classroom list
- View student list in each classroom
- Classroom statistics and reporting
- Export student data to CSV

### C. Student Management
- Add/edit/delete students
- View detailed student information
- Add personal notes
- View student score history
- Calculate average scores by subject

### D. Score Management
- Add scores by subject and assessment type
- View score history with filtering options
- Bulk score creation
- Score validation (0-10 range)

### E. Subject Management
- Manage subjects with codes
- View subject statistics
- Track scores by subject

---

## 4. API Features

### Teacher APIs
- CRUD operations for teacher profiles
- Get teacher's classrooms
- Get teacher's students
- Swagger tags: "Teacher: Classroom Management", "Teacher: Student Management"

### Classroom APIs
- CRUD operations for classrooms
- Get students in classroom
- Get classroom statistics
- Export students to CSV
- Swagger tags: "Classroom: Student Management", "Classroom: Statistics", "Classroom: Export"

### Student APIs
- CRUD operations for students
- Get student scores with filtering
- Get average scores by subject
- Swagger tags: "Student: Score Management", "Student: Statistics"

### Subject APIs
- CRUD operations for subjects
- Get subject scores
- Get subject statistics
- Swagger tags: "Subject: Score Management", "Subject: Statistics"

### Score APIs
- CRUD operations for scores
- Filter scores by classroom
- Bulk score creation
- Swagger tags: "Score: Classroom Filter", "Score: Bulk Operations"

---

## 5. Advanced Features

### Statistics and Reporting
- Average scores by subject and classroom
- Overall classroom performance metrics
- Student performance tracking

### Data Export
- CSV export for student lists
- Include average scores in exports
- Formatted with proper headers

### Permission System
- Teachers can only view/edit their own classrooms and students
- Automatic teacher assignment for score creation
- Role-based access control

### API Documentation
- Comprehensive Swagger documentation
- Organized by functional groups with tags
- Interactive API testing interface

---

## 6. Technology Stack

- Python 3.12+
- Django 5.1
- Django REST Framework
- JWT Authentication (Simple JWT)
- Swagger/OpenAPI documentation (drf-yasg)
- PostgreSQL or SQLite
- Redis for caching and Celery

---

## 7. Project Structure

### Apps
- `learning`: Main application containing all models and APIs

### Models Organization
- Separate files for each model in `learning/models/`
- Centralized imports in `__init__.py`

### Views Organization
- Separate ViewSets in `learning/views/`
- Organized by functionality with appropriate Swagger tags

### Serializers Organization
- Separate serializers in `learning/serializers/`
- Different serializers for list/detail views

### Admin Interface
- Comprehensive Django admin configuration
- Separate admin files for each model
- Enhanced admin features with custom methods

---

## 8. Development Goals

- Clean, maintainable code structure
- Comprehensive API documentation
- Robust permission system
- Easy to extend and modify
- Production-ready with proper validation
- Comprehensive test data generation
