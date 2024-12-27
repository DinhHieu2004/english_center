$(document).ready(function() {
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('id');
    console.log(courseId);

  
  
    if (courseId) {
        fetchCourseDetails(courseId);
        
    } else {
        alert("Không có lớp học được tìm thấy.");
    }
     
});

function fetchCourseDetails(courseId) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/course/${courseId}/`,
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(courseDetails) {
            console.log(courseDetails);
            let course = courseDetails.course;
            fetchTeacherDetails(course.teacher, course);
            fetchCourseStudents(courseId);
        },
        error: function() {
            alert("Không thể lấy thông tin lớp học");
        }
    });
}
function fetchCourseStudents(courseId) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/course/${courseId}/students/`,  
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(studentsResponse) {
            $('#studentTableBody').html('');
            console.log(studentsResponse);
            if (studentsResponse.students.length > 0) {
                studentsResponse.students.forEach(function(student, index) {
                    renderStudentDetails(student, index); 
                });
            } else {
                $('#studentList').html("<p>Không có học viên nào trong lớp.</p>");
            }
        },
        error: function() {
            alert("Không thể lấy danh sách học viên. Vui lòng thử lại.");
        }
    });
}
function renderStudentDetails(student, index) {
    const studentD = student
    let studentRow = `
                <tr>
                    <td>${index + 1}</td>
                    <td>${studentD.name}</td>
                    <td>${studentD.email}</td>
                    <td>${studentD.birth_date}</td>
                    <td>${studentD.address}</td>
                    <td>${studentD.phone}</td>
                    <td>${studentD.complete}%</td>
                </tr>
            `;
    $('#studentTableBody').append(studentRow);
}
function fetchTeacherDetails(teacherId, course) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/teacher/${teacherId}/`,
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(teacherResponse) {
            let teacherName = teacherResponse.teacher_name;
            renderCourseDetails(course, teacherName);
        },
        error: function() {
            alert("Không thể lấy thông tin giáo viên");
        }
    });
}

function renderCourseDetails(course, teacherName) {
    let schedulesHtml = '';
    if (course.schedules && course.schedules.length > 0) {
        schedulesHtml = `
            <h4>Lịch học:</h4>
            <ul>
                ${course.schedules.map(schedule => `
                    <li>
                        <strong>Thứ:</strong> ${schedule.weekday_display}, 
                        <strong>Giờ bắt đầu:</strong> ${schedule.session}
                    </li>
                `).join('')}
            </ul>
        `;
    } else {
        schedulesHtml = `<p>Không có lịch học nào được thiết lập.</p>`;
    }

    let courseDetailsHtml = `
        <h3>Thông tin lớp học: ${course.name}</h3>
        <p><strong>Miêu tả:</strong> ${course.description}</p>
        <p><strong>Trình độ:</strong> ${course.level}</p>
        <p><strong>Giáo viên:</strong> ${teacherName}</p>
        <p><strong>Ngày bắt đầu:</strong> ${course.start_date}</p>
        <p><strong>Tổng số buổi:</strong> ${course.total_session}</p>
        ${schedulesHtml}
    `;
    $('#courseDetail').html(courseDetailsHtml);
}
$('.look-course').on('click', function(e) {
    e.preventDefault();
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('id');
    
    if (courseId) {
        window.location.href = `attendance.html?id=${courseId}`;
    } else {
        alert('Không tìm thấy thông tin khóa học!');
    }

});
$('#view-notifications').on('click', function(e) {
    e.preventDefault();
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('id');
    
    if (courseId) {
        window.location.href = `../notification/notification.html?course_id=${courseId}`;
    } else {
        alert('Không tìm thấy thông tin khóa học!');
    }

});

function getAuthHeaders() {
    return {
        'Authorization': 'Token ' + localStorage.getItem('token'),
        'Content-Type': 'application/json'
    };
}