from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
NAME_REGEX = re.compile(r'/^[a-zA-Z]+', re.MULTILINE)
# PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$', re.MULTILINE)

# ==============================================================================
#                                   USER MANAGER
# ==============================================================================

class UserManager(models.Manager):

# ---------------------------
#    Registration Validator
# ---------------------------

    def reg_validator(self,POST):
        valid = True
        error_list = []
        first_name = POST['first_name'].lower()
        last_name = POST['last_name'].lower()
        email = POST['email'].lower()
        dob = POST['dob']
        password = POST['password'].encode()
        passconf = POST['passconf']
        email_check = User.objects.filter(email=POST['email'])
        if email_check:
            error_list.append('Invalid Email')
            return False, error_list

# Checking FIRST NAME
        if len(first_name) < 2:
            error_list.append('First Name cannot be less than 2 Characters')
            valid = False
        if not first_name.isalpha():
            error_list.append('First Name cannot contain Numbers or Blank Spaces')
            valid = False

# Checking LAST NAME
        if len(last_name) < 2:
            error_list.append('Last Name cannot be less than 2 Characters')
            valid = False
        if not  last_name.isalpha():
            error_list.append('Last Name cannot contain Numbers or Blank Spaces')
            valid = False

# Checking EMAIL
        if len(email) < 5:
            error_list.append('Email Too Short')
            valid = False
        if not EMAIL_REGEX.match(email):
            error_list.append('Invalid Email')
            valid = False

# Checking PASSWORD
        # if len(password) < 8:
        #     error_list.append('Password cannot be less than 8 Characters')
        #     valid = False
        # if not PASSWORD_REGEX.match(password):
        #     error_list.append('Password Requires atleast One Uppercase, One Lowercase, One Number and One Symbol')
        #     valid = False
        if password != passconf:
            error_list.append("Passwords Doesn't Match")
            valid = False

# If any Input Contraint Fails VALID is False
        if not valid:
            return False, error_list

# Creating New User Once all Input Contraint passed and return User object
        password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        User.objects.create(first_name=first_name,last_name=last_name,email=email,dob =dob,password=password_hashed)
        user = User.objects.filter(email = email)
        return True, user[0]

# ---------------------------
#       Login Validator
# ---------------------------

    def login_validate(self, POST):
        error_list = []
        email = POST['email'].lower()
        password = POST['password']
        user_pass = User.objects.filter(email=email)

# Checking if User Exist
        if not user_pass:
            error_list.append("Invalid Email or Password")
            return False, error_list

# Checking Password; if True Return With User Object
        confpass = user_pass[0].password
        if bcrypt.hashpw(password.encode(), confpass.encode()) == confpass:
            user = User.objects.filter(email = email)
            return True, user[0]
        else:
            error_list.append('Invalid Email or Password')
            return False, error_list
        return None

# ==============================================================================
#                                   Quote MANAGER
# ==============================================================================

class QuoteManager(models.Manager):
    def add_quote(self, POST, user_id):
        error_list = []
        quoteby = POST['quotedby'].lower()
        quote = POST['quote'].lower()
        U1 = User.objects.filter(id = user_id)
        valid = True
        if len(quoteby) < 3:
            error_list.append("Quoted By must by more than 3 Characters")
            valid = False
        if len(quote) < 10:
            error_list.append("Quote Message must 10 or more Characters")
            valid = False
        if not valid:
            return False, error_list
        Quotes.objects.create(quote = quote,quotedby = quoteby, user = U1[0])
        error_list.append("Quote Added Successfully")
        return True, error_list

# ==============================================================================
#                                   Favorite MANAGER
# ==============================================================================
#
class FavManager(models.Manager):
    def add_fav(self, user_id, quote_id):
        error_list = []
        valid = True
        U1 = User.objects.filter(id = user_id)
        Q1 = Quotes.objects.filter(id = quote_id)
        print 'here'
        if len(U1) < 1:
            print 'got it'
            error_list.append('Tried User Sniffing')
            valid = False
        if len(Q1) < 1:
            error_list.append('Tried Quote Sniffing')
            valid = False
        if not valid:
            return False, error_list
        print 'here at'
        print user_id
        F1 = fav_quotes.objects.filter(user__id = user_id, quotes__id = quote_id)
        print F1
        if len(F1) < 1:
            print 'here at'
            F1 = fav_quotes.objects.create(quotes = Q1[0], user = U1[0])
            error_list.append('Successfully Added to your List')
        else:
            error_list.append('Already added to your list')
        return True, error_list

    def rem_fav(self, user_id, quote_id):
        error_list = []
        U1 = User.objects.filter(id = user_id)
        Q1 = Quotes.objects.filter(id = quote_id)
        F1 = fav_quotes.objects.filter(user__id = user_id).filter(quotes__id = quote_id).delete()

        error_list.append('Successfully Removed to your List')

        return True, error_list


# ==============================================================================
#                                USER CLASS
# ==============================================================================


class User(models.Model):
    first_name = models.CharField(max_length=45, default = "Not Available")
    last_name = models.CharField(max_length=45, default = "Not Available")
    email =  models.CharField(max_length=45)
    password = models.TextField(default = "Not Available")
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Quotes(models.Model):
    quotedby = models.CharField(max_length=45, default = "Not Available")
    quote = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()

class fav_quotes(models.Model):

    quotes = models.ForeignKey(Quotes, default="1")
    user = models.ForeignKey(User, default='1')
    objects = FavManager()
