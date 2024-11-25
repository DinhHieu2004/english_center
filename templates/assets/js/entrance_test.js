class TOEICTest {
    constructor() {
        this.questions = [];
        this.duration = 0;
        this.timer = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        $('#submit-test').click(() => this.handleSubmit());
        $(window).on('beforeunload', () => {
            return 'Bạn có chắc muốn rời khỏi trang? Dữ liệu bài làm sẽ bị mất.';
        });
    }

    async initTest() {
        try {
            const response = await $.ajax({
                url: 'http://127.0.0.1:8000/api/placement-test/',
                method: 'GET',
                headers: {
                    'Authorization': 'Token ' + localStorage.getItem('token')
                }
            });

            this.questions = response.questions;
            this.duration = response.duration;
            
            this.displayTestInfo(response);
            this.sortAndDisplayQuestions();
            this.startTimer(this.duration * 60);
        } catch (error) {
            this.showError('Không thể tải bài kiểm tra. Vui lòng thử lại sau.');
        }
    }

    displayTestInfo(testData) {
        $('#test-description').html(`
            <p class="mb-2">${testData.description}</p>
            <p class="mb-0"><strong>Thời gian làm bài:</strong> ${testData.duration} phút</p>
        `);
    }

    sortAndDisplayQuestions() {
        const listeningQuestions = this.questions.filter(q => q.audio_file);
        const readingQuestions = this.questions.filter(q => !q.audio_file);

        $('#listening-questions').html(this.generateQuestionsHTML(listeningQuestions, true));
        $('#reading-questions').html(this.generateQuestionsHTML(readingQuestions, false));
    }

    generateQuestionsHTML(questions, isListening) {
        return questions.map((question, index) => `
            <div class="question" data-id="${question.id}">
                <p class="h5 mb-3">Câu ${index + 1}:</p>
                <p>${question.text}</p>
                ${isListening ? `
                    <audio controls class="mb-3">
                        <source src="${question.audio_file}" type="audio/mpeg">
                        Trình duyệt của bạn không hỗ trợ phát âm thanh.
                    </audio>
                ` : ''}
                <div class="options">
                    ${['a', 'b', 'c', 'd'].map(option => `
                        <div class="form-check">
                            <input class="form-check-input" type="radio" 
                                name="question${question.id}" 
                                id="q${question.id}${option}" 
                                value="${option.toUpperCase()}">
                            <label class="form-check-label" for="q${question.id}${option}">
                                ${question[`choice_${option}`]}
                            </label>
                        </div>
                    `).join('')}
                </div>
            </div>
        `).join('');
    }

    startTimer(duration) {
        let timer = duration;
        this.timer = setInterval(() => {
            const minutes = Math.floor(timer / 60);
            const seconds = timer % 60;

            $('#countdown').text(
                `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
            );

            if (--timer < 0) {
                clearInterval(this.timer);
                this.handleSubmit(true);
            }
        }, 1000);
    }

    async handleSubmit(isAutoSubmit = false) {
        if (!isAutoSubmit && !confirm('Bạn có chắc chắn muốn nộp bài?')) {
            return;
        }

        const answers = this.questions.map(question => ({
            question_id: question.id,
            selected_answer: $(`input[name="question${question.id}"]:checked`).val() || null
        })).filter(answer => answer.selected_answer);

        try {
            const response = await $.ajax({
                url: 'http://127.0.0.1:8000/api/placement-test/',
                method: 'POST',
                headers: {
                    'Authorization': 'Token ' + localStorage.getItem('token'),
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify(answers)
            });

            clearInterval(this.timer);
            $(window).off('beforeunload');
            
            this.showResult(response);
        } catch (error) {
            this.showError('Có lỗi xảy ra khi nộp bài. Vui lòng thử lại.');
        }
    }

    showResult(result) {
        const resultMessage = `
            Bạn đã hoàn thành bài kiểm tra!
            Số câu đúng: ${result.correct_answers}/${result.total_questions}
            Điểm số: ${result.score}%
            Trình độ: ${result.level.toUpperCase()}
        `;
        alert(resultMessage);
        window.location.href = '/test-result/';
    }

    showError(message) {
        const errorDiv = $('#error-message');
        errorDiv.text(message).slideDown();
        setTimeout(() => errorDiv.slideUp(), 5000);
    }
}

$(document).ready(() => {
    const test = new TOEICTest();
    test.initTest();
});