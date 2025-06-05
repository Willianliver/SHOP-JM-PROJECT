from django.contrib import admin
from django.urls import path
from core import views
from core import templates
from core import templates as templates_views


urlpatterns = [
    path('buscar-produto/<int:id_produto>/', views.buscar_produto_anymarket, name='buscar_produto', ),
    path('vincular-ids/', views.vincular_ids, name='vincular_ids'),
    path('admin/', admin.site.urls),
]