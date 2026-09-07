from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Servico
from .forms import ServicoForm

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
