from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/warehouse/')),  # 根路径重定向
    path('admin/', admin.site.urls),
    path('warehouse/', include('warehouse.urls')),  # 仓库应用
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    # 使用 Django 内置的 LogoutView
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]