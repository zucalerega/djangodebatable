from django.shortcuts import render, redirect
from chat.models import Room, Message, Rating
from django.http import HttpResponse, JsonResponse
from datetime import datetime
import time
import random
import string
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest
from users.models import Profile
from django.contrib.auth.models import User
import numpy as np
from itertools import chain

def match(searching_users):
	for searching_user in searching_users.reverse():
		#print(1)
		if (int(searching_user.ideology) - 1) > int(searching_users.reverse()[0].ideology) or int(searching_users.reverse()[0].ideology) > (int(searching_user.ideology) + 1):
			#print(2)
			if searching_user.topic == searching_users.reverse()[0].topic:
				#print(3)
				if searching_user.style == searching_users.reverse()[0].style:
					if searching_users[0] != searching_users[1]:
						print([searching_users.reverse()[0], searching_user])
						return [searching_users.reverse()[0], searching_user]
	return []
	#return [searching_users[0], searching_users[1]]
def ajax_required(f):
   """
   AJAX request required decorator
   use it in your views:

   @ajax_required
   def my_view(request):
       ....

   """

   def wrap(request, *args, **kwargs):
       if not request.is_ajax():
           return HttpResponseBadRequest()
       return f(request, *args, **kwargs)

   wrap.__doc__=f.__doc__
   wrap.__name__=f.__name__
   return wrap


# The way to use this decorator is:

# Create your views here.
@login_required
def home(request):
	queryset = list(chain(Room.objects.filter(auo=request.user), Room.objects.filter(aut=request.user)))
	message_list = {}
	for i in queryset:
		if len(Message.objects.filter(room=i.id)) > 0:
			message_list[i] = Message.objects.filter(room=i.id).order_by('-date')[0]
		else:
			message_list[i] = 'No messages yet'
	context = {
		"object_list": queryset,
		"message_list": message_list
		}
	return render(request, "chathome.html", context)

@login_required
def room(request, room):
    searching_user = Profile.objects.get(user=request.user)
    room_obj = Room.objects.get(name=room)
    if room_obj.auo.replace(' Profile', '') == searching_user.user.username or room_obj.aut.replace(' Profile', '') == searching_user.user.username:
        pass
    else:
        return redirect('/chat/')

    searching_user.searching = False
    searching_user.save()
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    if str(room_obj.auo) == str(request.user):
        opponent = Profile.objects.get(user=User.objects.get(username=room_obj.aut.replace(' Profile', '')))
        me = Profile.objects.get(user=User.objects.get(username=room_obj.auo.replace(' Profile', '')))
    else:
        opponent = Profile.objects.get(user=User.objects.get(username=room_obj.auo.replace(' Profile', '')))
        me = Profile.objects.get(user=User.objects.get(username=room_obj.aut.replace(' Profile', '')))
    queryset = Message.objects.filter(room=room_details.id)
    object_list = list(chain(Room.objects.filter(auo=request.user), Room.objects.filter(aut=request.user)))
    message_list = {}
    for i in object_list:
        if len(Message.objects.filter(room=i.id)) > 0:
            message_list[i] = Message.objects.filter(room=i.id).order_by('-date')[0]
        else:
            message_list[i] = 'No messages yet'

    totalratings = len(Rating.objects.filter(recipient=str(opponent.user)))
    return render(request, 'room.html', {
        "object_list": object_list,
        "message_list": message_list,
        "username": username,
        "room": room,
        "room_details": room_details,
        "opponent": opponent,
        "totalratings": totalratings,
        "me": me,
        "messages": queryset
    })

def checkview(request):
    searching_user = Profile.objects.get(user=request.user)
    searching_user.room = 'null'
    searching_user.topic = request.POST.get('topic', 'general')
    searching_user.style = request.POST.get('chat-style', 'general')

    #print(searching_user.searching)
    searching_user.searching = True
    searching_user.save()
    searching_users = []
    #print(Profile.objects.filter(searching = True))
    while len(searching_users) < 2:
        try:
            searching_users = match(Profile.objects.filter(searching = True))
        except IndexError:
            searching_users = []
    print(searching_users)
    for i in searching_users:
        i.room = searching_users[0].bio + searching_users[1].bio
        #print(i, i.room)
        i.save()
    room = request.POST.get('room_name', i.room)
    if Room.objects.filter(name=room).exists():
        return redirect('/chat/' + room + '/')
    new_room = Room.objects.create(name=room, auo=searching_users[0].user.username, aut = searching_users[1].user.username, topic=request.POST.get('topic', 'general'))
    new_room.save()
    return redirect('/chat/' + room + '/')

def send(request):
    message = request.POST['message']
    #username = request.POST['username']
    room_id = request.POST['room_id']
    now = datetime.now()
    new_message = Message.objects.create(value=message, user=request.user, room=room_id, sender=request.user.username)
    new_message.save()
    return HttpResponse('Message sent yeeyye')

@ajax_required
def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})


def rateview(request, room):
	new_rating = Rating.objects.create(
	rater = request.user.username,
	recipient = request.POST['opponent'],
	rating = int(request.POST['rating']),
	message = request.POST['feedback']
	)
	opponent = Profile.objects.get(user=User.objects.get(username=request.POST['opponent']))
	# if int(request.POST['rating']) > 5:
	# 	opponent.rating = opponent.rating + np.sqrt(int(request.POST['rating'])*int(Profile.objects.get(user=User.objects.get(username=request.user)).rating))
	# elif int(request.POST['rating']) < 5:
	# 	if (opponent.rating - np.sqrt(int(request.POST['rating'])*int(Profile.objects.get(user=User.objects.get(username=request.user)).rating))) >= 1:
	# 		opponent.rating = opponent.rating - np.sqrt((10-int(request.POST['rating']))*int(Profile.objects.get(user=User.objects.get(username=request.user)).rating))
	# 	else:
	# 		opponent.rating = 1
	print(type(opponent.user))
	print(Rating.objects.filter(recipient=str(opponent.user)))
	r_sum = 0
	for i in Rating.objects.filter(recipient=str(opponent.user)):
		r_sum += i.rating

	opponent.rating = r_sum/len(Rating.objects.filter(recipient=str(opponent.user)))
	opponent.save()
	return redirect("/chat/")

def report(request, message, room):
	banned_words = ['fuck',
	'porn'
	]
	reporter = Profile.objects.get(user=User.objects.get(username=request.user))
	offender = Profile.objects.get(user=message.user)
	for word in banned_words:
		if word in message.value:
			message.reported = True
			message.save()
	print(message.reported)
	return redirect("/chat/" + room + "/")
