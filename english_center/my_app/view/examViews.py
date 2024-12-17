from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import PlacementTest, Question, Answer, TestResult, Student, FinalExam
from ..serializers import PlacementTestSerializer, QuestionSerializer, FinalExamSerializer
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


class PlacementTestView(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]  
    
    def get(self, request):

        try:
            test = PlacementTest.objects.first()
            if not test: 
                return Response({"error" : "chưa có bài test đầu vào"}, status = status.HTTP_404_NOT_FOUND)

            serializer = PlacementTestSerializer(test)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                  {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        try:
            logger.info(f"User attempting to submit test: {request.user}")
            
            if not request.user.is_authenticated:
                return Response(
                    {"error": "Vui lòng đăng nhập để lưu kết quả bài test"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            student = None
            try:
                student = Student.objects.get(user=request.user)
                logger.info(f"Found student: {student}")
            except Student.DoesNotExist:
                logger.error(f"No student profile found for user: {request.user}")
                return Response(
                    {"error": "Không tìm thấy thông tin học viên"}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            with transaction.atomic():
                test = PlacementTest.objects.select_related().first()
                if not test:
                    return Response(
                        {"error": "Không tìm thấy bài test"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )

                answers_data = request.data
                if not isinstance(answers_data, list):
                    return Response(
                        {"error": "Dữ liệu không hợp lệ"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

                logger.info(f"Processing {len(answers_data)} answers for student {student}")

                # Xóa các câu trả lời cũ
                old_answers = Answer.objects.filter(
                    student=student,
                    exam_type='placement',
                    question__placement_test=test
                )
                old_answers_count = old_answers.count()
                old_answers.delete()
                logger.info(f"Deleted {old_answers_count} old answers")

                # Tạo các câu trả lời mới
                correct_count = 0
                total_questions = test.questions.count()
                answers_to_create = []

                for answer_data in answers_data:
                    question_id = answer_data.get('question_id')
                    selected_answer = answer_data.get('selected_answer')

                    if not question_id or not selected_answer:
                        logger.warning(f"Skipping invalid answer data: {answer_data}")
                        continue

                    try:
                        question = test.questions.get(id=question_id)
                        is_correct = question.correct_answer == selected_answer
                        
                        if is_correct:
                            correct_count += 1

                        answer = Answer(
                            student=student,
                            question=question,
                            selected_answer=selected_answer,
                            is_correct=is_correct,
                            exam_type='placement'
                        )
                        answers_to_create.append(answer)
                        
                    except Question.DoesNotExist:
                        logger.warning(f"Question {question_id} not found")
                        continue

                # Lưu câu trả lời
                if answers_to_create:
                    created_answers = Answer.objects.bulk_create(answers_to_create)
                    logger.info(f"Created {len(created_answers)} new answers")

                # Tính điểm và xác định level
                score = (correct_count / total_questions * 100) if total_questions > 0 else 0
                level_after_test = self.determine_level(score)

                logger.info(f"Student {student} scored {score}% and achieved level {level_after_test}")

                # Lưu kết quả bài test placement vào TestResult
                test_result = TestResult.objects.create(
                    student=student,
                    test_type='placement',
                    score=score,
                    level=level_after_test,
                    total_questions=total_questions,
                    correct_answers=correct_count
                )
                logger.info(f"Created test result: {test_result}")

                # Cập nhật level cho student
                student.level = level_after_test
                student.has_taken_test = True
                student.save()
                logger.info(f"Updated student level to {level_after_test}")


            response = Response({
            "correct_answers": correct_count,
            "total_questions": total_questions,
            "score": round(score, 2),
            "level": level_after_test,
            "message": "Đã lưu kết quả bài test thành công"
           })
            """
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"
            """
            return response
                

        except Exception as e:
            logger.error(f"Error in POST: {str(e)}", exc_info=True)
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def determine_level(self, score):
        if score >= 85:
            return 'b2'
        elif score >= 70:
            return 'b1'
        elif score >= 50:
            return 'a2'
        else:
            return 'a1'
        
class FinalExamView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, exam_id):
        try:
            exam = FinalExam.objects.get(id=exam_id)
            serializer = FinalExamSerializer(exam)
            return Response(serializer.data)
        except FinalExam.DoesNotExist:
            return Response({"error": "Không tìm thấy bài kiểm tra"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, exam_id):
        try:
            if not request.user.is_authenticated:
                return Response({"error": "Vui lòng đăng nhập để lưu kết quả bài kiểm tra"}, status=status.HTTP_401_UNAUTHORIZED)

            student = Student.objects.get(user=request.user)
            with transaction.atomic():
                exam = FinalExam.objects.get(id=exam_id)
                answers_data = request.data
                if not isinstance(answers_data, list):
                    return Response({"error": "Dữ liệu không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)

                correct_count = 0
                total_questions = exam.questions.count()
                answers_to_create = []

                for answer_data in answers_data:
                    question_id = answer_data.get('question_id')
                    selected_answer = answer_data.get('selected_answer')

                    if not question_id or not selected_answer:
                        continue

                    question = exam.questions.get(id=question_id)
                    is_correct = question.correct_answer == selected_answer
                    if is_correct:
                        correct_count += 1

                    answer = Answer(
                        student=student,
                        question=question,
                        selected_answer=selected_answer,
                        is_correct=is_correct,
                        exam_type='final'
                    )
                    answers_to_create.append(answer)

                Answer.objects.bulk_create(answers_to_create)

                score = (correct_count / total_questions * 100) if total_questions > 0 else 0
                level_after_test = self.determine_level(score)

                test_result = TestResult.objects.create(
                    student=student,
                    test_type='final',
                    score=score,
                    level=level_after_test,
                    total_questions=total_questions,
                    correct_answers=correct_count
                )

                student.level = level_after_test
                student.has_taken_test = True
                student.save()

            return Response({
                "correct_answers": correct_count,
                "total_questions": total_questions,
                "score": round(score, 2),
                "level": level_after_test,
                "message": "Đã lưu kết quả bài kiểm tra thành công"
            })
        except FinalExam.DoesNotExist:
            return Response({"error": "Không tìm thấy bài kiểm tra"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def determine_level(self, score):
        if score >= 85:
            return 'b2'
        elif score >= 70:
            return 'b1'
        elif score >= 50:
            return 'a2'
        else:
            return 'a1'
