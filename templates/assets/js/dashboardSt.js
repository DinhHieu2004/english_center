$(document).ready(function () {
    const token = localStorage.getItem('token');
    const userType = localStorage.getItem('userType');
    const userData = JSON.parse(localStorage.getItem('userData'));
    if (!token) {
        return;
    }


    $('#fullName').text(userData.fullname);
    $('#email').text(userData.email);

    if (userData.student_details) {

        $('#level').text(userData.student_details.level || 'Chưa xác định');

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
    if (!userData.student_details.has_taken_test) {
        document.getElementById("takeTestButton").style.display = "inline-block";

        takeTestButton.addEventListener('click', function () {
            // Điều hướng đến trang làm bài kiểm tra
            window.location.href = 'entrance_test.html';
        });
    }
    //   if(userData.student_details.level ==   "none"){
    //      document.getElementById("level").text("chưa xác định");
    //  }
    // Xử lý đăng xuất
    $('#logoutBtn').click(function (event) {
        event.preventDefault();
        localStorage.removeItem('token');
        localStorage.removeItem('userType');
        localStorage.removeItem('userData');
        window.location.href = '../base.html';
    });
});
