from django.urls import path

from . import views

urlpatterns = [
	path('<int:rubric_pk>/<int:pk>', views.detail, name='detail_url'),
	path('<int:pk>', views.by_rubric, name='by_rubric_url'),
	path('accounts/profile/delete', views.DeleteUserView.as_view(), name='profile_delete_url'),
	path('accounts/register/activate/<str:sign>', views.user_activate, name='register_activate_url'),
	path('accounts/register/done', views.RegisterDoneView.as_view(), name='register_done_url'),
	path('accounts/register', views.RegisterUserView.as_view(), name='register_url'),
	path('accounts/profile/change_password', views.BBPasswordChangeView.as_view(), name='change_password_url'),
	path('accounts/profile/change_user_info', views.ChangeUserInfoView.as_view(), name='change_user_info_url'),
	path('accounts/profile', views.profile, name='profile_url'),
	path('accounts/login/', views.BBLoginView.as_view(), name='login_url'),
	path('accounts/logout/', views.BBLogoutView.as_view(), name='logout_url'),
	path('<str:page>', views.other_page, name='other_page_url'),
	path('', views.index, name="index_url"),
]