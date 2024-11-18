from django.contrib import admin

from .models import User, Question, Answer, FinalExam, PlacementTest

admin.site.register(User)



class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('text', 'audio_file', 'choice_a', 'choice_b', 'choice_c', 'choice_d', 'correct_answer', 'level')

@admin.register(FinalExam)
class FinalExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'level', 'final_exam', 'placement_test', 'correct_answer')
    list_filter = ('level', 'final_exam', 'placement_test')
    search_fields = ('text', 'choice_a', 'choice_b', 'choice_c', 'choice_d')
    
    def text_preview(self, obj):
        # Hiển thị preview của text với độ dài tối đa 50 ký tự
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Question Text'

    fieldsets = (
        ('Question Content', {
            'fields': ('text', 'audio_file')
        }),
        ('Choices', {
            'fields': ('choice_a', 'choice_b', 'choice_c', 'choice_d', 'correct_answer')
        }),
        ('Classification', {
            'fields': ('level', 'final_exam', 'placement_test')
        })
    )

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'question_preview', 'selected_answer', 'is_correct', 'exam_type')
    list_filter = ('is_correct', 'exam_type', 'student')
    search_fields = ('student__user__username', 'question__text')
    
    def question_preview(self, obj):
        return obj.question.text[:50] + "..." if len(obj.question.text) > 50 else obj.question.text
    question_preview.short_description = 'Question'