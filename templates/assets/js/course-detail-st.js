 $(document).ready(function () {
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('id'); 
    const is_register = localStorage.getItem('is_register') === 'true'; 
    console.log(is_register, typeof is_register)


    if (courseId) {
        fetchCourseDetails(courseId, is_register);
        connectToWebSocket(courseId)
        
    } else {
        alert("Không có lớp học được tìm thấy.");
    }
});
function connectToWebSocket(courseId) {
    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/notifications/${courseId}/`);

    socket.onopen = function () {
        console.log("WebSocket connection established.");
    };

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log("Received notification:", data);

    };

    socket.onclose = function () {
        console.log("WebSocket connection closed.");
    };
}


function getAuthHeaders() {
    return {
        'Authorization': 'Token ' + localStorage.getItem('token'),
        'Content-Type': 'application/json'
    };
}


function fetchCourseDetails(courseId, is_register) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/course/${courseId}/`,
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(courseDetails) {
            console.log(courseDetails);
            let course = courseDetails.course;
            fetchTeacherDetails(course.teacher, course, is_register);
            renderCourseDetails(course, course.teacher, is_register)
        },
        error: function() {
            alert("Không thể lấy thông tin lớp học");
        }
    });
}
function renderCourseDetails(course, teacherName, is_register) {
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
    
     let paymentButton ='';
     if(is_register){
        paymentButton = `<p style="color: green;">Bạn đã đăng ký khóa học này.</p>`;
     }else{
        paymentButton = `<button class="btn btn-primary" id="payButton">Đăng kí khóa học này</button>`;
     }

    let courseDetailsHtml = `
        <h3>Thông tin lớp học: ${course.name}</h3>
        <p><strong>Miêu tả:</strong> ${course.description}</p>
        <p><strong>Trình độ:</strong> ${course.level}</p>
        <p><strong>Giá:</strong> ${course.price} VND</p>
        <p><strong>Ngày bắt đầu:</strong> ${course.start_date}</p>
        <p><strong>Giáo viên:</strong> ${teacherName}</p>
      
        ${schedulesHtml}
        ${paymentButton}

    `;
    $('#courseDetail').html(courseDetailsHtml);

    if (!is_register) {
        $('#payButton').on('click', function () {
            openPaymentModal(course);
        });
    }
}


function fetchTeacherDetails(teacherId, course, is_register) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/teacher/${teacherId}/`,
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(teacherResponse) {
            let teacherName = teacherResponse.teacher_name;
            renderCourseDetails(course, teacherName, is_register);
        },
        error: function() {
            alert("Không thể lấy thông tin giáo viên");
        }
    });
}

function openPaymentModal(course) {
    $('#modalCourseName').text(course.name);
    $('#modalCoursePrice').text(course.price);
    $('#paymentModal').modal('show');

    $('#confirmPaymentBtn').off('click').on('click', function () {
        enrollCourse(course.id);
    });
}
function enrollCourse(courseId) {
    $.ajax({
        url: 'http://127.0.0.1:8000/api/enroll-course/',
        method: 'POST',
        headers: getAuthHeaders(),
        data: JSON.stringify({
            course: courseId,
            payment: true
        }),
        success: function () {
            alert("Đăng ký khóa học thành công!");
            $('#paymentModal').modal('hide');
            
            localStorage.setItem('is_register', 'true');
            const paymentButton = document.querySelector('#payButton');
            if (paymentButton) {
                const parentElement = paymentButton.parentElement;
                paymentButton.remove();
                parentElement.innerHTML = `<p style="color: green;">Bạn đã đăng ký khóa học này.</p>`;
            }
        },
        error: function () {
            alert("Không thể thực hiện thanh toán. Vui lòng thử lại.");
        }
    });
}
