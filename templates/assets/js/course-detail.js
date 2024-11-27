 $(document).ready(function () {
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('id'); 

    if (courseId) {
        const apiUrl = `http://127.0.0.1:8000/api/course/${courseId}/`;
        $.get(apiUrl, function (data) {
            $('#course-title').text(`Tên khóa học: ${data.name}`);
            $('#course-level').text(data.level.toUpperCase());
            $('#course-description').text(data.description);
            $('#course-teacher').text(data.teacher);
            $('#course-students').text(data.students);
        }).fail(function () {
            alert('Không thể tải chi tiết khóa học.');
        });
    } else {
        alert('Không tìm thấy khóa học!');
    }
});