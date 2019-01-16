from django.db import models  

class Blogposts(models.Model):
    title=models.CharField(max_length=264)
    author=models.CharField(max_length=264)
    posttime=models.DateField()
    thumbnail=models.ImageField(upload_to='media/images')
    content=models.TextField()
    objects=models.Manager()
    
    def __str__(self):
        return self.title
  