from django.contrib import admin

# Register your models here.
from .models import Project, CaseStep, Case, Module, Variables, Config
admin.site.register(Project)
admin.site.register(CaseStep)
admin.site.register(Case)
admin.site.register(Module)
admin.site.register(Variables)
admin.site.register(Config)