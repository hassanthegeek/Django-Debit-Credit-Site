from django import forms
from django.core.checks import messages
from django.core.validators import DecimalValidator, MinValueValidator
from django.db.models.expressions import Case, When
from django.db.models.fields import DecimalField, FloatField
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import F, Sum, Window, RowRange
from django.shortcuts import resolve_url
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from .models import Shop, Account, AccountDetail
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ShopCreateForm, EntryCreationForm
# Create your views here.


@login_required
def home(request):
    return render(request, 'account/home.html')


class ShopListView(LoginRequiredMixin, ListView):
    model = Shop


# class ShopCreateView(LoginRequiredMixin, CreateView):
#     model = Shop

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


class ShopCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ShopCreateForm()
        return render(request, 'accounts/create_shop.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ShopCreateForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('account:home')
        return render(request, 'accounts/create_shop.html', {'form': form})


class ShopListView(LoginRequiredMixin, ListView):
    model = Shop
    context_object_name = 'shops'
    template_name = 'accounts/home.html'
    login_url = 'user:login'
    # def get_queryset(self):
    # return Shop.objects.filter(user=self.request.user)

    def get_queryset(self):
        s = Shop.objects.filter(user=self.request.user)
        r = s.annotate(balance=Sum('accountdetail__amount'),
                       td=Sum(Case(When(accountdetail__amount__gt=0, then=F(
                           'accountdetail__amount')), default=0, output_field=DecimalField(decimal_places=2))),
                       tc=Sum(Case(When(accountdetail__amount__lt=0, then=F('accountdetail__amount')), default=0, output_field=DecimalField(decimal_places=2))))
        td = 0
        tc = 0
        for e in r:
            td += abs(e.td)
            tc += abs(e.tc)
        menu = {'td': td, 'tc': tc, 'tb': td-tc}
        r = {'r': r, 'menu': menu}
        return r


class ShopUpdateView(UpdateView):
    model = Shop
    fields = ['name', 'address', 'phone']


class ShopAccounts(ListView):
    template_name = 'accounts/shop_account_details.html'
    context_object_name = 'entries'
    model = AccountDetail

    def get_queryset(self):
        u = self.request.user
        shop = Shop.objects.get(id=self.kwargs.get('pk'))
        ad = AccountDetail.objects.filter(shop=shop)
        d = {}
        d['data'] = ad.annotate(
            balance=Window(Sum(F'amount'),
                           order_by=F("date").asc(),
                           frame=RowRange(end=0))
        )
        d['shop'] = shop
        d['total_debit'] = ad.filter(amount__gt=0).aggregate(td=Sum('amount'))
        d['total_credit'] = ad.filter(amount__lt=0).aggregate(tc=Sum('amount'))
        d['total_balance'] = ad.aggregate(tb=Sum('amount'))
        return d


class CreateAccountDetail(View):
    def get(self, request, *args, **kwargs):
        form = EntryCreationForm()
        return render(request, 'accounts/create_account_detail.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = EntryCreationForm(self.request.POST)
        if form.is_valid():
            data = form.cleaned_data
            amount = data['debit'] if data['debit'] > 0 else -data['credit']
            remarks = data['remarks']
            shop = Shop.objects.get(id=kwargs.get('pk'))
            print(shop)
            account = Account.objects.get(user=request.user)
            AccountDetail.objects.create(
                account=account,
                shop=shop,
                amount=amount,
                remarks=remarks)
            return redirect('account:shop-account-details', shop.id)
        return render(request, 'accounts/create_account_detail.html', {'form': form})


def delete_accoun_detail(request, pk, *args):
    # ad = AccountDetail.objects.get(pk=pk)
    ad = get_object_or_404(AccountDetail, pk=pk)
    id = ad.shop.id
    ad.delete()
    return redirect(f'/shops/{id}/details/')


class UpdateAccountDetail(View):
    def get(self, request, *args, **kwargs):
        ad = get_object_or_404(AccountDetail, pk=self.kwargs.get('pk'))
        print(ad)
        d = ad.amount if ad.amount > 0 else 0
        c = -ad.amount if ad.amount < 0 else 0
        form = EntryCreationForm(
            data={'debit': d, 'credit': c, 'remarks': ad.remarks})
        return render(request, 'accounts/shop_account_detail_update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        ad = get_object_or_404(AccountDetail, pk=self.kwargs.get('pk'))
        form = EntryCreationForm(self.request.POST)
        if form.is_valid():
            d = form.cleaned_data.get(
                'debit') if form.cleaned_data.get('debit') > 0 else None
            c = -form.cleaned_data.get(
                'credit') if form.cleaned_data.get('credit') > 0 else None
            if d:
                ad.amount = d
            else:
                ad.amount = c
            ad.remarks = form.cleaned_data.get('remarks')
            print(ad.shop)
            ad.save()
            return redirect('account:shop-account-details', ad.shop.id)
        else:
            return render(request, 'accounts/shop_account_detail_update.html', {'form': form})
