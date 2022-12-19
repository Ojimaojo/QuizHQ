from django.contrib import admin
from django.contrib.auth.models import User
from .models import Topic,Essay,Winner,Quiz,Message,Question,Option,Score,Wallet,Dashboard,Transaction,Withdraw
# Register your models here.

class OptionsInline(admin.StackedInline):
    model = Option
    

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [OptionsInline]

class DashboardInline(admin.StackedInline):
    model = Dashboard

class WalletInline(admin.StackedInline):
    model = Wallet
     

class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [DashboardInline,WalletInline]
  

admin.site.register(Quiz)
admin.site.register(Question,QuestionAdmin)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Score)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Withdraw)
admin.site.register(Message)
admin.site.register(Dashboard)