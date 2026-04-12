from django.db import models
from clientes.models import Cliente
from estoque.models import Peca

class OrdemServico(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    descricao = models.TextField()
    mao_de_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"OS {self.id} - {self.cliente.nome}"

    def calcular_total(self):
        total = self.mao_de_obra

        itens = ItemOS.objects.filter(ordem_servico=self)
        for item in itens:
            total += item.peca.preco_venda * item.quantidade

        self.valor_total = total
        self.save()

    def __str__(self):
        return f"OS {self.id} - {self.cliente.nome}"

class ItemOS(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    peca = models.ForeignKey(Peca, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    
# Create your models here.
