from django.db import models
import string
import random

# Create your models here.
class  Url(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_url} | {self.created_at}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.short_code = self.generate_short_code()
        return super().save(*args, **kwargs)
    
    def generate_short_code(self):
        characters = string.ascii_letters + string.digits
        short_code = ''.join(random.choice(characters) for _ in range(6))
        return short_code
    
    class Meta:
        db_table = "url_list"