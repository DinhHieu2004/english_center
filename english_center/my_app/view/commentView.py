from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Comment, Notification
from ..serializers import CommentSerializer

class CommentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            comments = notification.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, notification_id):
        # Kiểm tra xem Notification có tồn tại hay không
        try:
            notification = Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

        # Log thông tin người dùng (nên sử dụng logging thay vì print)
        print(f"User ID: {request.user.id}, Username: {request.user.username}")

        # Sao chép và thêm dữ liệu 'notification' vào payload
        data = request.data.copy()
        data['notification'] = notification.id 

        # Khởi tạo serializer với dữ liệu
        serializer = CommentSerializer(data=data)
        
        if serializer.is_valid():
            # Lưu dữ liệu, thêm trường created_by
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Trả về lỗi nếu dữ liệu không hợp lệ
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)