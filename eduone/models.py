from django.db import models
from django.contrib.auth.models import User
import math
from datetime import datetime

# Create your models here.
status_choice = (
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
        ('Processing', 'Processing'),
        ('Succesful', 'Succesful'),
    )

class Topic(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=225)
    completed = models.BooleanField(default=False)
    start = models.DateField()
    close = models.DateField()
    prize = models.CharField(max_length=220)
    fee = models.IntegerField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def close_submittion(self):
        if self.close < datetime.now():
            self.active = False

    @property
    def get_essay(self):
        return self.Essay__set.all()

class Essay(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=225)
    email = models.EmailField()
    Essay = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Winner(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING)
    winner = models.ForeignKey(Essay, on_delete=models.DO_NOTHING)
    position = models.IntegerField()
    comment = models.CharField(max_length=225)
    edition = models.CharField(max_length=225)

    def __str__(self):
        return self.winner.name

#quize section

class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=225)
    duration = models.IntegerField()
    prize = models.CharField(max_length=225)
    fee = models.IntegerField()
    active = models.BooleanField(default=False)

    def get_qestion_count(self):
        return self.Question__set.all().count()

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=225)

    @property
    def get_options(self):
        return self.options.all()
    
    @property
    def get_answer(self):
        return self.options.get(correct=True)

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=225)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    questions = models.IntegerField()
    passed = models.IntegerField()
    failed = models.IntegerField()
    time_in = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_percentage(self):
        return math.floor((self.passed / self.questions) * 100) 

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['passed']



class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=220, null=True, blank=True)

    @property
    def get_wallet(self):
        return self.Wallet__set.get(user=user)

    @property
    def quiz_history(self):
        return self.Score__set.get(user=user)

    def __str__(self):
        return self.user.username


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    amount = models.IntegerField()
    action = models.CharField(max_length=225)
    tx_ref = models.CharField(max_length=225)
    completed = models.BooleanField(default=False)
    trans_id = models.CharField(max_length=225,blank=True, null=True)
    time_in= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-time_in']

    def __str__(self):
        return self.user.username

class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    amount = models.IntegerField()
    action = models.CharField(max_length=225)
    account =models.IntegerField()
    account_name =models.CharField(max_length=225)
    bank =models.CharField(max_length=225)
    status = models.CharField(max_length=225, choices=status_choice,default='Pending',blank=True, null=True)
    time_in= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['-time_in']

class Message(models.Model):
    name = models.CharField(max_length=225)
    email = models.EmailField()
    phone = models.CharField(max_length=225)
    message = models.TextField()

    def __str__(self):
        return self.name