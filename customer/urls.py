from django.urls import path
from .import views
from customer.views import LoginView

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('customer-login/', LoginView.as_view(), name='login'),
    # path('register/', RegisterView.as_view(), name='register'),
    path('register/', views.register, name='register'),
    # path('customer-login/',views.LoginView.as_view(),name='customer_login'),
    path('customer-logout/',views.LogoutView.as_view(),name='customer_logout'),
    path('add-ads/',views.add_ads, name='add_ads'),
    path('pack_confirm/', views.pack_confirm, name = 'pack_confirm'),
    path('customer-profile/',views.customer_profile,name='customer_profile'),
    path('customer-control/',views.customer_control,name='customer_control'),
    path('password_update/',views.password_update,name='password_update'),
    path('password_success/',views.password_success,name='password_success'),
    path('edit-customer/',views.edit_customer, name='edit_customer'),
    path('<int:customer_id>/', views.orders, name='customer'),
    path('add_ads/',views.add_ads, name='add_ads'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('ads_checkout/',views.ads_checkout, name='ads_checkout'),
    path('gold_ads_checkout/',views.gold_ads_checkout, name='gold_ads_checkout'),
    path('silver_ads_checkout/',views.silver_ads_checkout, name='silver_ads_checkout'),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='customer/password_reset.html'), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='customer/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='customer/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='customer/password_reset_complete.html'), name="password_reset_complete"),
    
    # path('customer/customer_reset_password/' ,authViews.PasswordResetView.as_view(template_name= "customer/customer_password_reset.html") , name="customer_reset_password"),
    # path('customer/customer_reset_password_sent/' ,authViews.PasswordResetDoneView.as_view(template_name= "customer/customer_password_reset_sent.html") , name="customer_password_reset_done"),
    # path('customer/customer_reset/<uidb64>/<token>/' ,authViews.PasswordResetConfirmView.as_view(template_name= "customer/customer_password_reset_form.html") , name="customer_password_reset_confirm"),
    # path('customer/customer_reset_password_complete/' ,authViews.PasswordResetCompleteView.as_view(template_name= "customer/customer_password_reset_done.html") , name="customer_password_reset_complete")





]
