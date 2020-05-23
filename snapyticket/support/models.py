from django.db import models

# Create your models here.
ROLES = (
    
    ('FE','FrontEnd Developer'),
    ('BE','BackEnd Developer'),
    ('FS','FullStack Developer'),
)



class TermsAndCondition(models.Model):
    title = models.CharField(max_length=100)
    body  = models.TextField()
    
    def __str__(self):
        return self.title





class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=100)
    body  = models.TextField()
    
    def __str__(self):
        return self.title
    
    
 
 
    
class OurTeam(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    role       = models.CharField(choices=ROLES,max_length=100)
    image      = models.ImageField(upload_to='our_team')
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.role}' 
    
    
    
 
    
class SocialProfile(models.Model):
    tean_member     = models.ForeignKey(OurTeam,on_delete=models.CASCADE)
    social_platform = models.CharField(max_length=100)
    profile_url     = models.URLField()
    
    
