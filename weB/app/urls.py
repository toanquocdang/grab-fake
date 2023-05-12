from django.contrib import admin
from django.urls import path
from app.views import home, login, signup, customer, rider, merchants
from django.conf import settings
from django.conf.urls.static import static
from .import views
from django.contrib.auth import views as auth_view
from .forms import MyPasswordChangeForm, MySetPasswordForm,MyPasswordResetForm
urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('login', login, name='login'),
    path('signup/', signup, name='signup'),
    path('customer/', customer, name='customer'),
    path('rider', rider, name='rider'),  
    path('merchants', merchants, name='merchants'),
    path('password_reset', signup, name='password_reset'),
    path('profile/', views.ProfileViews.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateaddress/<int:pk>', views.updateAddress.as_view(), name='updateaddress'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='changepassword.html',form_class=MyPasswordChangeForm, success_url = '/passwordchangedone'), name = 'passwordchange'),
    path('passwordchangedone', auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name = 'passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page = 'home'), name='logout'),

    
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('paword-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name= 'password_reser_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('paword-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name= 'password_reser_complete.html'), name='password_reser_complete'),

    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout', views.checkout.as_view(), name='checkout'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('orders/', views.orders, name='orders'),
    path('done/', views.done, name='done'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)