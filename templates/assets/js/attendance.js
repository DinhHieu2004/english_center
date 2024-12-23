let currentPage = localStorage.getItem('currentPage') ? parseInt(localStorage.getItem('currentPage')) : 1;
let attendanceDataCache = {}; 
$(document).ready(function() {
    
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('id');
    console.log(courseId);
    const courses = JSON.parse(localStorage.getItem('courses_data')) || [];

    if (courses.length > 0) {
        const courseSelect = $('#courseSelect');
        
        courses.forEach(course => {
            const option = $('<option>')
                .val(course.id) 
                .text(course.name);  

            courseSelect.append(option);
            if (course.id == courseId) {
                option.prop('selected', true);
            }
        });
        courseSelect.change(function () {
            const selectedCourseId = $(this).val();
            if (selectedCourseId) {
                const newUrl = new URL(window.location.href);
                newUrl.searchParams.set('id', selectedCourseId);
                window.history.pushState({ path: newUrl.href }, '', newUrl.href);
                location.reload();
            }
        });
    }
    if (courseId) {
        fetchCourseDetails(courseId, currentPage);
        
    } else {
        alert("Không có lớp học được tìm thấy.");
    }
});


function fetchCourseDetails(courseId, currentPage) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/course/${courseId}/`,
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(courseDetails) {
            console.log(courseDetails);
            fetchClassDates(courseId, currentPage);
            fetchCourseStudents(courseId);
        },
        error: function() {
            alert("Không thể lấy thông tin lớp học");
        }
    });
}
let classDates = [];
let pageSize = 10;   
let totalPages = 0;

function fetchClassDates(courseId, currentPage) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/course/${courseId}/schedule/?page=${currentPage}`,
        method: 'POST',
        headers: getAuthHeaders(),
        contentType: 'application/json',
        success: function(response) {
            console.log(response);
            classDates = response.results.class_dates; 
            totalPages = response.results.total_pages;
            currentPage = response.results.current_page;
            console.log(classDates);
            console.log(totalPages);
            console.log(currentPage);
            getAttendanceStatus(courseId, classDates);
        },
        error: function() {
            alert("Không thể lấy dữ liệu lịch học.");
        }
    });
}
let studentNames = [];
function fetchCourseStudents(courseId) {
    $.ajax({
        url: `http://127.0.0.1:8000/api/course/${courseId}/students/`, 
        method: 'GET',
        headers: getAuthHeaders(),
        success: function(studentsResponse) {
            studentNames = [];
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

            function getAuthHeaders() {
                return {
                    'Authorization': 'Token ' + localStorage.getItem('token'),
                    'Content-Type': 'application/json'
                };
            }
            
            function renderStudents(courseId, studentNames) {
                const startIndex = (currentPage - 1) * pageSize;
                const thead = document.querySelector('#attendanceTable thead tr');
                while (thead.children.length > 2) {
                    thead.deleteCell(2);
                }
                classDates.forEach((date, index) => {
                    const th = document.createElement('th');
                    th.textContent = `Buổi ${startIndex + index + 1}`;
                    th.title = `Ngày học: ${date}`;

                    thead.appendChild(th);
                });

                const tbody = document.getElementById('studentTableBody');
                tbody.innerHTML = '';
                studentNames.forEach(function(student, index) {
                    const row = document.createElement('tr');

                    const sttCell = document.createElement('td');
                    sttCell.textContent = index + 1; 
                    row.appendChild(sttCell);
                    const nameCell = document.createElement('td');
                    nameCell.textContent = student.name;
                    row.appendChild(nameCell);
                     

                    classDates.forEach((date) => {
                        console.log(student.id);
                        const cell = document.createElement('td');
                        const input = document.createElement('input');
                        input.type = 'text';
                        input.classList.add('form-control');
                        if (attendanceDataCache[date]) {
                            const attendance = attendanceDataCache[date].find(item => item.studentId === student.id);
                            if (attendance) {
                                input.value = attendance.status;
                            }
                        }
                            checkStatus(input);
            
                            input.onblur = function(event) {
                                event.preventDefault(); 
                                checkStatus(this); 
                                console.log(courseId, student.id, date, this.value);
                                saveAttendance(courseId, student.id, date, this.value);
                            };

                        cell.appendChild(input);
                        row.appendChild(cell);
                    });

                    tbody.appendChild(row);
                });
                attachInputNavigation()
            }
            function getAttendanceStatus(courseId, classDates) {
                $.ajax({
                    url: `http://127.0.0.1:8000/api/course/${courseId}/attendance/`, 
                    method: 'GET',
                    headers: getAuthHeaders(),
                    data: {
                        dates: classDates.join(','),
                    },
                    success: function(response) {
                        console.log(response);
                        classDates.forEach((date) => {
                            attendanceDataCache[date] = response[date];
                        });
                        console.log(attendanceDataCache);
                        renderStudents(courseId, studentNames);
                    },
                    error: function() {
                        alert("Không thể lấy trạng thái điểm danh.");
                    }
                });
                renderPagination(courseId);  
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
            function renderPagination(courseId) {
                const paginationContainer = $('#pagination');
                paginationContainer.html('');
                localStorage.setItem('currentPage', currentPage);
                for (let page = 1; page <= totalPages; page++) {
                    const pageLink = $('<a href="#" class="page-link">').text(page);
                    pageLink.on('click', function(e) {
                        e.preventDefault();
                        currentPage = page;
                        console.log("currentPage"+currentPage);
                        fetchCourseDetails(courseId, currentPage);
                        $('.page-item').removeClass('active');
                        $(this).parent().addClass('active');
                    });
                    const pageItem = $('<li class="page-item">')
                    .toggleClass('active', currentPage === page)
                    .append(pageLink);
        
                paginationContainer.append(pageItem);
                }
            }
function checkStatus(input) {
    if (input.value.toLowerCase() === "x") {
        input.style.backgroundColor = "#4CAF50"; 
        input.style.color = "#fff";
    } else if (input.value.toLowerCase() === "cp") {
        input.style.backgroundColor = "yellow";
        input.style.color = "#000";
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
