from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    CUSTOMER = 1
    VENDOR = 2
    ADMIN = 3
    ROLE_CHOICES = (
        (CUSTOMER, 'customer'),
        (VENDOR, 'vendor'),
        (ADMIN, 'admin'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


def default_security_question():
    response = SecurityQuestion.objects.get_or_create(question='What is the name of your favorite song?')
    return SecurityQuestion.objects.order_by('id').first()


class SecurityQuestion(models.Model):
    question = models.CharField(max_length=255, blank=False, null=False, unique=True)

    def __str__(self):
        return self.question


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    roles = models.ManyToManyField(Role)
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save()
        
class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, 
                                primary_key=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=255, default='')
    address = models.CharField(max_length=100, default='')
    telephone = models.CharField(max_length=100, default='')
    zip_code = models.CharField(max_length=20, default='')
    state = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')
    security_question = models.ForeignKey(SecurityQuestion, on_delete=models.SET_DEFAULT,
                                          default=default_security_question)
    security_question_answer = models.CharField(max_length=100, blank=False, null=True )

    def __str__(self):
        return self.user.username

    def check_security_question_answer(self, raw_answer):
        if self.security_question_answer == raw_answer:
            return True
        else:
            return False

    def check_security_question(self, raw_question):
        if self.security_question == raw_question:
            return True
        else:
            return False
    def save(self, *args, **kwargs):
        super().save()
        