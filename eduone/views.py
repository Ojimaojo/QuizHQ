import environ
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from .models import Topic,Essay,Winner,Message,Quiz,Question,Option,Score,Wallet,Dashboard,Transaction,Withdraw
import random
import string
import requests
from django.contrib.auth.decorators import login_required
env = environ.Env()



# Create your views here.
def index(request):
    context = {} 
    return render(request, 'index.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        new_message = Message(name=name,email=email,phone=phone,message=message)
        new_message.save()
    return render(request, 'contact.html')

def about(request):

    return render(request, 'about.html')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        print(request)
        new_user = User.objects.create_user(username,email,password,first_name=first_name,last_name=last_name)
        if new_user:
            dashboard = Dashboard.objects.get(user=new_user)
            dashboard.phone = phone
            dashboard.save()
            return redirect('/accounts/login/')
    else:
        context= {}
    return render(request, 'signup.html', context)


def dashboard(request):
    dashboard = Dashboard.objects.get(user=request.user)
    scores = Score.objects.filter(user=request.user)
    wallet = Wallet.objects.get(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)[:6]
    withdrawals = Withdraw.objects.filter(user=request.user)[:6]
    context = {
        'dashboard':dashboard,
        'scores':scores,
        'wallet':wallet,
        'transactions':transactions,
        'withdrawals':withdrawals
    }
    return render(request, 'dashboard.html', context)

def low_bal(request):
    context={}
    return render(request,'low_bal.html', context)

#quiz
def top_winners(request):
    results = Score.objects.order_by('-passed')[:10]
    context = {'results':results}
    return render(request, 'top_rank.html', context)


def free_quiz_list(request):
    pquiz = Quiz.objects.filter(fee=0)
    free = True
    context = {
        'free':free,
        'pquiz':pquiz
    }
    return render(request, 'quiz_list.html', context)

def quiz_list(request):
    
    pquiz = Quiz.objects.filter(fee__gte=0)

    context = {
        'pquiz':pquiz
    }
    return render(request, 'quiz_list.html', context)

@login_required(login_url='/accounts/login/')
def quiz_detail(request, id):
    quiz = Quiz.objects.get(id=id)
    qset = Question.objects.filter(quiz=quiz)
    shuffled = qset.order_by('?')
    questions = shuffled[:20]
    wallet = Wallet.objects.get(user=request.user)
    if wallet.balance < quiz.fee:
        return redirect('/insufficent_balance/')
    else:
        wallet.balance -= quiz.fee
        wallet.save()
        new_trans = Transaction(user=request.user,amount=quiz.fee, action='debit',tx_ref='payment for quiz',completed=True,trans_id=f'quiz{quiz.id}')
        new_trans.save()
        if request.method == "POST":
            correct = 0
            failed = 0
            number_of_q = 0
            for q in questions:
                number_of_q +=1 
                user_answer = str(request.POST.get(q.text))
                answer = str(q.get_answer)
                if user_answer == answer:
                    correct +=1
                else: 
                    failed +=1
            if number_of_q == correct:
                wallet.balance += int(quiz.prize)
                wallet.save()
                another_trans = Transaction(user=request.user,amount=quiz.prize, action='credit',tx_ref=f'You Won quiz {quiz.id}',completed=True,trans_id=f'quiz{quiz.id}')
                another_trans.save()
                quiz.active = False
                quiz.save()
            score = Score.objects.filter(Q(user=request.user) & Q(quiz=quiz)).get_or_create(user=request.user, 
            quiz=quiz, questions=number_of_q, passed=correct,failed=failed)
            
            context = {score:score}
            return redirect('/results/')
        else:
            context = {
                'quiz':quiz,
                'questions':questions
            }
        return render(request, 'quiz_detail.html', context)

def score(request):
    scores = Score.objects.filter(user=request.user)
    context = {'scores':scores}
    return render(request, 'scores.html', context)

#Essay
def essay_list(request):
    context = {}
    pass


#wallet
#fund wallet
@login_required(login_url='/accounts/login/')
def wallet_form(request):
    return render(request,'fund_wallet.html')


@login_required(login_url='/accounts/login/')
def fund_wallet(request):
    wallet = Wallet.objects.get(user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        print(amount)
        currency = request.POST.get('currency')
        user = request.user
        tx_ref = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10)) + user.username
        type_of_tans='fund wallet'
        #save transaction in database
        new_transaction = Transaction(user=user,amount=amount,action=type_of_tans,tx_ref=tx_ref,completed=False)
        headers = { 'Authorization': "Bearer "+env('FLWSECK')} #add secret key
        data = {
            'tx_ref': tx_ref,
            'amount': amount, 
            'currency':'NGN',
            'redirect_url': "http://localhost:8000/confirm",#create a redirect url
            'customer': {
                'email': user.email,
                'name': user.username
            },
        }
        url = "https://api.flutterwave.com/v3/payments"
        try:
            r = requests.post(url,json=data,headers=headers)
            if r.ok:
                new_transaction.save()
                res=r.json()
                link = res['data']['link']
                return redirect(link)
            else:
                return redirect('/payment_err/')
        except ConnectionError:
            return redirect('/payment_err/')

@login_required   
def payment_err(request):
    return render(request,'payment_err.html')

@login_required
def confirmTransaction(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    trans_id=request.GET.get('trans_id', None)
    transaction = Transaction.objects.get(tx_ref=tx_ref)
    if status == "successful":
        if transaction:
            user = transaction.user
            amount = transaction.amount
            transaction.trans_id = trans_id
            transaction.completed = True
            transaction.save()
            wallet=Wallet.objects.get(user=user)
            wallet.balance += int(amount)
            wallet.save()
            return redirect('/dashboard/')
    else:
        return redirect('/payment_err/')
    


#withdraw from wallet
@login_required(login_url='/accounts/login/')
def withdraw_form(request):
    return render(request,'withdraw_wallet.html')

@login_required(login_url='/accounts/login/')
def withdraw(request):
    wallet = Wallet.objects.get(user=request.user)
    if request.method == 'POST':
        user = request.user
        action ='Withdraw'
        amount = request.POST.get('amount')
        account = request.POST.get('account')
        account_name = request.POST.get('account_name')
        bank = request.POST.get('bank')
        if int(amount)>=1000:
            wallet.balance-=int(amount)
            wallet.save()
            new_withdrawal = Withdraw(user=user,amount=amount,action=action,account=account,account_name=account_name,bank=bank)
            new_withdrawal.save()
            return redirect('/dashboard/')
        else:
            return redirect('/dashboard/')
