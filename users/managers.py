from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**kwargs):
        email = self.normalize_email(email)

        user = self.model(email=email,**kwargs)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self,email,password=None,**kwargs):
        email = self.normalize_email(email)

        user = self.model(email=email,is_staff = True,is_superuser=True,**kwargs)
        user.set_password(password)
        user.save()
        return user