$(document).ready(function () {
  const token = localStorage.getItem("token");
  const userType = localStorage.getItem("userType");
  const userData = JSON.parse(localStorage.getItem("userData"));

  if (!token) {
    return;
  }
  if (userData) {
    $("#fullName").text(userData.fullname || "Không rõ");
    $("#email").text(userData.email || "Không rõ");
    $("#studentName").text(userData.fullname);

    if (userData.student_details) {
      $("#level").text(
        userData.student_details.level === "none"
          ? "Không xác định"
          : userData.student_details.level
      );
      if (userData.join_date) {
        const joinDate = new Date(userData.join_date);
        $("#joinDate").text(
          joinDate.toLocaleDateString("vi-VN", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
          })
        );
      } else {
        $("#joinDate").text("Chưa có thông tin");
      }
    }
  }
  $("#fullName").text(userData.fullname);
  $("#email").text(userData.email);

  if (userData.student_details) {
    const userLevel = userData.student_details.level || "none";

    $("#level").text(userLevel === "none" ? "Chưa xác định" : userLevel);

    if (userLevel === "none") {
      $("#takeTestButton").show();
      $("#takeTestButton").click(function () {
        window.location.href = "entrance_test.html";
      });
    } else {
      $("#takeTestButton").hide();
    }

    if (userData.join_date) {
      const joinDate = new Date(userData.join_date);
      const formattedDate = joinDate.toLocaleDateString("vi-VN", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
      });
      $("#joinDate").text(formattedDate);
    } else {
      $("#joinDate").text("Chưa có thông tin");
    }
  }

  //   if(userData.student_details.level ==   "none"){
  //      document.getElementById("level").text("chưa xác định");
  //  }
  // Xử lý đăng xuất
  $("#logoutBtn").click(function (event) {
    event.preventDefault();
    localStorage.removeItem("token");
    localStorage.removeItem("userType");
    localStorage.removeItem("userData");
    window.location.href = "../base.html";
  });

  function fetchDashboardData() {
    $.ajax({
      url: "http://127.0.0.1:8000/api/student/dashboard/",
      method: "GET",
      headers: {
        Authorization: `Token ${token}`,
      },
      success: function (response) {
        const is_register = response.current_course != null;
        console.log(is_register, typeof is_register);
        localStorage.setItem("is_register", is_register);
        if (is_register) {
          displayCurrentCourses(response.current_course, response.complete);
        } else {
          displayAvailableCourses(response.available_courses);
        }
      },
      error: function (xhr) {
        alert("Lỗi tải dữ liệu khóa học");
      },
    });
  }
async function checkForNewNotifications(courseId) {
    try {
        const response = await $.ajax({
            url: `http://127.0.0.1:8000/api/courses/${courseId}/check-new-notifications/`,
            method: 'GET',
            headers: getAuthHeaders()
        });
        return response.has_new_notification;
    } catch (error) {
        console.log("Không thể kiểm tra thông báo mới");
        return false;
    }
}
  //  khóa học hiện tại
  function displayCurrentCourses(course, complete) {
    console.log("Phần trăm hoàn thành:", complete, course.id);

    const coursesContainer = $("#currentCourses");
    coursesContainer.empty();

    checkForNewNotifications(course.id)
        .then(hasNewNotification => {
            const newNotificationBadge = hasNewNotification ? 
                '<span class="badge bg-danger ms-2">Có thông báo mới</span>' : '';

            const courseCard = `
              <div class="card mb-2">
                <div class="card-body">
                  <h5 class="card-title">${course.name} ${newNotificationBadge}</h5>
                  <p class="card-text">${course.description}</p>
                  <p><strong>Cấp độ:</strong> ${course.level.toUpperCase()}</p>
                  <p><strong>Ngày bắt đầu:</strong> ${new Date(course.start_date).toLocaleDateString()}</p>
                  <a href="course-detail.html?id=${course.id}">
                    <button class="btn btn-success look-course" data-course-id="${course.id}">
                      Xem khóa học
                    </button>
                  </a>
                </div>
              </div>
            `;
            coursesContainer.append(courseCard);

            const progressBar = $("#courseProgress");
            const courseNameElement = $(".courseName");
            courseNameElement.text("Khóa học " + course.level.toUpperCase());
            progressBar
                .css("width", `${complete}%`)
                .attr("aria-valuenow", complete)
                .text(`${complete}%`);

            // Kiểm tra nếu phần trăm hoàn thành là 100, tạo nút
            if (complete === 100) {
                const finalExamButton = `
                    <a href="final_test.html">
                        <button class="btn btn-warning w-100 mt-3">Làm bài kiểm tra cuối khóa</button>
                    </a>
                `;
                $("#final-exam-container").html(finalExamButton);
            } else {
                $("#final-exam-container").empty(); // Xóa nút nếu không đạt 100%
            }
        })
        .catch(error => {
            console.log("Lỗi khi kiểm tra thông báo mới:", error);
        });
}

function displayAvailableCourses(courses) {
  const registerContainer = $("#registerCourses");
  registerContainer.empty();

  if (!courses || courses.length === 0) {
      registerContainer.html("<p>Không có khóa học phù hợp hiện tại.</p>");
      return;
  }

  // Lấy thông tin userData từ localStorage
  const userData = JSON.parse(localStorage.getItem("userData") || "{}");
  const isOldStudent = userData.student_details.is_old_student || false;

  const coursesList = courses
      .map((course) => {
          let discountText = "";

          if (course.is_discounted && course.discounts && course.discounts.length > 0) {
              course.discounts.forEach((discount) => {
                  if (discount.for_old_students_only && !isOldStudent) {
                      return;
                  }

                  const discountInfo = `
                      <strong>${discount.name}</strong><br>
                      <strong>Loại:</strong> ${
                          discount.discount_type === "percent" ? "Phần trăm" : "Số tiền cố định"
                      }<br>
                      <strong>Giá trị:</strong> ${discount.value}${
                      discount.discount_type === "percent" ? "%" : " VNĐ"
                  }<br>
                      <strong>Bắt đầu:</strong> ${discount.start_date}<br>
                      <strong>Kết thúc:</strong> ${discount.end_date}
                  `;

                  discountText += `
                      <p 
                          class="card-text text-danger" 
                          data-bs-toggle="tooltip" 
                          data-bs-html="true"
                          title="${discountInfo}"
                      >
                          <strong>Đang giảm giá!</strong>
                      </p>
                  `;
              });
          }

          return `
              <div class="card mb-2">
                  <div class="card-body">
                      <p class="card-text">Mã khóa học: ${course.id}</p>
                      <p class="card-text">${course.name}</p>
                      <p class="card-text">${course.description}</p>
                      <p><strong>Cấp độ:</strong> ${course.level.toUpperCase()}</p>
                      ${discountText}
                      <a href="course-detail.html?id=${course.id}" >
                          <button class="btn btn-success look-course" data-course-id="${
                            course.id
                          }">
                              Xem khóa học
                          </button>
                      </a>
                  </div>
              </div>
          `;
      })
      .join("");
  registerContainer.html(`
      <h6>Các khóa học có thể đăng ký:</h6>
      ${coursesList}
  `);

  $('[data-bs-toggle="tooltip"]').tooltip();

  $(".look-course").on("click", function () {
      const courseId = $(this).data("course-id");
      window.location.href = `/course-detail.html?id=${courseId}`;
  });
}


  fetchDashboardData();
});
function getAuthHeaders() {
  return {
      'Authorization': 'Token ' + localStorage.getItem('token'),
      'Content-Type': 'application/json'
  };
}

