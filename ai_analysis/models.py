from django.db import models

class Ai_analysis_log(models.Model):
    image_path = models.CharField(max_length=255)
    success = models.BooleanField()
    message = models.CharField(max_length=255)
    cls = models.IntegerField(null=True,blank=True)
    confidence = models.DecimalField(max_digits=5, decimal_places=4,null=True,blank=True )
    request_timestamp = models.DateTimeField(null=True,blank=True)
    response_timestamp = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.image_path 
    