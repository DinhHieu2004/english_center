$(document).ready(function () {
    const token = localStorage.getItem('token');
    const userType = localStorage.getItem('userType');
    const userData = JSON.parse(localStorage.getItem('userData'));

    if (!token) {
        return;
    }
    if (userData) {
        $('#fullName').text(userData.fullname || 'Không rõ');
        $('#email').text(userData.email || 'Không rõ');

        if (userData.student_details) {
            $('#level').text(
                userData.student_details.level === "none" ? "Không xác định" : userData.student_details.level
            );
            if (userData.join_date) {
                const joinDate = new Date(userData.join_date);
                $('#joinDate').text(
                    joinDate.toLocaleDateString('vi-VN', {
                        day: '2-digit',
                        month: '2-digit',
                        year: 'numeric',
                    })
                );
            } else {
                $('#joinDate').text('Chưa có thông tin');
            }
        }

        if (userData.student_details && !userData.student_details.has_taken_test) {
            const takeTestButton = document.getElementById("takeTestButton");
            if (takeTestButton) {
                takeTestButton.style.display = "inline-block";
                takeTestButton.addEventListener('click', function () {
                    window.location.href = 'entrance_test.html';
                });
            }
        }
    }

    $('#logoutBtn').click(function (event) {
        event.preventDefault();
        localStorage.removeItem('token');
        localStorage.removeItem('userType');
        localStorage.removeItem('userData');
        window.location.href = '../base.html';
    });

    function fetchDashboardData() {
        $.ajax({
            url: 'http://127.0.0.1:8000/api/student/dashboard/',
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`
            },
            success: function(response) {
                console.log(response)
                if (response.current_data && response.current_data.length > 0) {
                    displayCurrentCourses(response.current_data);
                } else {
                    displayAvailableCourses(response.avilable_courses);
                }
            },
            error: function(xhr) {
                alert('Lỗi tải dữ liệu khóa học');
            }
        });
    }

    // Hiển thị khóa học hiện tại
    function displayCurrentCourses(courses) {
        const coursesContainer = $('#currentCourses');
        coursesContainer.empty();
    
        courses.forEach(course => {
            const courseCard = `
                <div class="card mb-2">
                    <div class="card-body">
                        <h5 class="card-title">${course.name}</h5>
                        <p class="card-text">${course.description}</p>
                        <p><strong>Cấp độ:</strong> ${course.level.toUpperCase()}</p>
                        <p><strong>Ngày bắt đầu:</strong> ${new Date(course.start_date).toLocaleDateString()}</p>
                        <a href="/course/${course.id}" class="btn btn-primary mt-2">Học ngay</a>
                    </div>
                </div>
            `;
            coursesContainer.append(courseCard);
        });
    }
    // Hiển thị khóa học có thể đăng ký
    function displayAvailableCourses(courses) {
        const registerContainer = $('#registerCourses');
        registerContainer.empty();

        if (!courses || courses.length === 0) {
            registerContainer.html('<p>Không có khóa học phù hợp hiện tại.</p>');
            return;
        }

        const coursesList = courses.map(course => `
            <div class="card mb-2">
                <div class="card-body">
                    <p class="card-text"> Mã khóa học :${course.id}</p>

                    <p class="card-text">${course.name}</p>
                    <p class="card-text">${course.description}</p>

                    <p><strong>Cấp độ:</strong> ${course.level.toUpperCase()}</p>
                    <button class="btn btn-success register-course" data-course-id="${course.id}">
                        Xem khóa học
                    </button>
                </div>
            </div>
        `).join('');

        registerContainer.html(`
            <h6>Các khóa học có thể đăng ký:</h6>
            ${coursesList}
        `);

        // Đăng ký khóa học
        $('.register-course').on('click', function() {
            const courseId = $(this).data('course-id');
          //  registerForCourse(courseId);
        });
    }

    // Đăng ký khóa học
    function registerForCourse(courseId) {
        $.ajax({
          //  url: '/api/student/register-course/',
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({ course_id: courseId }),
            success: function() {
                alert('Đăng ký khóa học thành công!');
                fetchDashboardData();
            },
            error: function() {
                alert('Đăng ký khóa học thất bại. Vui lòng thử lại.');
            }
        });
    }
  

    // Sự kiện kiểm tra trình độ
    $('#takeTestButton').on('click', function() {
        window.location.href = '/placement-test';
    });

    // Khởi tạo
    fetchDashboardData();
});