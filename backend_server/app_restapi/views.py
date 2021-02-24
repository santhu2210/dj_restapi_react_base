from django.shortcuts import render
import os
import shutil
from datetime import datetime,timedelta
from ast import literal_eval
import json
import logging
import logging.handlers as handlers
import time

from django.db.models import Q
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User

from baseproject.about import __version__ as version, __title__ as project_name
from app_restapi.models import UserProfile
from app_restapi.serializers import UserSerializer, UserProfileSerializer


# Logger Config
logger = logging.getLogger(project_name)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

logHandler = handlers.TimedRotatingFileHandler(os.path.join(settings.LOG_DIR, project_name+"_v{}_info.log".format(version)), when='midnight', interval=1, backupCount=0)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)
logHandler.suffix = "%d-%m-%Y"

errorLogHandler = handlers.TimedRotatingFileHandler(os.path.join(settings.LOG_DIR, project_name+"_v{}_error.log".format(version)), when='midnight', interval=1, backupCount=0)
errorLogHandler.setLevel(logging.ERROR)
errorLogHandler.setFormatter(formatter)
errorLogHandler.suffix = "%d-%m-%Y"

logger.addHandler(logHandler)
logger.addHandler(errorLogHandler)

logger.info("Initializing the User Management API service Main engine...")


class Home(generics.ListCreateAPIView):
	if settings.USE_TOKEN:
		permission_classes = (IsAuthenticated, )
		authentication_classes = (JSONWebTokenAuthentication, )

	def get(self, request, format=None):
		logger.info("Calling home endpoint (GET) url by {}".format(request.user))
		return Response({'success': True,'Message':"Welcome to the User Management API service!.."}, status=status.HTTP_200_OK)


class UserCreateList(generics.ListCreateAPIView):
	# if settings.USE_TOKEN:
	# 	permission_classes = (IsAuthenticated, )
	# 	authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (AllowAny, )

    def post(self,request):
        user = request.data.get('user')
        if not user:
            return Response({'response' : 'error', 'message' : 'No data found'})
        serializer = UserSerializer(data = user)
        if serializer.is_valid():
            saved_user = serializer.save()
        else:
            return Response({"response" : "error", "message" : serializer.errors})
        return Response({"response" : "success", "message" : "user created succesfully"})


class ProfileCreateList(generics.ListCreateAPIView):
	# if settings.USE_TOKEN:
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self,request):
        up_obj = UserProfile.objects.filter(user_id=request.user).values()
        if up_obj:
        	return Response({'response' : 'success', 'data' : up_obj})
        else:
        	return Response({'response' : 'error', 'message' : 'No profile data found'})


class GetUser(generics.ListCreateAPIView):

	permission_classes = (AllowAny, )

	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response(serializer.data)


class ProfileUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    
    def put(self,request):
        profile = request.data.get('profile')
        if not profile:
            return Response({'response' : 'error', 'message' : 'No profile data found'})

        # user_obj = User.objects.get(pk=request.user)
        # serializer = UserProfileSerializer(user=user_obj.id, data = profile)
        # if serializer.is_valid():
        #     saved_user = serializer.save()
        # else:
        #     return Response({"response" : "error", "message" : serializer.errors})
        # return Response({"response" : "success", "message" : "user profile updated succesfully"})
        

        # user_obj = UserProfile.objects.get(user_id=request.user)
        # user_obj.telephone = profile['telephone']
        # user_obj.email = profile['email']
        # user_obj.save()

        if UserProfile.objects.filter(user_id=request.user).exists():
            UserProfile.objects.filter(user_id=request.user).update(**profile)
            return Response({"response" : "success", "message" : "user profile updated succesfully"})
        else:
        	up_obj = UserProfile.objects.create(user_id=request.user)
        	up_obj.update(**profile)
        	return Response({'response' : 'error', 'message' : 'No profile data found in DB, so created justnow'})

# class RoomBooking(generics.ListCreateAPIView):
# 	permission_classes = (IsAuthenticated, )
# 	authentication_classes = (JSONWebTokenAuthentication, )

# 	def post(self, request, format=None):
# 		logger.info("Calling rooms booking endpoint (POST) url by {}".format(request.user))	
# 		logger.info("request data : {}".format(request.data))	
# 		try:		
# 			dt_obj = datetime.strptime(request.data['date'], '%d-%m-%Y').date()
# 			room_id=int(request.data['room'])
# 			title = request.data['title']
# 			description = request.data['description']
# 			start = datetime.strptime(request.data['start'], '%H:%M').time()
# 			end = datetime.strptime(request.data['end'], '%H:%M').time()
# 			members_list = literal_eval(request.POST.get("members", str([request.user.id]))) #if No members list, created user assigned by default

