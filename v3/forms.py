import re
from django.core.exceptions import ValidationError
from django import forms
from .models import Servico, PessoaFisica, PessoaJuridica, Veiculo

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
        placa_limpa = re.sub(r'[^A-Z0-9]', '', placa) # permite apenas letras e números
        if not re.match(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$', placa_limpa):
            raise ValidationError('A placa informada é inválida.')
        return placa_limpa
        # solution suggested by Gemini