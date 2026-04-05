from django.contrib import admin
from django.urls import path
from api.views import VisualizeSVMView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/visualize/svm/', VisualizeSVMView.as_view(), name='visualize_svm'),

]

