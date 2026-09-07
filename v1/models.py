import uuid
from django.db import models


class ModeloBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)      
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:        
        abstract = True


class Pessoa(ModeloBase):
    nome = models.CharField(max_length=150)
    endereco = models.CharField(max_length=200)
    email = models.EmailField(max_length=150, null=True, blank=True)
    celular = models.CharField(max_length=20)
    credito = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta: # type: ignore
        db_table = 'pessoas' 


    @property   # Ultima vez q o cliente lavou o veiuclo
    def ultima_lavagem(self):
        from .models import Movimento        

        ultimo_movimento = Movimento.objects.filter(
            veiculo__pessoa=self
        ).order_by('-data', '-hora').first()
        
        return ultimo_movimento.data if ultimo_movimento else None    

    def __str__(self):
        return self.nome

class PessoaFisica(Pessoa):                 
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    identidade = models.CharField(max_length=20, null=True, blank=True)

    class Meta:    # type: ignore
        db_table = 'pessoas_fisicas'

class PessoaJuridica(Pessoa):
    cnpj = models.CharField(max_length=14, unique=True)
    contato_nome = models.CharField(max_length=150, null=True, blank=True)

    class Meta:  # type: ignore
        db_table = 'pessoas_juridicas'

class Veiculo(ModeloBase):    
    pessoa = models.ForeignKey(Pessoa, on_delete=models.PROTECT, related_name='veiculos')
    placa = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=50)
    modelo = models.CharField(max_length=80)
    cor = models.CharField(max_length=40, null=True, blank=True)

    class Meta: # type: ignore
        db_table = 'veiculos'

    def __str__(self):
        return f"{self.modelo} ({self.placa})"

    @property    
    def ultima_lavagem(self):
        ultimo_movimento = self.movimentos.order_by('-data', '-hora').first() # type: ignore
        return ultimo_movimento.data if ultimo_movimento else None
        # Atenção com o paramentro -data e -hora 

class Servico(ModeloBase):
    OPCOES_FIDELIDADE = [
        ('S', 'Sim'),
        ('N', 'Não'),
    ]
    descricao = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fidelidade = models.CharField(max_length=1, choices=OPCOES_FIDELIDADE)

    class Meta: # type: ignore
        db_table = 'servicos'

    def __str__(self):
        return self.descricao

class Movimento(ModeloBase):
    OPCOES_PAGAMENTO = [
        ('S', 'Sim'),
        ('N', 'Não'),
    ]    

    veiculo = models.ForeignKey(
        Veiculo, 
        to_field='placa',              # ESTA USANDO A PLACA COMO FK
        db_column='placa', 
        on_delete=models.PROTECT, 
        related_name='movimentos'
    )
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    data = models.DateField()
    hora = models.TimeField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    pagamento = models.CharField(max_length=1, choices=OPCOES_PAGAMENTO)
    data_pagto = models.DateField(null=True, blank=True)

    class Meta: # type: ignore
        db_table = 'movimentos'

    def __str__(self):
        return f"Movimento {self.id} - {self.veiculo.placa}"  # type: ignore