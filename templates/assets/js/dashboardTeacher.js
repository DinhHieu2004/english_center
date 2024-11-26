$(document).ready(function () {
    const token = localStorage.getItem('token');
    const userType = localStorage.getItem('userType');
    const userData = JSON.parse(localStorage.getItem('userData'));
    if (!token) {
        return;
    }
    
    $('#teacherName').text(userData.username);
    $('#fullName').text(userData.fullname);
    $('#email').text(userData.email);

    if (userData.teacher_details) {
        $('#level').text(userData.teacher_details.level || 'Chưa xác định');

        if (userData.join_date) {
            const joinDate = new Date(userData.join_date);
            const formattedDate = joinDate.toLocaleDateString('vi-VN', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            });
            $('#joinDate').text(formattedDate);
        } else {
            $('#joinDate').text('Chưa có thông tin');
        }
    }
    // Hiển thị danh sách lớp học
    $.ajax({
        url: `http://127.0.0.1:8000/api/teacher/dashboard/`,
        method: 'GET',
        headers: {
            'Authorization': 'Token ' + token, 
            'Content-Type': 'application/json'
        },
        success: function(response) {  
            if (response.courses_data && response.courses_data.length > 0) {
                let classListHtml = '';
                response.courses_data.forEach(course => {
                    classListHtml += `
                        <div class="card mt-3">
                            <div class="card-body">
                                <h5 class="card-title">${course.name}</h5>
                                <p>${course.description}</p>
                                <p><strong>Cấp độ:</strong> ${course.level}</p>
                                <p><strong>Ngày bắt đầu:</strong> ${course.start_date}</p>
                                <p><strong>Số lượng buổi học:</strong> ${course.total_session}</p>
                                <button class="btn btn-success look-course" data-id="${course.id}">Chi tiết</button>
                            </div>
                        </div>
                    `;
                });
                $('#classList').html(classListHtml);
            } else {
                $('#classList').html('<p>Chưa có lớp học nào.</p>');
            }
        },
        error: function(xhr, status, error) {
            console.error('Có lỗi xảy ra:', error);
            $('#classList').html('<p>Không thể lấy danh sách lớp học. Vui lòng thử lại sau.</p>');
        }
    });
    // Xử lý sự kiện khi người dùng nhấn nút Xem chi tiết
    $('#classList').on('click', '.look-course', function () {
        const courseId = $(this).data('id');
        window.location.href = `../teacher/course_detail.html?id=${courseId}`;
    });
    // Xử lý đăng xuất
    $('#logoutBtn').click(function (event) {
        event.preventDefault();
        localStorage.removeItem('token');
        localStorage.removeItem('userType');
        localStorage.removeItem('userData'); 
        window.location.href = '../base.html';
    });
    
});
