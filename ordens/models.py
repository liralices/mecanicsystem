from django.db import models
from clientes.models import Cliente, Veiculo
from estoque.models import Peca

class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('em_andamento', 'Em andamento'),
        ('aguardando_peca', 'Aguardando peça'),
        ('concluida', 'Concluída'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.DateField(auto_now_add=True)
    data_conclusao = models.DateField(null=True, blank=True)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    mao_de_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_total(self):
        itens = self.itemos_set.all()
        total_pecas = sum([item.peca.preco_venda * item.quantidade for item in itens])
        self.valor_total = total_pecas + self.mao_de_obra
        self.save()

    def __str__(self):
        return f"OS {self.id} - {self.cliente.nome}"

class ItemOS(models.Model):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    peca = models.ForeignKey(Peca, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    