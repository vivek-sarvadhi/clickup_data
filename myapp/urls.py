from django.urls import path
from myapp.views import RegisterView,LoginView, IndexView, ResultView
from django.contrib.auth import views as auth_views
# from django.contrib.auth import views as auth_views
# from django.urls import reverse_lazy
# from users.users_api.views import IndexAPIView

urlpatterns = [
	path('register/', RegisterView.as_view(), name="register"),
	path('login/', LoginView.as_view(), name="login"),
	path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

	path('index/', IndexView.as_view(), name="index"),
	path('result/', ResultView.as_view(), name="result"),
]