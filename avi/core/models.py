from django.db import models
from datetime import datetime

class LogBusca(models.Model):
    sku = models.CharField(max_length=100)
    id_prod_hub = models.CharField(max_length=100)
    status = models.CharField(max_length=50)  # Sucesso, Erro, etc.
    mensagem = models.TextField()
    data_hora = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.sku} - {self.status}'
