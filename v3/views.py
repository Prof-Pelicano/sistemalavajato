from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Servico, PessoaFisica, PessoaJuridica, Veiculo
from .forms import ServicoForm, PessoaFisicaForm, PessoaJuridicaForm, VeiculoForm

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