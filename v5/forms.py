from django.utils.timezone import localtime, now
import calendar
import re
from django.core.exceptions import ValidationError
from django import forms
from .models import Movimento, Servico, PessoaFisica, PessoaJuridica, Veiculo

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['descricao', 'valor', 'fidelidade']
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control', 
                'autofocus': 'autofocus'  
            }),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'fidelidade': forms.Select(attrs={'class': 'form-select'}),
        }        

class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica       
        fields = ['nome', 'cpf', 'identidade', 'data_nascimento', 'endereco', 'celular', 'email', 'credito']
        
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}),
            'identidade': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'credito': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PessoaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        fields = ['nome', 'cnpj', 'contato_nome', 'endereco', 'celular', 'email', 'credito']
        
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}),
            'contato_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do responsável'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'credito': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['pessoa', 'placa', 'tipo', 'modelo', 'cor']
        
        widgets = {
            'pessoa': forms.Select(attrs={'class': 'form-select', 'autofocus': 'autofocus'}),
            'placa': forms.TextInput(attrs={
                'class': 'form-control', 
                'style': 'text-transform: uppercase;',
                'placeholder': 'AAA-0000 ou AAA0A00',                
                'pattern': '[a-zA-Z]{3}-?[0-9][a-zA-Z0-9][0-9]{2}',
                'title': 'Digite uma placa válida (ex: AAA-0000 ou AAA0A00)'
            }),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Sedan, SUV, Moto'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'cor': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_placa(self):
        placa = self.cleaned_data.get('placa', '').upper()
        placa_limpa = re.sub(r'[^A-Z0-9]', '', placa) # permite apenas letras e números - REgullar expression 
        if not re.match(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$', placa_limpa):
            raise ValidationError('A placa informada é inválida.')
        return placa_limpa
        # solution suggested by Gemini


from django import forms
from django.utils.timezone import localtime, now
from .models import Movimento

from django import forms
from django.utils.timezone import localtime, now
from .models import Movimento

class MovimentoForm(forms.ModelForm):
    class Meta:
        model = Movimento
        fields = ['veiculo', 'servico', 'data', 'hora', 'valor', 'pagamento', 'data_pagto']
        
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select', 'autofocus': 'autofocus'}),
            'servico': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(format='%H:%M', attrs={'class': 'form-control', 'type': 'time'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pagamento': forms.Select(attrs={'class': 'form-select'}),
            'data_pagto': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # INTERCEPTAÇÃO (Antes da construção do formulário)
        # Verifica se é um registro novo analisando a instância dentro do kwargs
        instancia = kwargs.get('instance')
        
        if not instancia or not instancia.pk:
            agora = localtime(now())

            initial = kwargs.get('initial', {})

            ultimo_dia_mes = calendar.monthrange(agora.year, agora.month)[1]
            data_vencimento = agora.replace(day=ultimo_dia_mes)

            initial['data_pagto'] = data_vencimento.strftime('%Y-%m-%d')
            
            initial = kwargs.get('initial', {})
            
            initial['data'] = agora.strftime('%Y-%m-%d')
            initial['hora'] = agora.strftime('%H:%M')
            initial['pagamento'] = 'N'
            
            kwargs['initial'] = initial

        super().__init__(*args, **kwargs)
        
        self.fields['pagamento'].disabled = True
        # solution suggested by Gemini