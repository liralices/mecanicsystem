from django.db import models

class ConfiguracaoOficina(models.Model):
    nome_oficina = models.CharField(max_length=200, default="Minha Oficina")
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    endereco = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome_oficina
    
    class Meta:
        verbose_name = "Configuração da Oficina"
        verbose_name_plural = "Configurações da Oficina"

class Funcionario(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
