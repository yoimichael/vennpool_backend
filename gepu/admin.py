from django.contrib import admin

from .models import *

# what models to display on the admin site
admin.site.register(Event)
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Group)

