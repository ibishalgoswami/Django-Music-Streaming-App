from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class LoginLogoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    login_time = models.DateTimeField(auto_now_add=True)
    # logout_time = models.DateTimeField()

    # logout_time = models.DateTimeField(auto_now=False, blank=True, null=True)
    # browser_name = models.CharField(max_length=255, blank=True, null=True)
    # os_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'log_login_logout'