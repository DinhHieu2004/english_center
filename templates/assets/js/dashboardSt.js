$(document).ready(function () {
  const token = localStorage.getItem("token");
  const userType = localStorage.getItem("userType");
  const userData = JSON.parse(localStorage.getItem("userData"));
  console.log(token);
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
        is_register =
          Array.isArray(response.current_course) &&
          response.current_course.length > 0;
        console.log(is_register, typeof is_register);
        localStorage.setItem("is_register", is_register);
        if (is_register) {
          displayCurrentCourses(response.current_course);
        } else {
          displayAvailableCourses(response.available_courses);
        }
      },
      error: function (xhr) {
        alert("Lỗi tải dữ liệu khóa học");
      },
    });
  }

<<<<<<< HEAD
  //  khóa học hiện tại
  function displayCurrentCourses(courses) {
    const coursesContainer = $("#currentCourses");
    coursesContainer.empty();

    courses.forEach((course) => {
      const courseCard = `
=======
    function fetchDashboardData() {
        $.ajax({
            url: 'http://127.0.0.1:8000/api/student/dashboard/',
            method: 'GET',
            headers: {
                'Authorization': `Token ${token}`
            },
            success: function(response) {
                const is_register = response.current_course != null;
                console.log(is_register, typeof is_register)
                localStorage.setItem('is_register', is_register)
                if(is_register){
                    displayCurrentCourses(response.current_course, response.complete)
                }else{
                    displayAvailableCourses(response.available_courses)
                }
            },
            error: function(xhr) {
                alert('Lỗi tải dữ liệu khóa học');
            }
        });
    }

    //  khóa học hiện tại
    function displayCurrentCourses(course, complete) {
        const coursesContainer = $('#currentCourses');
        coursesContainer.empty();
    
            const courseCard = `
>>>>>>> 0a61a83ec1b61ff91c86eed1b7b112411d5a2c00
                <div class="card mb-2">
                    <div class="card-body">
                        <h5 class="card-title">${course.name}</h5>
                        <p class="card-text">${course.description}</p>
                        <p><strong>Trình độ:</strong> ${course.level.toUpperCase()}</p>
                        <p><strong>Hoàn thành:</strong> ${course.completion_percentage.toFixed(
                          2
                        )}%</p>
                        <p><strong>Ngày bắt đầu:</strong> ${new Date(
                          course.start_date
                        ).toLocaleDateString()}</p>
                    </div>
                </div>
            `;
<<<<<<< HEAD
      coursesContainer.append(courseCard);
    });
  }

  //  khóa học có thể đăng ký
  function displayAvailableCourses(courses) {
    const registerContainer = $("#registerCourses");
    registerContainer.empty();

    if (!courses || courses.length === 0) {
      registerContainer.html("<p>Không có khóa học phù hợp hiện tại.</p>");
      return;
    }

    const coursesList = courses
      .map(
        (course) => `
            <div class="card mb-2">
                <div class="card-body">
                    <p class="card-text"> Mã khóa học :${course.id}</p>

                    <p class="card-text">${course.name}</p>
                    <p class="card-text">${course.description}</p>

                    <p><strong>Cấp độ:</strong> ${course.level.toUpperCase()}</p>
                    <a href="course-detail.html?id=${course.id}" >
                    <button class="btn btn-success look-course" data-course-id="${
                      course.id
                    }">
                        Xem khóa học
                    </button>
                     <a>
                </div>
            </div>
        `
      )
      .join("");

    registerContainer.html(`
=======
            coursesContainer.append(courseCard);
        const progressBar = $('#courseProgress');
        const courseNameElement = $('.courseName');
        courseNameElement.text("Khóa học " + course.level.toUpperCase());
        progressBar.css('width', `${complete}%`).attr('aria-valuenow', complete).text(`${complete}%`);
    }
    function displayAvailableCourses(courses) {
        const registerContainer = $('#registerCourses');
        registerContainer.empty();

        if (!courses || courses.length === 0) {
            registerContainer.html('<p>Không có khóa học phù hợp hiện tại.</p>');
            return;
        }

        const  coursesList = courses.map(course => {
            let discountText = '';
            if (course.is_discounted) {
                discountText = `<p class="card-text text-danger"><strong>Đang giảm giá!</strong></p>`;
            }
    
            return `
                <div class="card mb-2">
                    <div class="card-body">
                        <p class="card-text"> Mã khóa học :${course.id}</p>
    
                        <p class="card-text">${course.name}</p>
                        <p class="card-text">${course.description}</p>
    
                        <p><strong>Cấp độ:</strong> ${course.level.toUpperCase()}</p>
    
                        ${discountText}
    
                        <a href="course-detail.html?id=${course.id}" >
                            <button class="btn btn-success look-course" data-course-id="${course.id}">
                                Xem khóa học
                            </button>
                        </a>
                    </div>
                </div>
            `;
        }).join('');
        registerContainer.html(`
>>>>>>> 0a61a83ec1b61ff91c86eed1b7b112411d5a2c00
            <h6>Các khóa học có thể đăng ký:</h6>
            ${coursesList}
        `);

    $(".look-course").on("click", function () {
      const courseId = $(this).data("course-id");
      window.location.href = `/course-detail.html?id=${courseId}`;
    });
  }

  fetchDashboardData();
});
