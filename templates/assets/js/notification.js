$(document).ready(function () {
    const API_BASE_URL = "http://127.0.0.1:8000/api";
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('course_id');

    function loadNotifications() {
        $.ajax({
            url: `${API_BASE_URL}/courses/${courseId}/notifications/`,
            type: "GET",
            headers: getAuthHeaders(),
            success: function (data) {
                const notificationList = $("#notifications");
                notificationList.empty();
                const unreadIds = [];

                data.forEach(notification => {
                    if (!notification.is_read) {
                        unreadIds.push(notification.id);
                    }
                    const unreadBadge = !notification.is_read ? 
                        '<span class="badge bg-danger ms-2">Thông báo mới</span>' : '';

                    notificationList.append(`
                        <div class="notification" data-id="${notification.id}" data-is-read="${notification.is_read}">
                            <h3>${notification.title} ${unreadBadge}</h3>
                            <p>${notification.content}</p>
                            <small>Posted by: ${notification.created_by}</small>
                            <br>
                            <button class="toggle-comments-btn" data-id="${notification.id}">Show Comments</button>
                            <div class="comments" id="comments-${notification.id}" style="display: none;"></div>
                            <textarea id="new-comment-${notification.id}" placeholder="Write your comment here..."></textarea>
                            <button class="add-comment-btn" data-id="${notification.id}">Add Comment</button>
                        </div>
                    `);
                });

                if (unreadIds.length > 0) {
                    if (!sessionStorage.getItem('markedRead')) {
                        markNotificationsAsRead(unreadIds);
                        sessionStorage.setItem('markedRead', 'true');
                    }
                }
            },
            error: function (xhr, status, error) {
                console.error("Error loading notifications:", error);
                $("#notifications").html("<p>Could not load notifications. Please try again later.</p>");
            }
        });
    }

    $("#create-notification-btn").on("click", function (e) {
        e.preventDefault();
        
        const content = $("#new-notification-content").val().trim();
        const title =$("#title").val().trim();
        if (!content) {
            alert("Notification content cannot be empty!");
            return;
        }

        $.ajax({
            url: `${API_BASE_URL}/courses/${courseId}/notifications/`,
            type: "POST",
            headers: getAuthHeaders(),
            data: JSON.stringify({
                title: title,
                content: content,
            }),
            success: function () {
                $("#new-notification-content").val("");
                sessionStorage.removeItem('markedRead');
                loadNotifications();
            },
            error: function (xhr, status, error) {
                console.error("Error creating notification:", error);
                alert("Failed to create notification. Please try again.");
            }
        });
    });

    $(document).on("click", ".add-comment-btn", function () {
        const notificationId = $(this).data("id");
        const content = $(`#new-comment-${notificationId}`).val().trim();
        if (!content) {
            alert("Comment cannot be empty!");
            return;
        }

        $.ajax({
            url: `${API_BASE_URL}/notifications/${notificationId}/comments/`,
            type: "POST",
            headers: getAuthHeaders(),
            data: JSON.stringify({ content: content }),
            success: function () {
                $(`#new-comment-${notificationId}`).val("");
                loadComments(notificationId);
            },
            error: function (xhr, status, error) {
                console.error("Error adding comment:", error);
                alert("Failed to add comment. Please try again.");
            }
        });
    });

    $(document).on("click", ".toggle-comments-btn", function () {
        const notificationId = $(this).data("id");
        const commentsDiv = $(`#comments-${notificationId}`);
        if (commentsDiv.is(":visible")) {
            commentsDiv.hide();
        } else {
            loadComments(notificationId);
            commentsDiv.show();
        }
    });

    function loadComments(notificationId) {
        $.ajax({
            url: `${API_BASE_URL}/notifications/${notificationId}/comments/`,
            type: "GET",
            headers: getAuthHeaders(),
            success: function (data) {
                const commentsDiv = $(`#comments-${notificationId}`);
                commentsDiv.empty();
                data.forEach(comment => {
                    commentsDiv.append(`<div class="comment"><strong>${comment.created_by_name}:</strong> ${comment.content}</div>`);
                });
            },
            error: function (xhr, status, error) {
                console.error("Error loading comments:", error);
                $(`#comments-${notificationId}`).html("<p>Could not load comments. Please try again later.</p>");
            }
        });
    }

    function markNotificationsAsRead(notificationIds) {
        if (!notificationIds.length) return;
        
        $.ajax({
            url: `${API_BASE_URL}/notifications/mark-read/`,
            type: "POST",
            headers: getAuthHeaders(),
            data: JSON.stringify({ notification_ids: notificationIds }),
            contentType: "application/json",
            success: function() {
                console.log("Notifications marked as read");
            },
            error: function(xhr, status, error) {
                console.error("Error marking notifications as read:", error);
            }
        });
    }

    window.addEventListener('beforeunload', function() {
        sessionStorage.removeItem('markedRead');
    });

    loadNotifications();
});

function getAuthHeaders() {
    return {
        'Authorization': 'Token ' + localStorage.getItem('token'),
        'Content-Type': 'application/json'
    };
}