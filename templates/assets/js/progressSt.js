// Dữ liệu mẫu: thông tin các khóa học
const courses = [
    { name: "A1", totalSessions: 20 },
    { name: "A2", totalSessions: 20 },
    { name: "B1", totalSessions: 20 },
    { name: "B2", totalSessions: 20 }
];

// Trạng thái học viên (giả sử từ API hoặc cơ sở dữ liệu)
const studentProgress = {
    currentCourse: "A2", // Khóa đang học
    completedSessions: 8, // Số buổi đã hoàn thành trong khóa hiện tại
};

// Hàm hiển thị tiến độ các khóa học
function renderCourseProgress(courses, progress) {
    const container = document.getElementById("courseProgress");
    container.innerHTML = "";

    courses.forEach((course, index) => {
        let statusHTML = "";

        // Xác định trạng thái từng khóa học
        if (index < courses.findIndex(c => c.name === progress.currentCourse)) {
            // Các khóa đã hoàn thành
            statusHTML = `
                <div class="mb-3">
                    <h6>Khóa học ${course.name}</h6>
                    <div class="progress">
                        <div class="progress-bar bg-success" role="progressbar" style="width: 100%" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
                            Hoàn thành 100% (${course.totalSessions}/${course.totalSessions} buổi)
                        </div>
                    </div>
                </div>
            `;
        } else if (course.name === progress.currentCourse) {
            // Khóa đang học
            const percentage = Math.round((progress.completedSessions / course.totalSessions) * 100);
            statusHTML = `
                <div class="mb-3">
                    <h6>Khóa học ${course.name}</h6>
                    <div class="progress">
                        <div class="progress-bar bg-info" role="progressbar" style="width: ${percentage}%" aria-valuenow="${percentage}" aria-valuemin="0" aria-valuemax="100">
                            Đang học ${percentage}% (${progress.completedSessions}/${course.totalSessions} buổi)
                        </div>
                    </div>
                </div>
            `;
        } else {
            // Các khóa chưa bắt đầu
            statusHTML = `
                <div class="mb-3">
                    <h6>Khóa học ${course.name}</h6>
                    <div class="progress">
                        <div class="progress-bar bg-secondary" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
                            Chưa bắt đầu (0/${course.totalSessions} buổi)
                        </div>
                    </div>
                </div>
            `;
        }

        container.innerHTML += statusHTML;
    });
}

// Gọi hàm để hiển thị tiến độ
renderCourseProgress(courses, studentProgress);
