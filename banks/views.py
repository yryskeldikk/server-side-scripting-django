from django.http import HttpResponse, Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from .forms import BankForm, BranchForm
from .models import Bank, Branch


class BankCreateView(LoginRequiredMixin, FormView):
    template_name = "banks/bank_create.html"
    form_class = BankForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("UNAUTHORIZED", status=401)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        bank = form.save(commit=False)
        bank.owner = self.request.user
        bank.save()
        self.success_url = reverse_lazy(
            "banks:bank-details", kwargs={"bank_id": bank.id}
        )
        return super().form_valid(form)


class BankDetailsView(DetailView):
    model = Bank
    template_name = "banks/bank_detail.html"
    context_object_name = "bank"

    def get_object(self, queryset=None):
        bank = get_object_or_404(Bank, pk=self.kwargs["bank_id"])
        return bank


class BranchCreateView(LoginRequiredMixin, FormView):
    template_name = "banks/branch_create.html"
    form_class = BranchForm

    def dispatch(self, request, bank_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("UNAUTHORIZED", status=401)
        
        try:
            bank = Bank.objects.get(id=bank_id)
        except Bank.DoesNotExist:
            raise Http404()

        if bank.owner != self.request.user:
            return HttpResponseForbidden()

        return super().dispatch(request, bank_id, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BranchCreateView, self).get_context_data(*args, **kwargs)
        context["bank_id"] = self.kwargs["bank_id"]
        return context

    def form_valid(self, form):
        branch = form.save(commit=False)
        branch.bank = Bank.objects.get(id=self.kwargs["bank_id"])
        branch.save()
        self.success_url = reverse_lazy(
            "banks:branch-details", kwargs={"branch_id": branch.id}
        )
        return super().form_valid(form)


class BranchDetailsView(View):
    def get(self, request, branch_id, *args, **kwargs):
        branch = get_object_or_404(Branch, pk=branch_id)
        data = {
            "id": branch.id,
            "name": branch.name,
            "transit_num": branch.transit_num,
            "address": branch.address,
            "email": branch.email,
            "capacity": branch.capacity,
            "last_modified": branch.last_modified,
        }
        return JsonResponse(data)


class BranchListView(View):
    def get(self, request, bank_id, *args, **kwargs):
        bank = get_object_or_404(Bank, pk=bank_id)
        branches = Branch.objects.filter(bank__id=bank_id)
        branch_data = [
            {
                "id": branch.id,
                "name": branch.name,
                "transit_num": branch.transit_num,
                "address": branch.address,
                "email": branch.email,
                "capacity": branch.capacity,
                "last_modified": branch.last_modified,
            }
            for branch in branches
        ]
        return JsonResponse(branch_data, safe=False)


class BankListView(ListView):
    model = Bank
    template_name = "banks/bank_list.html"
    context_object_name = "bank_list"


class BranchUpdateView(LoginRequiredMixin, UpdateView):
    model = Branch
    template_name = "banks/edit_branch.html"
    form_class = BranchForm
    
    def dispatch(self, request, branch_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("UNAUTHORIZED", status=401)
        return super().dispatch(request, branch_id, *args, **kwargs)

    def get_object(self, queryset=None):
        branch = get_object_or_404(Branch, pk=self.kwargs["branch_id"])
        if branch.bank.owner != self.request.user:
            return self.handle_no_permission()

        return branch

    def get_context_data(self, *args, **kwargs):
        context = super(BranchUpdateView, self).get_context_data(*args, **kwargs)
        context["branch_id"] = self.kwargs["branch_id"]
        return context

    def get_success_url(self):
        return reverse_lazy(
            "banks:branch-details", kwargs={"branch_id": self.kwargs["branch_id"]}
        )
