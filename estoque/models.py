from django.db import models
from django.db.models import Max

class Peca(models.Model):
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Código")
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=5)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    fornecedor = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['nome']

    def save(self, *args, **kwargs):
        if not self.codigo:
            # Gerar código automático: PEC + próximo número
            max_id = Peca.objects.aggregate(Max('id'))['id__max'] or 0
            self.codigo = f"PEC{max_id + 1:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        if self.codigo:
            return f"{self.codigo} - {self.nome}"
        return self.nome

    def estoque_baixo(self):
        return self.quantidade <= self.estoque_minimo
    
