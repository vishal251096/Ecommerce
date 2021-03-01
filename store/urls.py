from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, UserPasswordResetForm, UserSetPasswordForm

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='show_cart'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('category/<slug:data>/', views.CategoryView.as_view(), name='categorydata'),
    path('brand/', views.BrandView.as_view(), name='brand'),
    path('brand/<slug:data>/', views.BrandView.as_view(), name='branddata'),
    path('tracking/', views.TrackingView.as_view(), name='tracking'),
    path('confirmation/', views.ConfirmationView.as_view(), name='confirmation'),
    path('elements/', views.ElementsView.as_view(), name='elements'),
    path('account/register/', views.UserRegistrationView.as_view(), name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html', form_class=LoginForm), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('account/reset_password', auth_views.PasswordResetView.as_view(template_name='passwordreset.html', form_class=UserPasswordResetForm), name='password_reset'),
    path('account/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='passwordresetdone.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=UserSetPasswordForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),
    path('shippingaddress/', views.ShippingAddressView.as_view(), name='shippingaddresscreate'),
    path('shippingdetail/', views.ShippingAddressListView.as_view(), name='shipping_list'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('search/', views.search, name='search'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('payment/paytm/', views.paytm_payment, name='paytm_payment'),
    path('response/', views.response, name='response'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)