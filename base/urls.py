from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Включаем маршруты из приложения core
    path('', include('userauths.urls')),


    path('reset_password/', auth_views.PasswordResetView.as_view(),
         name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),


]

# Настройки для статических и медиафайлов
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
