from django.core.validators import *
from django import forms
from .models import AccountDetail, Shop
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ShopCreateForm(forms.ModelForm):
    phone = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial='PK'))

    class Meta:
        model = Shop
        fields = ['name', 'phone', 'address']


class EntryCreationForm(forms.Form):
    '''        Adding an entry.
    '''
    debit = forms.DecimalField(required=False, validators=[DecimalValidator(
        10, 2), MinValueValidator(0, 'It could not be empty')])
    credit = forms.DecimalField(required=False, validators=[DecimalValidator(
        10, 2), MinValueValidator(0, 'It could not be empty')])
    remarks = forms.CharField(required=False, widget=forms.Textarea)

    def clean(self):
        try:
            credit = float(self.cleaned_data.get('credit'))

        except TypeError:
            credit = 0
        try:
            debit = float(self.cleaned_data.get('debit'))
        except TypeError:
            debit = 0

        if (debit == 0 and credit == 0) or (debit > 0 and credit > 0):
            raise forms.ValidationError('Only and only one must be filled')
        self.cleaned_data['debit'] = debit
        self.cleaned_data['credit'] = credit
        self.cleaned_data['remarks'] = self.data.get('remarks')
        return self.cleaned_data

# class EntryCreationForm(forms.ModelForm):
#     debit = forms.DecimalField(validators=[DecimalValidator(
#         10, 2), MinValueValidator(0, 'It could not be empty')])
#     credit = forms.DecimalField(validators=[DecimalValidator(
#         10, 2), MinValueValidator(0, 'It could not be empty')])

#     class Meta:
#         model = AccountDetail
#         fields = ['debit', 'credit', 'remarks']

#     def clean(self):
#         debit = float(self.cleaned_data.get('debit'))
#         try:
#             credit = float(self.cleaned_data.get('credit'))

#         except TypeError:
#             credit = 0
#         try:
#             debit = float(self.cleaned_data.get('debit'))
#         except TypeError:
#             debit = 0

#         if (debit == 0 and credit == 0) or (debit > 0 and credit > 0):
#             raise forms.ValidationError('Only and only one must be filled')
#         return super().clean()
