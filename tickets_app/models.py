from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField


class EventHost(AbstractUser):
    vk_id = models.URLField(blank=True)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=False, unique=True)

    REQUIRED_FIELDS = ['email', 'password', 'phone']

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)


class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', primary_key=True)
    description = models.TextField()
    date = models.DateTimeField()
    event_host = models.ForeignKey(EventHost, related_name='Events', on_delete=models.CASCADE)

    def __str__(self):
        return '{event_name}, создано {event_host}'.format(event_name=self.name, event_host=self.event_host)


class Wallet(models.Model):
    TYPE = [
        ('CRD', 'Credit Card'),
        ('WLT', 'Online Wallet'),
        ('CHK', 'Checking Account')
    ]

    wallet_id = models.CharField(max_length=250)
    event_host = models.OneToOneField(EventHost, on_delete=models.CASCADE, unique=True, related_name='wallets')
    wallet_type = models.CharField(max_length=3, choices=TYPE, default='CRD')

    def __str__(self):
        return '{wallet_id} пользователя {name}'.format(wallet_id=self.wallet_id, name=self.event_host)


class Ticket(models.Model):
    TICKET_TYPE = [
        ('VIPP', 'Vip plus'),
        ('VIP', 'Vip ticket'),
        ('PLUS', 'Plus ticket'),
        ('COMF', 'Comfort ticket'),
        ('STND', 'Standard ticket')
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    event_host = models.ForeignKey(EventHost, on_delete=models.CASCADE, related_name='tickets_host')
    ticket_count = models.PositiveIntegerField()
    ticket_type = models.CharField(max_length=4, choices=TICKET_TYPE, default='STND')

    def __str__(self):
        return '{ticket_type} билет на {event}, кол-во {count}'.format(ticket_type=self.ticket_type,
                                                                       event=self.event,
                                                                       count=self.ticket_count)


class Cart(models.Model):
    PAYMENT_STATUS = [
        ('NPD', 'Not paid'),
        ('SPD', 'Successful paid'),
    ]

    user = models.ForeignKey(EventHost, on_delete=models.CASCADE, related_name='cart')
    status = models.CharField(max_length=4, choices=PAYMENT_STATUS, default='NPD')

    def __str__(self):
        return 'Корзина пользователя {user}'.format(user=self.user)


class CartItem(models.Model):
    PAYMENT_STATUS = [
        ('NPD', 'Not paid'),
        ('SPD', 'Successful paid'),
    ]

    user = models.ForeignKey(EventHost, on_delete=models.CASCADE, related_name='cart_items', blank=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='cart_items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items', blank=True)
    ticket_count = models.PositiveIntegerField()
    previous_count = models.PositiveIntegerField(blank=True, default=0)

    def clean(self):
        if self.ticket_count > self.ticket.ticket_count:
            raise ValidationError('Вы покупаете больше, чем можно')

    def save(self, *args, **kwargs):
        if self.ticket_count > self.previous_count:
            self.ticket.ticket_count -= self.ticket_count - self.previous_count
        else:
            self.ticket.ticket_count += self.previous_count - self.ticket_count
        self.previous_count = self.ticket_count
        self.ticket.save()
        super(CartItem, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.ticket.ticket_count += self.ticket_count
        self.ticket.save()
        super(CartItem, self).delete(*args, **kwargs)

    def __str__(self):
        return 'Билет на {event}, пользователя {user} в кол-ве {ticket_count} шт.'.format(event=self.ticket.event,
                                                                                   user=self.user,
                                                                                   ticket_count=self.ticket_count)
