from django.db import models
from django.contrib.auth.models import User

class PredictionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255,default='Unknown')
    prediction = models.CharField(max_length=100)
    age=models.IntegerField(default=0)
    gender=models.CharField(max_length=10,default='Unknown')
    localization=models.CharField(max_length=50,default='Unknown')
    #image = models.ImageField(upload_to='prediction_images/')

    def __str__(self):
        return f"{self.name} - {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']

