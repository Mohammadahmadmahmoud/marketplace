from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from vendor.views import  LoginView

urlpatterns=[
 
    path('become-vendor/', views.become_vendor, name='become_vendor'),
    path('vendor-admin/', views.vendor_admin, name='vendor_admin'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-vendor/', views.edit_vendor, name='edit_vendor'),
    path('vendor_add_ads/', views.vendor_add_ads, name='vendor_add_ads'),
    path('vendor_ads_checkout/', views.vendor_ads_checkout, name='vendor_ads_checkout'),
    path('updateProduct/<int:pk>/', views.updateProduct, name='updateProduct'),
    path('deleteProduct/<int:pk>/', views.deleteProduct, name='deleteProduct'),
    path('update_vendor_ads/<int:pk>/', views.update_vendor_ads, name='update_vendor_ads'),
    path('delete_vendor_ads/<int:pk>/', views.delete_vendor_ads, name='delete_vendor_ads'),
    path('vendor_gold_ads_checkout/', views.vendor_gold_ads_checkout, name='vendor_gold_ads_checkout'),
    path('vendor_silver_ads_checkout/', views.vendor_silver_ads_checkout, name='vendor_silver_ads_checkout'),
    path('pdf/', views.html_to_pdf_view, name='pdf'),
    path('vendor-logout/', views.LogoutView.as_view(), name='vendor_logout'),
    path('vendor-login/', views.LoginView.as_view(), name='vendor_login'),
    path('vendor_reset_password/', auth_views.PasswordResetView.as_view(template_name="vendor/vendor_password_reset.html") , name="vendor_reset_password"),
    path('vendor_reset_password_sent/' , auth_views.PasswordResetDoneView.as_view(template_name="vendor/vendor_password_reset_sent.html") , name="vendor_password_reset_done"),
    path('reset/<uidb64>/<token>/' , auth_views.PasswordResetConfirmView.as_view(template_name="vendor/vendor_password_reset_form.html") , name="vendor_password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="vendor/vendor_password_reset_done.html") , name="vendor_password_reset_complete"),
    path('', views.vendors, name='vendors'),
    path('<int:vendor_id>/', views.vendor, name='vendor'),


]
