from main_site.models import PersonalBlog
from django.contrib.auth.models import User
def base_context(request):
	try:
		current_user = User.objects.get(username = request.user.username)
	except User.DoesNotExist:
		current_username = 'Гость'
	else:
		current_username = current_user.username
	all_users = User.objects.all()
	return {'current_username':current_username,'all_users':all_users}