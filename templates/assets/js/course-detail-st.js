 $(document).ready(function () {
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('id'); 

    if (courseId) {
        fetchCourseDetails(courseId);
        
    } else {
        alert("Không có lớp học được tìm thấy.");
    }
});

function getAuthHeaders() {
    return {
        'Authorization': 'Token ' + localStorage.getItem('token'),
        'Content-Type': 'application/json'
    };
}

function fetchCourseDetails(courseId) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/course/${courseId}/`,
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(courseDetails) {
            console.log(courseDetails);
            let course = courseDetails.course;
            fetchTeacherDetails(course.teacher, course);
            renderCourseDetails(course, course.teacher)
        },
        error: function() {
            alert("Không thể lấy thông tin lớp học");
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
                        <strong>Giờ bắt đầu:</strong> ${schedule.start_time}
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
        <p><strong>Ngày bắt đầu:</strong> ${course.start_date}</p>
        <p><strong>Giáo viên:</strong> ${teacherName}</p>
        ${schedulesHtml}
    `;
    $('#courseDetail').html(courseDetailsHtml);
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