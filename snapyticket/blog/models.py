from django.db import models

# Create your models here.

POST_TAG=(
        ('Tr','Trends And Release'),
        ('Pr','Press Release'),
        ('Sr','Security Release'),
    )

# Manager for all Trend and Insights Post
class TrendPostManager(models.Manager):
    def get_queryset(self):
        return super(TrendPostManager,self).get_queryset(tag='Tr')
  
# manager for all Press related Post  
class PressReleasePostManager(models.Manager):
    def get_queryset(self):
        return super(PressReleasePostManager,self).get_queryset(tag='Pr')

# manager for all security related Post
class SecurityPostManager(models.Manager):
    def get_queryset(self):
        return super(SecurityPostManager,self).get_queryset(tag='Sr')
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to='blog_post')
    body = models.TextField()
    tag  = models.CharField(choices=POST_TAG,max_length=50,)
    
    
    # Hooking models to managers
    objects  = models.Manager()
    security = SecurityPostManager()
    trend    = TrendPostManager()
    press    = PressReleasePostManager()
    
    def __str__(self):
        return self.title
    
    # returns the tag of the post
    @property
    def get_post_tag(self):
        return self.tag
    
    