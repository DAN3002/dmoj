from django.contrib.auth import login
import requests
from django.contrib.auth.models import User
from django.shortcuts import redirect
import json
from django.http import Http404, JsonResponse
from judge.models.profile import Profile
from django.conf import settings


def login_with_accesstoken(request):
    FAILED_TO_LOGIN_WITH_ACCESS_TOKEN = "FAILED_TO_LOGIN_WITH_ACCESS_TOKEN"

    if request.method != "POST": 
        raise Http404 
    
    req_body = json.loads(request.body)

    accesstoken = req_body.get("accesstoken") 
    full_path = req_body.get("full_path")

    if accesstoken is None: 
        print(FAILED_TO_LOGIN_WITH_ACCESS_TOKEN, ": missing accesstoken")
        return JsonResponse({
            "status": 400, 
            "message": "Missing Credentials"
        },safe=False)
    
    if full_path is None: 
        print(FAILED_TO_LOGIN_WITH_ACCESS_TOKEN, ": missing full_path")
        return JsonResponse({
            "status": 400, 
            "message": "Missing full_path"
        },safe=False)

    try:
        res = requests.post(settings.LMS_AUTHENTICATION_URL, headers={"Content-Type": "application/json"}, json={
            "token": accesstoken
        }, timeout=5)
    except: 
        print(FAILED_TO_LOGIN_WITH_ACCESS_TOKEN, ": Failed to fetch user info by access token probably due to LMS server.")
        return JsonResponse({
            "status": 500, 
            "message": "Internal Server Error"
        },safe=False)


    if res.status_code == 500:
        print(FAILED_TO_LOGIN_WITH_ACCESS_TOKEN, ": Failed to fetch user info by access token due to LMS server.")
        return JsonResponse({
            "status": 500, 
            "message": "Internal Server Error"
        },safe=False)
    
    if res.status_code != 200:
        print(FAILED_TO_LOGIN_WITH_ACCESS_TOKEN, ": wrong access token.")
        return JsonResponse({
            "status": 403, 
            "message": "Wrong Credentials"
        },safe=False)

    data = res.json()

    username = data.get("username")
    name = data.get("name")
    email = data.get("email")

    if username is None or name is None or email is None: 
        return JsonResponse({
            "status": 500, 
            "message": "Internal Server Error"
        },safe=False)

    user = User.objects.filter(username=username, email=email).first()

    if user is None: 
        user = User.objects.create_user(username=username, email=email, last_name=name, password="funix.edu.vn")
        user.is_active = True
        user.save()

        Profile.objects.create(user=user)

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")

    return redirect(full_path)
        
