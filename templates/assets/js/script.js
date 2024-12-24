$(document).ready(function () {
  // Get user data from localStorage
  const userData = JSON.parse(localStorage.getItem("userData"));

  // Check if userData exists and has student_details
  if (userData && userData.student_details) {
    const userLevel = userData.student_details.level || "none";

    // Display level with appropriate text
    $("#level").text(userLevel === "none" ? "Chưa xác định" : userLevel);
  } else {
    // Handle case where data is not available
    $("#level").text("Chưa có thông tin");
  }
});

// Function to display course with completion
function displayCourseWithCompletion(course) {
  const courseHtml = `
          
                  
                  <p><strong>Cấp độ:</strong> ${course.level.toUpperCase()}</p>
                  
          
      `;

  $("#currentCourses").append(courseHtml);
  // Fetch completion for this course
  fetchAndDisplayCompletion(course.id);
}

// Example usage when loading courses
function loadCourses() {
  $.ajax({
    url: "http://127.0.0.1:8000/api/student/dashboard/",
    method: "GET",
    headers: {
      Authorization: `Token ${token}`,
    },
    success: function (response) {
      const courses = response.current_course || [];
      $("#currentCourses").empty();

      if (courses.length === 0) {
        $("#currentCourses").html("<p>Không có khóa học nào.</p>");
        return;
      }

      courses.forEach((course) => {
        displayCourseWithCompletion(course);
      });
    },
    error: function (xhr) {
      $("#currentCourses").html(`
                  <div class="alert alert-danger">
                      Không thể tải dữ liệu khóa học
                  </div>
              `);
    },
  });
}
