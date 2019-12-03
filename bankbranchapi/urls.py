from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from bankapi.api import BranchIFSCView, BankBranchView
from bankapi.views import index

urlpatterns = [
    path('', index, name='index'),
    path('api/branch-ifsc/<ifsc>/', BranchIFSCView.as_view(), name="branch-ifsc"),
    path('api/bank-branch/', BankBranchView.as_view(), name="bank-branch"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)