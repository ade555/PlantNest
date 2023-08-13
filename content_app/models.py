from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Feedback"
        verbose_name_plural = "User Feedback"
    
    def __str__(self):
        return self.name
