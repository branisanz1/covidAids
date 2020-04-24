from django.contrib import admin
from django.contrib.admin import StackedInline
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import Ad, User, Category, Address, Mission, Conversation,Message
from dateutil.relativedelta import relativedelta
import datetime


class AdInline(StackedInline):
    model = Ad
    verbose_name_plural = _('Ads')
    show_change_link = True
    extra = 0


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', '_name', '_age','_fullAddress', 'phone', 'updated', 'created')
    readonly_fields = ('created', 'updated')
    search_fields = ('email',)
    list_display_links = ['email',]
    ordering = ('created',)
    inlines = [
        AdInline
    ]

    def _name(self,obj):
        output = "{}. {}".format(
            obj.first_name[0],
            obj.last_name
        )

        return output

    def _age(self,obj):
        dateNow = datetime.datetime.now()
        dateBirthday = obj.birth_date
        delta = relativedelta(dateNow, dateBirthday)
        return delta.years


    def _fullAddress(self,obj):
        output = "{}, {}, {}".format(
            obj.address.address1,
            obj.address.address2,
            obj.address.postal_code

        )

        return output



@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'type', 'status', 'updated', 'created')
    readonly_fields = ('created', 'updated')
    list_filter = ('user', 'category', 'type', 'status')
    search_fields = ('title', 'description')
    list_display_links = ['user', 'title']
    ordering = ('created',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address1', 'address2', 'postal_code', 'city', 'country', 'latitude', 'longitude')
    readonly_fields = ('created', 'updated')
    list_filter = ('postal_code', 'city', 'country')
    ordering = ('created',)

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('ad', 'customer')
    readonly_fields = ('created', 'updated')
    ordering = ('created',)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('ad', 'updated')
    readonly_fields = ('created', 'updated')
    ordering = ('created',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'content', 'created')
    readonly_fields = ('created', 'updated')
    ordering = ('created',)

admin.site.register(Category)
#admin.site.register(Conversation)
#admin.site.register(Message)
#admin.site.register(Message)
