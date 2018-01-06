from __future__ import unicode_literals
import bcrypt
from datetime import datetime
from django.db import models
import re
name_regex = re.compile(r'^[a-zA-Z ]{3,}$')

class UserManager(models.Manager):
    def regis_validator(self, post):
        name = post['name']
        username = post['username']
        password = post['password']
        cpassword = post['cpassword']
        date_hired = post['date_hired']

        errors=[]

        if len(name)<3 or len(username)<3:
            errors.append("Name and Username: at least 3 characters")
        else:
            if not name_regex.match(name):
                errors.append("incorrect name format")
            else:
                if len(User.objects.filter(username=username)) > 0:
                    errors.append('Username is already used')

        if len(password) < 8 or len(cpassword)<8:
            errors.append('Password and Confirm Password: at least 8 characters')
        elif password != cpassword:
            errors.append('Password is not match with Comfirm Password, please try again')

        if len(date_hired) < 1 :
            errors.append("Date Hired can not be empty")
        else:
            date_object = datetime.strptime(date_hired, '%Y-%m-%d')
            if date_object > datetime.now():
                errors.append("Date Hired should not be future date")
        
        if not errors:
            hashed = bcrypt.hashpw((password.encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=name,
                username=username,
                password=hashed,
                date_hired=date_hired,
            )
            return new_user                

        return errors

    def login_validator(self, post):
        username = post['username']
        password = post['password']

        try:
            user = User.objects.get(username=username)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return user
        except:
            pass

        return False

    def item_validator(self, post):
        item = post['item']
        errors=[]
        if len(item)<3:
            errors.append("Item should be more than 3 characters")
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    date_hired = models.DateField(null=True, blank=True)

    objects = UserManager()

class Wish(models.Model):
    item = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    creator = models.ForeignKey(User,related_name='createwish')
    follower = models.ManyToManyField(User, related_name="addwish")