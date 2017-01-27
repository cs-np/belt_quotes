from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import User, Quotes, fav_quotes
from django.contrib import messages
import bcrypt

# ==============================================================================
#                                   Render
# ==============================================================================

def delete(request):
    User.objects.all().delete()
    print 'Successfully delete'
    return redirect('/')
# ---------------------------
#       Index Route
# ---------------------------

def index(request):
    if 'user_id' in request.session:
        return redirect('/success')

    return render(request, 'quotes/index.html')

# ---------------------------
#       Register
# ---------------------------

def register(request):
    if 'user_id' in request.session:
        return redirect('/success')
    return render(request, 'quotes/register.html')

# ---------------------------
#       Login_Success
# ---------------------------

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id = request.session['user_id'])
    quotes = Quotes.objects.all()
    fav = fav_quotes.objects.filter(user__id = request.session['user_id'])
    uniquequoteid = []
    quotes_list = []
    if len(fav) == 1:
        if fav[0].quotes.id not in uniquequoteid:
            uniquequoteid.append(fav[0].quotes.id)
        for q in quotes:
            if q.id not in uniquequoteid:
                quotes_list.append(q)
    else:
        for i in fav:
            if i.quotes.id not in uniquequoteid:
                uniquequoteid.append(i.quotes.id)
        for q in quotes:
            if q.id not in uniquequoteid:
                quotes_list.append(q)
    print quotes_list
    context = {'user': user[0],'quotes':quotes_list, 'fav_quotes': fav}
    return render(request, 'quotes/success.html', context)

# ---------------------------
#           View User
# ---------------------------

def view_user(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id = user_id)
    if len(user) <= 0:
        return render(request, 'quotes/no_user.html')
    quotes = Quotes.objects.filter(user__id = user_id)

    context = {'user':user[0], 'total_quotes': len(quotes), 'quotes': quotes}

    return render(request, 'quotes/view_user.html', context)

# ==============================================================================
#                                   Process
# ==============================================================================

# ---------------------------
#       Registration
# ---------------------------

def registration(request):
    if 'user_id' in request.session:
        return redirect('/success')

    if request.method == 'POST':
        reg_data = User.objects.reg_validator(request.POST)
        if reg_data[0]:
            request.session['user_id'] = reg_data[1].id
            return redirect('/success')

        for error in reg_data[1]:
            messages.add_message(request, messages.INFO ,error)
    return redirect('/register')

# ---------------------------
#           Login
# ---------------------------

def login(request):
    if 'user_id' in request.session:
        return redirect('/success')

    if request.method == 'POST':
        login_data = User.objects.login_validate(request.POST)

        if login_data[0]:
            request.session['user_id'] = login_data[1].id
            return redirect('/success')

        for error in login_data[1]:
            messages.add_message(request, messages.INFO ,error)
    return redirect('/')

# ---------------------------
#           Logout
# ---------------------------

def logout(request):
    if 'user_id' in request.session:
        messages.add_message(request, messages.INFO ,"You're Successfully Logged Out")
    else:
        messages.add_message(request, messages.INFO ,"You're Already logged Out")
    request.session.flush()
    return redirect('/')

# ---------------------------
#           Add Quote
# ---------------------------
def add_quote(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        user_id = request.session['user_id']
        Q1 = Quotes.objects.add_quote(request.POST, user_id)
        for error in Q1[1]:
            messages.add_message(request, messages.INFO ,error)
    return redirect('/success')

# ---------------------------
#           Add Favorite
# ---------------------------

def add_fav(request, quote_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    fav = fav_quotes.objects.add_fav(user_id, quote_id)
    for error in fav[1]:
        messages.add_message(request, messages.INFO ,error)

    return redirect('/success')

# ---------------------------
#           Add Favorite
# ---------------------------

def rem_fav(request, quote_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    fav = fav_quotes.objects.rem_fav(user_id, quote_id)
    for error in fav[1]:
        messages.add_message(request, messages.INFO ,error)

    return redirect('/success')
