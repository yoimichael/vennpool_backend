# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *
# Register your models here.
# what models to display on the admin site
admin.site.register(Event)
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Group)


