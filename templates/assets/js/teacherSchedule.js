$(document).ready(function() {
    const urlParams = new URLSearchParams(window.location.search);
    const teacherId = urlParams.get('id');

    if (teacherId) {
        loadScheduleForWeek();

        $('#loadSchedule').click(function() {
            loadScheduleForWeek();
        });
    } else {
        alert("Không có lớp học được tìm thấy.");
    }
});

function loadScheduleForWeek() {
    const teacherId = new URLSearchParams(window.location.search).get('id');
    const weekValue = $('#week-selector').val(); 
    let startDate, endDate;

    if (!weekValue) {
        const today = new Date();
        const firstDayOfWeek = new Date(today.setDate(today.getDate() - today.getDay() + 1));
        const lastDayOfWeek = new Date(today.setDate(firstDayOfWeek.getDate() + 6));
        const formatDate = (date) => {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        };

        startDate = formatDate(firstDayOfWeek);
        endDate = formatDate(lastDayOfWeek);
    } else {
        const year = parseInt(weekValue.split('-W')[0], 10);
        const week = parseInt(weekValue.split('-W')[1], 10);
        const firstDayOfYear = new Date(year, 0, 1);
        const daysOffset = (week - 1) * 7;

        const firstDayOfWeek = new Date(firstDayOfYear.setDate(firstDayOfYear.getDate() + daysOffset - firstDayOfYear.getDay() + 1));
        const lastDayOfWeek = new Date(firstDayOfWeek);
        lastDayOfWeek.setDate(firstDayOfWeek.getDate() + 6);

        const formatDate = (date) => {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        };

        startDate = formatDate(firstDayOfWeek);
        endDate = formatDate(lastDayOfWeek);
    }
    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); 
        const day = String(date.getDate()).padStart(2, '0'); 
        return `${year}-${month}-${day}`;
    };
    const weekStart = new Date(startDate);
    const weekEnd = new Date(endDate);
    document.getElementById('week-range').innerText = `Tuần: ${startDate} - ${endDate}`;

    $.ajax({
        url: `http://127.0.0.1:8000/api/teacher/${teacherId}/schedule/`,
        method: 'GET',
        headers: getAuthHeaders(),
        data: {
            start_date: formatDate(weekStart),
            end_date: formatDate(weekEnd) 
        },
        success: function(data) {
            console.log('Dữ liệu trả về từ API:', data);
        
            const tableBody = $('table.schedule-table tbody');
            const daysOfWeek = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật'];
        
            const length = data.all_sessions.length;

            const schedule = daysOfWeek.reduce((acc, day) => {
                acc[day] = new Array(length).fill(null); 
                return acc;
            }, {});
        
            Object.keys(data.teacher_schedule).forEach(function(dayIndex) {
                const daySchedule = data.teacher_schedule[dayIndex];
                const day = daysOfWeek[parseInt(dayIndex)]; 
                    for (let i = 1; i <= length; i++) {
                        if (daySchedule[i]) {
                            const classInfo = `${daySchedule[i].course_name}`;
                            schedule[day][i - 1] = classInfo; 
                        }
                    }
            });
            let rows = '';
            for (let i = 0; i < length; i++) {
                const session = data.all_sessions[i];
                const str = session.name + " (" + session.start_time + "-"+ session.end_time+ ")"
                rows += '<tr>';
                rows += `<td class="day-column"> ${str}</td>`;
                daysOfWeek.forEach(function(day) {
                    const daySchedule = schedule[day] || [];
                    const scheduleText = daySchedule[i] ? daySchedule[i] : '-----';
                    rows += `<td class="${daySchedule[i] ? '' : 'null'}">${scheduleText}</td>`;
                });
                rows += '</tr>';
            }
            tableBody.html(rows);
        },
        error: function(error) {
            console.log('Lỗi khi lấy dữ liệu:', error);
        }
    });
}

function filterClassesForWeek(classes, weekStart, weekEnd) {
    const classArray = Object.values(classes).filter(item => item !== null);

    return classArray.filter(function(item) {
        const classDate = new Date(item.class_date);
        return classDate >= weekStart && classDate <= weekEnd;
    });
}



function getAuthHeaders() {
    return {
        'Authorization': 'Token ' + localStorage.getItem('token'),
        'Content-Type': 'application/json'
    };
}
