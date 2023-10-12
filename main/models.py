from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'
    
class Session(models.Model):
    session = models.CharField(max_length=100)

    def __str__(self):
        return self.session
    
    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'