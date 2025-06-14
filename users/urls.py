from django.contrib.auth.views import LoginView
from django.urls import path
from users.apps import UsersConfig
from users.views import PaymentsCreateApiView, PaymentsUpdateApiView, PaymentsRetrieveApiView, PaymentsDestroyApiView, \
    PaymentsListApiView, logout_view, UserListView, UserDeleteView, UserUpdateView,UserCreateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', UserCreateView.as_view(template_name="user_form.html"), name='register'),
    # path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path("payments/", PaymentsListApiView.as_view(), name="payments_list"),
    path("payments/<int:pk>/", PaymentsRetrieveApiView.as_view(), name="payment_retrieve"),
    path("payments/create/", PaymentsCreateApiView.as_view(), name="payment_create"),
    path("payments/<int:pk>/delete/", PaymentsDestroyApiView.as_view(), name="payment_delete"),
    path("payments/<int:pk>/update/", PaymentsUpdateApiView.as_view(), name="payment_update"),
]