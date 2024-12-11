document.addEventListener("DOMContentLoaded", () => {
    const notificationList = document.getElementById("notificationList");
    const notificationForm = document.getElementById("newNotificationForm");

    // Kết nối WebSocket
    const courseId = 5; // ID của khóa học
    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/notifications/${courseId}/`);

    socket.onopen = () => {
        console.log("WebSocket kết nối thành công!");
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const { title, content, sender, time } = data;

        // Thêm thông báo mới vào danh sách
        const notificationItem = document.createElement("li");
        notificationItem.classList.add("list-group-item");
        notificationItem.innerHTML = `
            <strong>${title}</strong><br>
            <small>Người gửi: ${sender} | Thời gian: ${time}</small><br>
            ${content}
        `;
        notificationList.appendChild(notificationItem);
    };

    notificationForm.addEventListener("submit", (e) => {
        e.preventDefault();

        const title = document.getElementById("newNotificationTitle").value;
        const content = document.getElementById("newNotificationContent").value;
        const sender = 5; // Bạn có thể thay đổi thông tin này nếu cần
        const time = new Date().toISOString().slice(0, 19).replace("T", " ");

        // Gửi thông báo qua WebSocket
        const message = { title, content, sender, time };
        socket.send(JSON.stringify(message));

        // Xóa form sau khi gửi
        notificationForm.reset();
    });

    socket.onclose = () => {
        console.log("WebSocket đã đóng kết nối!");
    };

    socket.onerror = (error) => {
        console.error("Lỗi WebSocket:", error);
    };
});
