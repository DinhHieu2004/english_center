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

    // Xử lý đăng xuất
    $('#logoutBtn').click(function (event) {
        event.preventDefault();
        localStorage.removeItem('token');
        localStorage.removeItem('userType');
        localStorage.removeItem('userData'); 
        window.location.href = '../base.html';
    });
});
let dayCount = 3; // Bắt đầu với 3 ngày

        function addColumn() {
            const dateInput = document.getElementById("dateInput"); // Lấy ngày từ input
            const selectedDate = dateInput.value;

            if (!selectedDate) {
                alert("Vui lòng chọn ngày.");
                return;
            }

            dayCount++; // Tăng số ngày lên 1

            // Lấy bảng, thêm cột vào tiêu đề (thead)
            const thead = document.querySelector("thead tr");
            const th = document.createElement("th");
            th.textContent = selectedDate;
            thead.appendChild(th);

            // Thêm cột vào phần thân bảng (tbody)
            const rows = document.querySelectorAll("tbody tr");
            rows.forEach(row => {
                const td = document.createElement("td");
                td.innerHTML = `<input type="text" class="status-input" oninput="checkStatus(this)">`;
                row.appendChild(td);
            });
        }

        function checkStatus(input) {
            if (input.value.toLowerCase() === "x") {
                input.style.backgroundColor = "#ffcccc"; // Đổi màu khi nhập "x"
            } else {
                input.style.backgroundColor = ""; // Đặt lại màu khi không phải "x"
            }
        }