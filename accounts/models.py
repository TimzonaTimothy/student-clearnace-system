import imp
from django.db import models
from django.utils import timezone
import secrets
from main.models import *
from .paystack import PayStackPayment
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser

class MyAccountManager(BaseUserManager):
    def create_user(self,email, first_name,last_name,username,password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have username')

        user = self.model(
            email = self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name,email,last_name,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name = last_name,
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    Gender = (
        ('Male','Male'),
        ('Female','Female'),
    )

    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    username     = models.CharField(max_length=100, unique=True)
    email         = models.EmailField(max_length=100, unique=True)
    matric_number = models.CharField(max_length=100, unique=True, null=True)
    total_cleared = models.FloatField(blank=True, null=True, default=00.00)
    outstanding = models.FloatField(blank=True, null=True, default=00.00)
    phone = models.CharField(blank=True, max_length=100) 
    gender = models.CharField(blank=True, max_length=100, choices=Gender)
    date_of_birth = models.CharField(blank=True, max_length=10)  
    profile_picture = models.ImageField(blank=True, upload_to='userprofile/%Y%m%d/')
    city = models.CharField(blank=True, max_length=100) 
    state = models.CharField(blank=True, max_length=100) 
    country = models.CharField(blank=True, max_length=100)
    department = models.ForeignKey(Department,on_delete=models.CASCADE, null=True, blank=True)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey(Session,on_delete=models.CASCADE, null=True, blank=True)
    year1_fee = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    year2_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year3_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year4_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year5_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)

    date_joined   = models.DateTimeField(auto_now_add=True) 
    last_login    = models.DateTimeField(auto_now_add=True)   
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=False)
    is_support = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name', ]

    objects = MyAccountManager()


    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    

    
class SchoolFees(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    amount = models.CharField(max_length=250, null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.amount)
    
    class Meta:
        ordering = ('-date',)
        verbose_name = 'School Fee'
        verbose_name_plural = 'School Fees'


class Paystack(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    service = models.CharField(max_length=1000000)
    amount = models.CharField(max_length=1000000)
    email =  models.EmailField(max_length=3000, blank=True, null=True)
    reference = models.CharField(max_length=200)
    generated = models.DateTimeField(default=timezone.now)
    verified =  models.BooleanField(default=False)

    class Meta:
        ordering = ('-generated',)

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        while not self.reference:
            ref = secrets.token_urlsafe(50)
            same_ref = Paystack.objects.filter(reference = ref)
            if not same_ref:
                self.reference = ref
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return int(self.amount)*100

    def verify_payment(self):
        paystack = PayStackPayment()
        status, result = paystack.verify_payment(self.reference, self.amount)
        if status:
            if result['amount']/100 == int(self.amount):
                self.verified = True
            self.save()
        return False

class Userhistory(models.Model):
    Status = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    )
    # paystack = models.OneToOneField(Paystack, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    email  = models.EmailField(max_length=40, blank=True, null=True)
    ref = models.CharField(max_length=30, blank=True, null=True)
    amount = models.CharField(max_length=30, blank=True, null=True)
    transaction = models.CharField(max_length=20,blank=True, null=True,default='Unpaid', choices=Status)
    confirm =  models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-date_created',)
        verbose_name = 'User Payment History'
        verbose_name_plural = 'User Payment Histories'


    def __str__(self):
        return f"{self.transaction}: {self.amount}"