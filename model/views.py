from django.shortcuts import render,redirect
from .models import PredictionRecord
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from keras.models import load_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django.template import TemplateDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.conf import settings
#from io import BytesIO
from keras.preprocessing import image
import numpy as np
from django.db import IntegrityError

#import io
#import re
import os
# Create your views here.
def main(request):
        return render(request,'main.html')

@login_required(login_url='main')
def main1(request):
        return render(request,'main1.html')

def register(request):
        if request.method=="POST":
            uname=request.POST.get('username')
            #contact=request.POST.get('contact')
            email=request.POST.get('email')
            #gender=request.POST.get('gender')
            pass1=request.POST.get('password1')
            pass2=request.POST.get('password2')

            if pass1!=pass2:
               return HttpResponse("Your password and confirm password are not same!!!")
            else:
               try:
                my_user=User.objects.create_user(uname,email,pass1)
                my_user.save()
                return redirect('login')
               except IntegrityError:
                return HttpResponse("Username already exists. Please choose a different one.")
        return render(request,'register.html')

def login(request):
        if request.method=='POST':
            username=request.POST.get('username')
            pass1=request.POST.get('pass')
            user=authenticate(request,username=username,password=pass1)
            if user is not None:
               auth_login(request,user)
               return redirect('main1')
            else:
                 return HttpResponse('Username or Password is incorrect!!!!!')  
        return render(request,'login.html')
def logoutp(request):
     logout(request)
     return redirect('main')


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'best_model_c1.keras')#'my_model.h5')
loaded_model = load_model(MODEL_PATH)

def index(request):
    return render(request, 'index.html')
def classify_skin_lesion(image):
    return True
def predict(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = int(request.POST['age'])
        gender = request.POST['gender']
        localization = request.POST['localization']

        img = request.FILES['image']
        fs = FileSystemStorage()
        uploaded_image = fs.save(img.name, img)
        uploaded_image_path = fs.url(uploaded_image)
        pil_img = Image.open(img)
        pil_img=pil_img.convert('RGB')
        pil_img = pil_img.resize((28,28))  # Resize the image
        
        # Convert the PIL Image to a numpy array
        img_array = np.array(pil_img)
        img_array = img_array / 255.0  # Normalize the image
        
        if img_array.shape[2] == 4:
            # If the image has 4 channels (RGBA), convert it to 3 channels (RGB)
            img_array = img_array[:, :, :3]
        img_array = np.expand_dims(img_array, axis=0)
        is_lesion=classify_skin_lesion(img_array)
        # Make prediction
        if is_lesion:           
            class_names = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

            predictions = loaded_model.predict(img_array)
            predicted_class = np.argmax(predictions)

            prediction_record = PredictionRecord(
                user=request.user,
                name=name,
                age=age,
                gender=gender,
                localization=localization,
                prediction=class_names[predicted_class],  # Use 'prediction' instead of 'prediction_result'
                #image=uploaded_image_path  # Use 'image' field and provide the uploaded image path
            )      

            prediction_record.save()

        # Map predicted class index to labels
    
            predicted_class_name = class_names[predicted_class]

        # Render the corresponding HTML file
        if predicted_class_name:
            try:
                context = {
                'image_url': os.path.join(settings.MEDIA_URL, uploaded_image_path)
            }
                html_template = f"{predicted_class_name}.html"
                return render(request, html_template,context)
        
            except TemplateDoesNotExist:
                return HttpResponse("Class information not available.")
    else:
        return HttpResponse('This image does not appear to be a skin lesion')
    return HttpResponse("Invalid Request")


def user_records(request):
    user_records = PredictionRecord.objects.filter(user=request.user)
    context = {'user_records': user_records}
    return render(request, 'user_records.html', context)
