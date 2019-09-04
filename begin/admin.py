from django.contrib import admin

# Register your models here.
from .models import Project, Step, Case, Variables, Config, Category, API, Classify, TestSuite, Report


class ClassifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'level')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'parent_category', 'category_type')


admin.site.register(Project)
admin.site.register(Step)
admin.site.register(Case)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Variables)
admin.site.register(Config)
admin.site.register(API)
admin.site.register(Classify, ClassifyAdmin)
admin.site.register(TestSuite)
admin.site.register(Report)