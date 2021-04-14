from django import forms
from _db import models
from datetime import datetime
from .utils import serial_number_transfer


class SEOForm(forms.ModelForm):
    class Meta:
        model = models.SEO
        fields = ['id', 'title', 'keywords', 'description']
        widgets = {
            'id': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'id': 'SEOTitleInput',
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
            }),
            'keywords': forms.TextInput(attrs={
                'id': 'SEOKeywordsInput',
                'class': 'form-control',
                'placeholder': 'Введите ключевые слова',
            }),
            'description': forms.TextInput(attrs={
                'id': 'SEODescriptionInput',
                'class': 'form-control',
                'placeholder': 'Введите описание',
            }),
        }


class WebsiteMainPageForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteMainPage
        fields = ['slide1', 'slide2', 'slide3', 'title', 'description']
        widgets = {
            'slide1': forms.FileInput(attrs={
                'class': 'upload',
                'id': 'File1Input',
            }),
            'slide2': forms.FileInput(attrs={
                'class': 'upload',
                'id': 'File2Input',
            }),
            'slide3': forms.FileInput(attrs={
                'class': 'upload',
                'id': 'File3Input',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
                'rows': '3',
            }),
            'description': forms.Textarea(attrs={
                'id': 'DescriptionInput',
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание',
            }),
        }


class WebsiteMainPageBlocksForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteMainPageBlocks
        fields = ['id', 'image', 'title', 'description']
        widgets = {
            'id': forms.HiddenInput(),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
                'rows': '3',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание',
            }),
        }


class WebsiteAboutForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteAbout
        fields = ['poster', 'title', 'description']
        widgets = {
            'poster': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
                'rows': '3',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание',
            }),
        }


class WebsiteAboutGalleryForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteMainPageBlocks
        fields = ['id', 'image']
        widgets = {
            'id': forms.HiddenInput(),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
        }


class WebsiteTariffsForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteTariffs
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
                'rows': '3',
            }),
            'description': forms.Textarea(attrs={
                'id': 'DescriptionInput',
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание',
            }),
        }


class WebsiteTariffsBlocksForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteTariffBlocks
        fields = ['id', 'image', 'title']
        widgets = {
            'id': forms.HiddenInput(),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
                'rows': '3',
            }),
        }


class WebsiteServiceBlocksForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteServiceBlocks
        fields = ['id', 'image', 'name', 'description']
        widgets = {
            'id': forms.HiddenInput(),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название услуги',
                'rows': '3',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание услуги',
            }),
        }


class WebsiteContactsForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteContacts
        fields = ['title', 'description', 'site', 'name', 'address', 'tel', 'email', ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание',
            }),
            'site': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ссылку',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес',
            }),
            'tel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер телефона',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите электронную почту',
            }),
        }


class RateForm(forms.ModelForm):

    class Meta:
        model = models.Rate
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'input_type': 'text',
                'class': 'form-control',
                'area_required': 'true',
            }),
            'description': forms.TextInput(attrs={
                'input_type': 'text',
                'class': 'form-control',
                'area_required': 'false',
            }),
        }


class AccountTransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transfer
        user = forms.ModelChoiceField(
            queryset=models.User.objects.filter(is_superuser=False),
            to_field_name="user",
            empty_label=None,
        )
        manager = forms.ModelChoiceField(
            queryset=models.User.objects.filter(is_superuser=True),
            to_field_name="manager",
            empty_label=None,
        )
        account = forms.ModelChoiceField(
            queryset=models.Account.objects.all(),
            to_field_name="account",
            empty_label=None,
        )
        fields = ['user', 'manager', 'account', 'transfer_type', 'amount', 'comment', 'payment_made', 'created_date',
                  'number']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'id': 'AmountInput',
                'class': 'form-control',
                'placeholder': 'Введите число',
            }),
            'comment': forms.Textarea(attrs={
                'id': 'CommentInput',
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите комментарий',
            }),
            'payment_made': forms.CheckboxInput(attrs={
                'id': 'PaymentMadeInput',
                'class': 'form-control',
            }),
            'created_date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': "form-control",
            }),
            'number': forms.TextInput(attrs={
                'input_type': 'text',
                # 'value': serial_number_transfer(),
                'class': 'form-control',
                'required': 'false'
            }),
        }

        
class AccountForm(forms.ModelForm):

    class Meta:
        model = models.Account
        house = forms.ModelChoiceField(
            queryset=models.House.objects.all(),
            empty_label=None,
        )

        section = forms.ModelChoiceField(
            queryset=models.Section.objects.all(),
            empty_label=None,
        )

        floor = forms.ModelChoiceField(
            queryset=models.Floor.objects.all(),
            empty_label=None,
        )

        fields = ['status', 'section', 'house', 'floor', 'wallet']
        widgets = {
            'wallet': forms.TextInput(attrs={
                'input_type': 'text',
                'class': 'form-control',
                # 'value': serial_number_account(),
                'aria-required': 'true'
            })
        }


class ApartmentForm(forms.ModelForm):

    class Meta:
        model = models.Apartment
        fields = ['apartment_area', 'name', 'house', 'floor', 'section', 'user', 'account', 'self_account']
        widgets = {
            'name': forms.TextInput(attrs={
                'input_type': 'text',
                'class': 'form-control',
                'area_required': 'true',
            }),
            'apartment_area': forms.NumberInput(attrs={
                'class': 'form-control',
                'area_required': 'false',
            }),
            'self_account': forms.TextInput(attrs={
                'input_type': 'text',
                'class': 'form-control',
                'area_required': 'false',
            }),
        }


class InvoiceIDCreateForm(forms.ModelForm):

    pass


class InvoiceTitleCreateForm(forms.ModelForm):
    pass


class InvoiceServicesCreateForm(forms.ModelForm):
    pass