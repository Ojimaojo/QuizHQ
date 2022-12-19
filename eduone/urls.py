from django.urls import path
from . import views

urlpatterns = [
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('payment_err/',views.payment_err,name='payment_err'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('withdraw/',views.withdraw,name='withdraw'),
    path('withdraw_form/',views.withdraw_form, name='withdraw_form'),
    path('fund_form/',views.wallet_form, name='fund_form'),
    path('fund/',views.fund_wallet, name='fund'),
    path('confirm/', views.confirmTransaction, name='confirm' ),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('insufficent_balance/', views.low_bal, name='insufficent_balance'),
    path('leader_board/', views.top_winners, name='leader_board'),
    path('results/', views.score, name='results'),
    path('quiz/<id>/', views.quiz_detail, name='quiz'),
    path('freequiz_list/', views.free_quiz_list, name='freequiz_list'),
    path('quiz_list/', views.quiz_list, name='quiz_list'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('', views.index, name='home')

] 