# 			mod_start = (datetime.strptime(request.data['start'], '%H:%M')+timedelta(seconds=1)).time()		
# 			mod_end = (datetime.strptime(request.data['end'], '%H:%M')-timedelta(seconds=1)).time()

# 			booked_rooms = Booking.objects.filter(Q(start__range=(mod_start, end)) | Q(end__range=(mod_start, end)), date=dt_obj, room=room_id)
# 			logger.info("booked_rooms data : {}".format(booked_rooms))
			
# 			if booked_rooms:
# 				book_response = {'success': False,'Message':"Room No. {} is already booked on given time. Please change the timing and try".format(room_id)}
# 				return Response(book_response, status=status.HTTP_200_OK)
# 			else:

# 				booking_req_data = {"title": title, "description": description, "date": dt_obj , "start": mod_start,"end":end,
# 								"room": room_id, "created_by": request.user.id,"is_delete":False,"created_at": datetime.now(),"members": members_list}

# 				book_serializer = BookingSerializer(data=booking_req_data)

# 				if book_serializer.is_valid():
# 					book_serializer.save()
# 					logger.info("Room is booked on requested datetime ")
# 					book_response = {'success': True,'Message':"Room No. {} is booked.".format(room_id)}
# 					return Response(book_response, status=status.HTTP_201_CREATED)
# 				else:
# 					book_response = {'success': False,'Message':book_serializer.errors}
# 					return Response(book_response, status=status.HTTP_406_NOT_ACCEPTABLE)

# 		except Exception as e:
# 			logger.exception("Exception raised at rooms booking endpoint : {}".format(str(e)))
# 			book_response = {'success': False,'Message':"{} Exception raised, Please check the form-data fields".format(str(e))}
# 			return Response(book_response, status=status.HTTP_406_NOT_ACCEPTABLE)		


# class FreeRoomsList(generics.ListCreateAPIView):
# 	permission_classes = (IsAuthenticated, )
# 	authentication_classes = (JSONWebTokenAuthentication, )

# 	def get(self, request, format=None):
# 		try:
# 			logger.info("Calling Free rooms check endpoint (GET) url by {}".format(request.user))	
# 			dt_obj = datetime.strptime(request.GET['date'], '%d-%m-%Y').date()
# 			start = datetime.strptime(request.GET['start'], '%H:%M').time()
# 			end = datetime.strptime(request.GET['end'], '%H:%M').time()

# 			mod_start = (datetime.strptime(request.GET['start'], '%H:%M')+timedelta(seconds=1)).time()		
# 			mod_end = (datetime.strptime(request.GET['end'], '%H:%M')-timedelta(seconds=1)).time()

# 			booked_rooms = Booking.objects.filter(Q(start__range=(mod_start, end)) | Q(end__range=(mod_start, end)), date=dt_obj)
# 			booked_rooms_list = [br.room.id for br in booked_rooms ]
# 			logger.info("booked rooms list on mention datetime {}".format(booked_rooms_list))

# 			all_rooms = Room.objects.all()
# 			all_rooms_list = [ar.id for ar in all_rooms ]
# 			logger.info("All rooms list {}".format(all_rooms_list))

# 			free_room_list = list(set(all_rooms_list) - set(booked_rooms_list))
# 			logger.info("Free rooms list {}".format(free_room_list))

# 			if free_room_list:
# 				free_room_data = Room.objects.filter(pk__in=free_room_list).values('id','name','description')
# 				logger.info("free_room_data {}".format(free_room_data))
# 				rooms_response = {'success': True,'Message':"Rooms are available","data":free_room_data}
# 				return Response(rooms_response, status=status.HTTP_200_OK)	

# 			else:
# 				rooms_response = {'success': True,'Message':"All rooms are booked at this time period."}
# 				return Response(rooms_response, status=status.HTTP_200_OK)		
		
# 		except Exception as e:
# 			logger.exception("Exception raised at free rooms list endpoint : {}".format(str(e)))
# 			rooms_response = {'success': False,'Message':"{} Exception raised, Please check the query param fields".format(str(e))}
# 			return Response(rooms_response, status=status.HTTP_406_NOT_ACCEPTABLE)