from django.contrib import admin
from django.urls import path
from core import views
from core import templates
from core import templates as templates_views


urlpatterns = [
    path('buscar-produto/<int:id_produto>/', views.buscar_produto_anymarket, name='buscar_produto', ),
    path('admin/', admin.site.urls),
]