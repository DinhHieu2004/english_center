$(document).ready(function () {
    const token = localStorage.getItem('token');
    const userData = JSON.parse(localStorage.getItem('userData'));
    const usertype = localStorage.getItem('userType');
    if (token) {
        document.getElementById("guestActions").classList.add("d-none");
        document.getElementById("userActions").classList.remove("d-none");
        $("#userName").text(userData.fullname);

    } else {
        document.getElementById("guestActions").classList.remove("d-none");
        document.getElementById("userActions").classList.add("d-none");
    }
    if (usertype === 'student') {
        profileLink.href = "/templates/student/dashboard.html";
    } else if (usertype === 'teacher') {
        profileLink.href = "/templates/teacher/dashboard.html";
    }
});
function getCSRFToken() {
    //var name = "csrftoken=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
        $("#loginForm").on("submit", function(event) {
            event.preventDefault(); 
            
            $.ajax({
        url: 'http://127.0.0.1:8000/api/login/',  
        method: 'POST',
        data: {
            username: $('#username').val(),
            password: $('#password').val()
        },
        success: function(response) {
            console.log(response);
            localStorage.setItem('token', response.token);
            localStorage.setItem('userType', response.user_type);
            localStorage.setItem('userData', JSON.stringify(response.user_data));
            if (response.message === 'Login successful') {
                document.getElementById("guestActions").classList.add("d-none");
                document.getElementById("userActions").classList.remove("d-none");
                $("#userName").text(response.user_data.fullname);
                const userType = response.user_type;
                
                if (userType === 'admin') {
                    window.location.href = '/templates/admin/dashboard.html';
                } else if (userType === 'student') {
                    profileLink.href = "/templates/student/dashboard.html";
                } else if (userType === 'teacher') {
                    profileLink.href = "/templates/teacher/dashboard.html";
                }
                $('#loginModal').modal('hide');
            } else {
                alert('Invalid credentials');
            }
        },
        error: function(err) {
            alert('Đăng nhập thất bại');
        }
    });
});
$(document).ready(function() {
    $('#studentRegisterForm').on('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            fullname: $('input[name="fullname"]').val(),
            username: $('input[name="username"]').val(),
            email: $('input[name="email"]').val(),
            phone: $('input[name="phone"]').val(),
            password: $('input[name="password"]').val(),
            password2: $('input[name="password2"]').val(),
            address: $('textarea[name="address"]').val(),
            date_of_birth: $('input[name="date_of_birth"]').val()
        };

        if (formData.password !== formData.password2) {
            alert('Mật khẩu xác nhận không khớp!');
            return;
        }

        $.ajax({
            url: 'http://127.0.0.1:8000/api/register/student/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            headers: {
               // 'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                alert('Đăng ký thành công!');
                $('#registerModal').modal('hide');
                $('#studentRegisterForm')[0].reset();
            },
            error: function(xhr) {
                if (xhr.responseJSON) {
                    const errors = xhr.responseJSON;
                    if (errors.username) {
                        alert('Lỗi tên đăng nhập: ' + errors.username.join(', '));
                    } else if (errors.email) {
                        alert('Lỗi email: ' + errors.email.join(', '));
                    } else if (errors.password) {
                        alert('Lỗi mật khẩu: ' + errors.password.join(', '));
                    } else {
                        alert('Đăng ký thất bại. Vui lòng kiểm tra lại thông tin.');
                    }
                } else {
                    alert('Có lỗi xảy ra. Vui lòng thử lại sau.');
                }
            }
        });
    });
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    $('#registerModal').on('hidden.bs.modal', function() {
        $('#studentRegisterForm')[0].reset();
    });

    $('input[name="password2"]').on('input', function() {
        const password = $('input[name="password"]').val();
        const password2 = $(this).val();
        
        if (password2 && password !== password2) {
            $(this).addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
});
$('#logoutButton').click(function (event) {
    event.preventDefault();
    localStorage.clear();
    window.location.href = '/templates/base.html';
});$(document).ready(function () {
    function fetchCourses() {
      $.ajax({
        url: 'http://127.0.0.1:8000/api/course/',  
        method: 'GET',
        success: function (response) {
            let discountContent = '';
            response.forEach(function(item) {
                let discount = item.discount;
                let courses = item.courses;
                
                // Thêm thông tin giảm giá vào nội dung
                discountContent += `
                <div id="discount-banner" class="alert alert-danger">
                    <strong class="discount-heading">${discount.name}</strong><br>
                    <strong class="discount-details">Giảm giá: ${discount.value}%</strong><br>
                    <strong class="discount-dates">Thời gian: Từ ${discount.start_date} đến ${discount.end_date}</strong>
                    </div>
                `;
                discountContent += '<div class="d-flex flex-wrap justify-content-between">';
                // Vòng lặp qua từng khóa học trong chương trình giảm giá
                if (courses.length > 0) {
                    courses.forEach(function(course) {
                        discountContent += `
                           <div class="card mb-2">
                                <div class="card-body">
                                    <h4 class="card-title">Khóa học - ${course.level.toUpperCase()}</h4>
                                    <p class="card-text inline"><strong>Mã khóa học:</strong> ${course.id} <strong>Số buổi:</strong> ${course.total_session}</p>
                                    <p class="card-text"><strong>Mô tả:</strong> ${course.description}</p>
                                    <p class="card-text"><strong>Cấp độ:</strong> ${course.level.toUpperCase()}</p>
                                    <p class="card-text"><strong>Bắt đầu:</strong> ${course.start_date}</p>
                                    <ul>
                                    ${course.schedules.map(schedule => `
                                    <li>
                                        <strong>Thứ:</strong> ${schedule.weekday_display}, 
                                        <strong>Giờ bắt đầu:</strong> ${schedule.session},
                        
                                    </li>
                                    `).join('')}
                                    </ul>
                                </div>
                            </div>
                        `;
                    });
                    discountContent += '</ul>';
                } else {
                    discountContent += '<p>Không có khóa học nào trong chương trình giảm giá này.</p>';
                }

                discountContent += '</div>';
            });

            $('#discounts-container').html(discountContent);
        },
         
      });
    }

    fetchCourses();
});