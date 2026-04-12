from django.db import models

class Peca(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField(default=0)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    fornecedor = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nome
    
