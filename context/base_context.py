from main_site.models import PersonalBlog
from django.contrib.auth.models import User
from django.conf import settings

def base_context(request):
	try:
		current_user = User.objects.get(username = request.user.username)
	except User.DoesNotExist:
		current_username = 'Гость'
	else:
		current_username = current_user.username
	all_users = User.objects.all()
	return {'current_username':current_username,'all_users':all_users}
    

def feed_list(request): #
    session = request.session
    notelist = session.get(settings.FEED_SESSION_ID)
    need_list = []
    if notelist!=None:
        for number in notelist.values():
            for sub_number in number:
                sub_number = int(sub_number)
                need_list.append(sub_number)
    
    return {'test_list':need_list}
    
    