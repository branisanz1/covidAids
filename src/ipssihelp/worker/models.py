from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=_('Email'),
        unique=True,
    )
    gender = models.CharField(
        max_length=1,
        choices=(
            ('m', _('Man')),
            ('w', _('Women')),
            ('o', _('Other')),
        ),
        blank=True,
        null=True
    )

    username = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique= False,
    )

    phone = models.CharField(
        max_length=16,
        blank=True,
        null=True,
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Birth date')
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'user'
        unique_together = ('email', 'phone')
        indexes = [
            models.Index(fields=[
                'email',
                'phone',
            ]),
        ]

    def __str__(self):
        return '{}. {}'.format(
            self.first_name[0],
            self.last_name
        )


class Address(models.Model):
    user = models.OneToOneField(
        'User',
        null=True,
        on_delete=models.PROTECT,
    )
    address1 = models.CharField(
        max_length=255,
        blank=False
    )
    address2 = models.CharField(
        max_length=255,
        blank=True
    )
    postal_code = models.CharField(
        max_length=255,
        blank=False
    )
    city = models.CharField(
        max_length=255,
        blank=False
    )
    country = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        default='FR',
        verbose_name=_('Country'),
        help_text='ISO Alpha-2'
    )
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name=_('Latitude')
    )
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name=_('Latitude')
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created')
    )

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        indexes = [
            models.Index(fields=['address1', 'postal_code']),
        ]
        db_table = 'address'

    def __str__(self):
        return '{}. {} - {}'.format(
            self.address1,
            self.city,
            self.country
        )


class Ad(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    title = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        verbose_name=_('Title')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Description')
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        blank=True,
        verbose_name=_('Category')
    )
    type = models.CharField(
        max_length=32,
        choices=(
            ('supply', _('Supply')),
            ('demand', _('Demand')),
        ),
        default='supply',
        verbose_name=_('Type')
    )
    status = models.CharField(
        max_length=32,
        choices=(
            ('waiting', _('Waiting')),
            ('online', _('Online')),
            ('cancelled', _('Cancelled')),
        ),
        default='waiting'
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created')
    )

    class Meta:
        verbose_name = _('AD')
        verbose_name_plural = _('Ads')
        db_table = 'ad'
        indexes = [
            models.Index(fields=[
                'title',
                'status',
            ]),
        ]

    def __str__(self):
        return '{} ({})'.format(
            self.title,
            self.pk
        )


class Mission(models.Model):
    customer = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name=_('User')
    )
    ad = models.ForeignKey(
        'Ad',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name=_('Ad')
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created')
    )

    class Meta:
        verbose_name = _('Mission')
        verbose_name_plural = _('Missions')
        db_table = 'mission'

    def __str__(self):
        return '{} - {}'.format(
            self.ad,
            self.customer
        )


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('title')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('description')
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        db_table = 'category'
        indexes = [
            models.Index(fields=[
                'name',
            ]),
        ]

    def __str__(self):
        return str(self.name)


class Conversation(models.Model):
    ad = models.ForeignKey(
        'Ad',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created')
    )

    class Meta:
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversations')
        db_table = 'conversation'

    def __str__(self):
        return '{} - {}'.format(
            self.pk,
            self.ad
        )


class Message(models.Model):
    sender = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name=_('User'),
    )
    conversation = models.ForeignKey(
        'Conversation',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name=_('Conversation')
    )
    content = models.TextField(
        null=False,
        blank=False,
        verbose_name=_('Content')
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created')
    )

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        db_table = 'message'

    def __str__(self):
        return 'Message - {}'.format(
            self.conversation
        )
