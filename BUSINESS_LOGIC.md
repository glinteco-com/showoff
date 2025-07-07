# 🎯 Project: Student Manager

Một ứng dụng Django nhỏ gọn, dành cho giáo viên quản lý học sinh và lớp học. Phù hợp để luyện tập mô hình quan hệ, Django admin, view cơ bản hoặc API.

---

## 1. Mục tiêu chính

- Cho phép giáo viên đăng nhập và quản lý học sinh.
- Xem danh sách học sinh theo lớp học.
- Ghi điểm và xem lịch sử điểm của học sinh.
- Ghi chú cá nhân cho từng học sinh.

---

## 2. Mô hình dữ liệu (Models)

### 👤 `Student`
- `full_name`: tên đầy đủ
- `birth_date`: ngày sinh
- `classroom`: liên kết đến lớp học (`Classroom`)
- `notes`: ghi chú riêng (tùy chọn)

### 🧑‍🏫 `Teacher`
- `user`: liên kết với Django `User`
- `full_name`: tên giáo viên
- `email`: địa chỉ email

### 🏫 `Classroom`
- `name`: tên lớp học (VD: "10A1")
- `teacher`: giáo viên chủ nhiệm (`Teacher`)

### 🧾 `Score`
- `student`: học sinh được chấm điểm
- `subject`: tên môn học (VD: Toán, Văn)
- `score`: điểm số
- `date`: ngày ghi điểm

---

## 3. Chức năng chính

### A. Đăng nhập giáo viên
- Chỉ giáo viên đăng nhập mới được truy cập hệ thống

### B. Quản lý lớp học
- Xem danh sách lớp
- Xem danh sách học sinh trong lớp

### C. Quản lý học sinh
- Thêm / sửa / xoá học sinh
- Xem thông tin chi tiết của từng học sinh
- Thêm ghi chú riêng

### D. Ghi điểm học sinh
- Thêm điểm theo từng môn học
- Xem lịch sử điểm

---

## 4. Mở rộng tiềm năng (tuỳ chọn)

- **Thống kê lớp học**: điểm trung bình môn theo lớp
- **Xuất dữ liệu CSV**: danh sách học sinh và điểm
- **Phân quyền giáo viên**: mỗi giáo viên chỉ xem lớp của họ
- **API RESTful**: xây dựng API phục vụ frontend hoặc mobile app

---

## 5. Công nghệ sử dụng

- Python 3.12+
- Django 5.1
- (Tùy chọn) Django REST Framework
- SQLite hoặc PostgreSQL

---

## 6. Mục tiêu phát triển

- Ưu tiên cấu trúc đơn giản, rõ ràng
- Có thể chạy độc lập bằng Django Admin
- Code dễ mở rộng nếu cần thêm tính năng sau này