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
    path('rider', views.ordersRider, name='rider'),  
    path('merchants', merchants, name='merchants'),
    path('addproduct', views.addproduct, name='addproduct'),
    path('password_reset', signup, name='password_reset'),
    path('profile/', views.ProfileViews.as_view(), name='profile'),
    path('profilemerchants/', views.ProfileViewsMerchants.as_view(), name='profilemerchants'),
    path('address/', views.address, name='address'),
    path('merchantsaddress/', views.merchantsaddress ,name='merchantsaddress'),
    path('updateaddrider/<int:pk>', views.updateAddressMerchants.as_view(), name='updateaddrider'),
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
    path('ordersmc/', views.ordersmc, name='ordersmc'),
    path('done/', views.done, name='done'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    
    path('profilerider/', views.ProfileViewsRider.as_view(), name='profilerider'),
    path('rideraddress/', views.rideraddress ,name='rideraddress'),
    path('updatemerchants/<int:pk>', views.updateAddressRider.as_view(), name='updatemerchants'),

    path('dashboardcus/', views.dashboardcus , name = 'dashboardcus'),
    path('cancel-order/<int:order_id>/', views.cancel_order , name='cancel_order'),

    path('dashboardmer/', views.dashboardmer , name = 'dashboardmer'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('ridersave/<int:order_id>/', views.ridersave, name='ridersave'),
     path('savedorders/', views.savedorders, name='savedorders')

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)