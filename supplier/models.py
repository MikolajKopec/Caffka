from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinLengthValidator

class Supplier(models.Model):
    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(4)],
        null=False,
        blank=False
    )
    phone_regex = RegexValidator(
        regex = r'^[\d+]{4,15}$',
        message=_("Phone number must be entered in the format: '000000000000000'. Up to 15 digits alowed.")
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=False,
        null=False
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-name',)
    
    @property
    def custom_id(self):
        return f'{self.phone_number[1:3]}-{self.name[:2]}-{self.created_date.year}'

    def __str__(self) -> str:
        return self.custom_id