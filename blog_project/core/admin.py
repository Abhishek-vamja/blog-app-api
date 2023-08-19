"""
Admin for all models.
"""

from django.contrib import admin

from core.models import *


admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Tag)