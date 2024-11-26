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