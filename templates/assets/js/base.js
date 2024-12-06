
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
            localStorage.setItem('token', response.token);
            localStorage.setItem('userType', response.user_type);
            localStorage.setItem('userData', JSON.stringify(response.user_data));
            if (response.message === 'Login successful') {
                const userType = response.user_type;
                
                if (userType === 'admin') {
                    window.location.href = '/templates/admin/dashboard.html';
                } else if (userType === 'student') {
                    window.location.href = '/templates/student/dashboard.html';
                } else if (userType === 'teacher') {
                    window.location.href = '/templates/teacher/dashboard.html';
                }
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