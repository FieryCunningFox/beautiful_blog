from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class loginView(APIView):
    
    def post(self, request):
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            
            if data.get('username') is None:
                response['message'] = 'key username not found'
                raise Exception('key username not found')
            
            if data.get('password') is None:
                response['message'] = 'key password not found'
                raise Exception('key password not found')
            
            check_user = User.objects.filter(username = data.get('username')).first()
            
            if check_user is None:
                response['message'] = 'invalid username, user not found'
                raise Exception('invalid username, user not found')
            
            user_obj = authenticate(username = data.get('username'), password = data.get('password'))
            
            if user_obj:
                response['status'] = 200
                response['message'] = 'Welcome!'
            else:
                response['message'] = 'invalid password'
                raise Exception('invalid password')
            
        except Exception as e:
            print(e)
        
        return Response(response)


class registerView(APIView):
    
    def post(self, request):
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            
            if data.get('username') is None:
                response['message'] = 'key username not found'
                raise Exception('key username not found')
            
            if data.get('password') is None:
                response['message'] = 'key password not found'
                raise Exception('key password not found')
            
            check_user = User.objects.filter(username = data.get('username')).first()
            
            if check_user:
                response['message'] = 'username is already taken'
                raise Exception('username is already taken')
            
            user_obj = User.objects.create(username = data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.save()
            response['message'] = 'User created'
            response['status'] = 200
            
            
        except Exception as e:
            print(e)
        
        return Response(response)