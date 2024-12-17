$(document).ready(function() {
        
    // Lấy courseId từ URL
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('id');
    console.log(courseId);

    if (courseId) {
        fetchCourseDetails(courseId);
        
    } else {
        alert("Không có lớp học được tìm thấy.");
    }
});

// Hàm lấy thông tin lớp học
function fetchCourseDetails(courseId) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/course/${courseId}/`,
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(courseDetails) {
            console.log(courseDetails);
            fetchClassDates(courseId);
            fetchCourseStudents(courseId);
        },
        error: function() {
            alert("Không thể lấy thông tin lớp học");
        }
    });
}
let classDates = [];
function fetchClassDates(courseId) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/course/${courseId}/schedule/`,  // API để lấy ngày học
        method: 'GET',
        headers: getAuthHeaders(),  // Thêm headers nếu cần
        success: function(response) {
            classDates = response.class_dates; // Dữ liệu trả về từ API
        },
        error: function() {
            alert("Không thể lấy dữ liệu lịch học.");
        }
    });
}
let studentNames = [];
function fetchCourseStudents(courseId) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/course/${courseId}/students/`,  // API lấy học viên
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(studentsResponse) {
            $('#studentTableBody').html('');
            console.log(studentsResponse);
             if (studentsResponse.students.length > 0) {
                studentsResponse.students.forEach(function(student) {
                    studentNames.push(student);
                    console.log(studentNames);
                });
                renderStudents(courseId, studentNames); 
            } else {
                $('#studentList').html("<p>Không có học viên nào trong lớp.</p>");
            }
        },
        error: function() {
            alert("Không thể lấy danh sách học viên. Vui lòng thử lại.");
        }
    });
}

// function fetchStudentDetails(studentId) {
//     return new Promise(function(resolve, reject) {
//         $.ajax({
//             url: `http://127.0.0.1:8000/api/student/${studentId}/`,  
//             method: 'GET',
//             headers: getAuthHeaders(),
//             success: function(studentDetails) {
//                 console.log(studentDetails.student);
//                 studentNames.push(studentDetails.student); 
//                 resolve();
//             },
//             error: function() {
//                 alert("Không thể lấy thông tin học viên.");
//                 reject(); 
//             }
//         });
//     });
// }
            function getAuthHeaders() {
                return {
                    'Authorization': 'Token ' + localStorage.getItem('token'),
                    'Content-Type': 'application/json'
                };
            }

            // Hàm hiển thị sinh viên trong bảng
            function renderStudents(courseId, studentNames) {
                // studentNames.sort();

                // Thêm cột ngày vào bảng
                const thead = document.querySelector('#attendanceTable thead tr');
                classDates.forEach(date => {
                    const th = document.createElement('th');
                    th.textContent = date;
                    thead.appendChild(th);
                });

                // Thêm sinh viên vào bảng
                const tbody = document.getElementById('studentTableBody');
                studentNames.forEach(function(student, index) {
                    const row = document.createElement('tr');

                    const sttCell = document.createElement('td');
                    sttCell.textContent = index + 1; // Số thứ tự bắt đầu từ 1
                    row.appendChild(sttCell);
                    // Tên sinh viên
                    const nameCell = document.createElement('td');
                    nameCell.textContent = student.name;
                    row.appendChild(nameCell);
                    
                    // Cột ngày điểm danh
                    classDates.forEach((date) => {
                        console.log(student.id);
                        const cell = document.createElement('td');
                        const input = document.createElement('input');
                        input.type = 'text';
                        input.classList.add('form-control');
                        getAttendanceStatus(courseId, student.id, date, function(currentStatus) {
                            if (currentStatus) {
                                input.value = currentStatus;
                            }
                            checkStatus(input);
            
                            input.onblur = function() {
                                checkStatus(this); 
                                console.log(courseId, student.id, date, this.value);
                                saveAttendance(courseId, student.id, date, this.value);
                            };
                        });
                        cell.appendChild(input);
                        row.appendChild(cell);
                    });

                    tbody.appendChild(row);
                });
                attachInputNavigation()
            }
            function getAttendanceStatus(courseId, student, date, callback) {
                let status = "";
                $.ajax({
                    url: `http://127.0.0.1:8000/api/course/${courseId}/attendance/`, 
                    method: 'GET',
                    headers: getAuthHeaders(),
                    data: {
                        student: student,
                        date: date
                    },
                    success: function(response) {
                            status = response.status;

                        callback(status);
                    },
                    error: function() {
                        alert("Không thể lấy trạng thái điểm danh.");
                    }
                });
            }
            function saveAttendance(courseId, studentId, date, status) {
                
                const data = {
                    student_id: studentId,
                    date: date,
                    status: status
                };
                console.log("Dữ liệu gửi lên:", data);
                $.ajax({
                    url: `http://127.0.0.1:8000/api/course/${courseId}/attendance/`,
                    method: 'POST',
                    headers: getAuthHeaders(),
                    contentType: 'application/json', 
                    data: JSON.stringify(data),  
                    success: function(response) {
                        console.log('Điểm danh đã được lưu:', response);
                    },
                    error: function(xhr, status, error) {
                        console.error('Lỗi khi lưu điểm danh:', error);
                    }
                });
            }
            
// Hàm kiểm tra trạng thái nhập liệu
function checkStatus(input) {
    if (input.value.toLowerCase() === "x") {
        input.style.backgroundColor = "#4CAF50"; // Đổi màu khi nhập "x"
        input.style.color = "#fff";
    } else if (input.value.toLowerCase() === "cp") {
        input.style.backgroundColor = "yellow";
    } else if (input.value.toLowerCase() === "v") {
        input.style.backgroundColor = "red";
        input.style.color = "#fff";
    } else {
        input.style.backgroundColor = "";
        input.style.color = "#000";
    }
}

function attachInputNavigation() {
    $("input[type='text']").on("keydown", function(e) {
        var current = $(this);
        var next = null;
        var currentColumnIndex = current.closest("td").index();
        var currentRow = current.closest("tr");

        // Di chuyển lên (phím mũi tên lên)
        if (e.which === 38) {
            if (currentRow.prev("tr").length > 0) {
                next = currentRow.prev("tr").find("td").eq(currentColumnIndex).find("input[type='text']");
            }
        }
        // Di chuyển xuống (phím mũi tên xuống)
        else if (e.which === 40) {
            if (currentRow.next("tr").length > 0) {
                next = currentRow.next("tr").find("td").eq(currentColumnIndex).find("input[type='text']");
            }
        }
        // // Di chuyển sang trái (phím mũi tên trái)
        // else if (e.which === 37) {
        //     if (currentColumnIndex > 0) {
        //         next = current.closest("tr").find("td").eq(currentColumnIndex - 1).find("input[type='text']");
        //     }
        // }
        // else if (e.which === 39) {
        //     if (currentColumnIndex < current.closest("tr").find("td").length - 1) {
        //         next = current.closest("tr").find("td").eq(currentColumnIndex + 1).find("input[type='text']");
        //     }
        // }

        if (next && next.length > 0) {
            next.focus();
            e.preventDefault();  
        }
    });
}
$(document).ready(function () {
    $('.look-course').on('click', function (e) {
        e.preventDefault();
        const urlParams = new URLSearchParams(window.location.search);
        const courseId = urlParams.get('id');
        window.location.href = `course_detail.html?id=${courseId}`;
    });
});
