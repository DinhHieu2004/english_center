from django.contrib import admin

from .models import User  # Hoặc import User từ app của bạn nếu nó khác

admin.site.register(User)