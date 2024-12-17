document.addEventListener("DOMContentLoaded", () => {
    const notificationList = document.getElementById("notificationList");

    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('id'); 
    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/notifications/${courseId}/`);

    socket.onopen = () => {
        console.log("WebSocket kết nối thành công!");
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const { title, content, sender, time } = data;

        const notificationItem = document.createElement("li");
        notificationItem.classList.add("list-group-item");
        notificationItem.innerHTML = `
            <strong>${title}</strong><br>
            <small>Người gửi: ${sender} | Thời gian: ${time}</small><br>
            ${content}
        `;
        notificationList.appendChild(notificationItem);
    };

    socket.onclose = () => {
        console.log("WebSocket đã đóng kết nối!");
    };

    socket.onerror = (error) => {
        console.error("Lỗi WebSocket:", error);
    };
});