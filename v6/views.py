from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.utils.timezone import localtime, now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Movimento, Servico, PessoaFisica, PessoaJuridica, Veiculo
from .forms import MovimentoForm, ServicoForm, PessoaFisicaForm, PessoaJuridicaForm, VeiculoForm
from django.db.models import Sum, Count

class ServicoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Servico
    template_name = 'servicos/servico_list.html'
    permission_required = 'lavajato.view_servico'

    def get_queryset(self):
        queryset = super().get_queryset()
        pesquisa = self.request.GET.get('pesquisaURL')
        if pesquisa:            
            queryset = queryset.filter(descricao__icontains=pesquisa)            
        return queryset

class ServicoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'servicos/servico_form.html'
    success_url = reverse_lazy('servico_list')
    permission_required = 'lavajato.add_servico' 

class ServicoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'servicos/servico_form.html'
    success_url = reverse_lazy('servico_list')
    permission_required = 'lavajato.change_servico'

class ServicoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Servico
    template_name = 'servicos/servico_confirm_delete.html'
    success_url = reverse_lazy('servico_list')
    permission_required = 'lavajato.delete_servico'

class PessoaFisicaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PessoaFisica
    template_name = 'fisica/fisica_list.html'
    permission_required = 'lavajato.view_pessoafisica'

    def get_queryset(self):
        queryset = super().get_queryset()
        termo_busca = self.request.GET.get('pesquisaURL')

        if termo_busca:
            queryset = queryset.filter(
                Q(nome__icontains=termo_busca) | Q(cpf__icontains=termo_busca)
            )
        return queryset

class PessoaFisicaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = PessoaFisica
    form_class = PessoaFisicaForm
    template_name = 'fisica/fisica_form.html'
    success_url = reverse_lazy('pessoafisica_list')
    permission_required = 'lavajato.add_pessoafisica'

class PessoaFisicaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PessoaFisica
    form_class = PessoaFisicaForm
    template_name = 'fisica/fisica_form.html'
    success_url = reverse_lazy('pessoafisica_list')
    permission_required = 'lavajato.change_pessoafisica'

class PessoaFisicaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = PessoaFisica
    template_name = 'fisica/fisica_confirm_delete.html'
    success_url = reverse_lazy('pessoafisica_list')
    permission_required = 'lavajato.delete_pessoafisica'

class PessoaJuridicaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PessoaJuridica
    template_name = 'juridica/juridica_list.html'
    permission_required = 'lavajato.view_pessoajuridica'

    def get_queryset(self):
        queryset = super().get_queryset()
        termo_busca = self.request.GET.get('pesquisaURL')
        if termo_busca:
            queryset = queryset.filter(
                Q(nome__icontains=termo_busca) | Q(cnpj__icontains=termo_busca)
            )
        return queryset

class PessoaJuridicaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = PessoaJuridica
    form_class = PessoaJuridicaForm
    template_name = 'juridica/juridica_form.html'
    success_url = reverse_lazy('pessoajuridica_list')
    permission_required = 'lavajato.add_pessoajuridica'

class PessoaJuridicaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PessoaJuridica
    form_class = PessoaJuridicaForm
    template_name = 'juridica/juridica_form.html'
    success_url = reverse_lazy('pessoajuridica_list')
    permission_required = 'lavajato.change_pessoajuridica'

class PessoaJuridicaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = PessoaJuridica
    template_name = 'juridica/juridica_confirm_delete.html'
    success_url = reverse_lazy('pessoajuridica_list')
    permission_required = 'lavajato.delete_pessoajuridica'    

class VeiculoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Veiculo
    template_name = 'veiculos/veiculo_list.html'
    permission_required = 'lavajato.view_veiculo'

    def get_queryset(self):
        # OBSERVAÇÃO  <<<<<<<<<<<<<<<<<
        # select_related faz um SQL JOIN antecipado com a tabela Pessoa.
        # Sem isso, se a tela listar 50 veículos, o Django faria 51 consultas separadas 
        # para ver o nome do dono de cada carro.
        queryset = super().get_queryset().select_related('pessoa')
        
        termo_busca = self.request.GET.get('pesquisaURL')

        if termo_busca:
            queryset = queryset.filter(
                Q(placa__icontains=termo_busca) | Q(modelo__icontains=termo_busca)
            )
        return queryset.order_by('placa')

class VeiculoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'veiculos/veiculo_form.html'
    success_url = reverse_lazy('veiculo_list')
    permission_required = 'lavajato.add_veiculo'

class VeiculoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'veiculos/veiculo_form.html'
    success_url = reverse_lazy('veiculo_list')
    permission_required = 'lavajato.change_veiculo'

class VeiculoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Veiculo
    template_name = 'veiculos/veiculo_confirm_delete.html'
    success_url = reverse_lazy('veiculo_list')
    permission_required = 'lavajato.delete_veiculo'    


class MovimentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Movimento
    template_name = 'movimentos/movimento_list.html'
    permission_required = 'lavajato.view_movimento'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('veiculo', 'servico')
        
        termo_busca = self.request.GET.get('pesquisaURL')
        apenas_pendentes = self.request.GET.get('pendentes')

        if termo_busca:            
            queryset = queryset.filter(
                Q(veiculo__placa__icontains=termo_busca) | 
                Q(servico__descricao__icontains=termo_busca)   # ATENÇÃO no duplo underline para acessar o campo descricao Servico
            )       

        if apenas_pendentes == 'on':
            queryset = queryset.filter(pagamento='N')     
        
        return queryset.order_by('-data', '-hora')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apenas_pendentes'] = self.request.GET.get('pendentes')
        context['termo_busca'] = self.request.GET.get('pesquisaURL', '')
        
        return context

class MovimentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Movimento
    form_class = MovimentoForm
    template_name = 'movimentos/movimento_form.html'
    success_url = reverse_lazy('movimento_list')
    permission_required = 'lavajato.add_movimento'

class MovimentoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Movimento
    form_class = MovimentoForm
    template_name = 'movimentos/movimento_form.html'
    success_url = reverse_lazy('movimento_list')
    permission_required = 'lavajato.change_movimento'

class MovimentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Movimento
    template_name = 'movimentos/movimento_confirm_delete.html'
    success_url = reverse_lazy('movimento_list')
    permission_required = 'lavajato.delete_movimento'    


#    Vamos misturar com Function-Based View
def painel_pagamentos(request):
    cliente_busca = request.GET.get('cliente', '')
    movimentos_pendentes = None
    total_geral = 0

    if cliente_busca:
        movimentos_pendentes = Movimento.objects.filter(
            veiculo__pessoa__nome__icontains=cliente_busca, 
            pagamento='N'
        )
        
        soma = movimentos_pendentes.aggregate(Sum('valor'))['valor__sum']
        total_geral = soma if soma else 0

    if request.method == 'POST':
        lista_ids = request.POST.getlist('movimentos_ids')
        
        if lista_ids:
            Movimento.objects.filter(id__in=lista_ids).update(
                pagamento='S',
                data_pagto=localtime(now()).date()
            )
            messages.success(request, 'Pagamentos confirmados com sucesso!')
            return redirect('painel_pagamentos')

    return render(request, 'movimentos/painel_pagamentos.html', {
        'movimentos': movimentos_pendentes,
        'total': total_geral,
        'cliente_busca': cliente_busca  
    })

def dashboard(request):
    data_inicial = request.GET.get('data_inicial', '')
    data_final = request.GET.get('data_final', '')

    movimentos = Movimento.objects.all()

    if data_inicial and data_final:
        movimentos = movimentos.filter(data__range=[data_inicial, data_final])

    total_lavagens = movimentos.count()
    
    faturamento_geral = movimentos.aggregate(Sum('valor'))['valor__sum'] or 0
    
    pendentes_qs = movimentos.filter(pagamento='N')
    qtd_pendentes = pendentes_qs.count()
    valor_pendente = pendentes_qs.aggregate(Sum('valor'))['valor__sum'] or 0

    servico_top = movimentos.values('servico__descricao').annotate(total=Count('id')).order_by('-total').first()    

    carro_top = movimentos.values('veiculo__modelo').annotate(total=Count('id')).order_by('-total').first()

    ranking_clientes = movimentos.values('veiculo__pessoa__nome').annotate(total_gasto=Sum('valor')).order_by('-total_gasto')[:5]

    contexto = {
        'data_inicial': data_inicial,
        'data_final': data_final,
        'total_lavagens': total_lavagens,
        'faturamento_geral': faturamento_geral,
        'qtd_pendentes': qtd_pendentes,
        'valor_pendente': valor_pendente,
        'servico_top': servico_top,
        'carro_top': carro_top,
        'ranking_clientes': ranking_clientes,
    }
    
    return render(request, 'movimentos/dashboard.html', contexto)
