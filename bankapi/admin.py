from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin import TabularInline
from .models import Branch, Bank


class BranchInline(admin.TabularInline):
    model = Branch
    extra = 1


class BankAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name','id']
    inlines = (
    	BranchInline,
    	)


admin.site.register(Bank, BankAdmin)


class BranchAdmin(admin.ModelAdmin):
    list_display = ['state','ifsc','city','district','branch','bank']
    search_fields = ['state','ifsc','city','district','branch','bank__name']

    def get_queryset(self, request):
        return super(BranchAdmin, self).get_queryset(request).prefetch_related('bank')


admin.site.register(Branch, BranchAdmin)

