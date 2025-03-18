from django import forms
from .models import PlantingRequest, Donation, TreeType


class PlantingRequestForm(forms.ModelForm):
    class Meta:
        model = PlantingRequest
        fields = ['name', 'email', 'phone', 'address', 'description', 'preferred_tree_type']
        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Расскажите, почему вы хотите озеленить это место?'}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес для озеленения'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs[
                'class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500'


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'email', 'phone', 'donation_type', 'amount', 'description', 'is_anonymous']
        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Дополнительная информация о вашей поддержке'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'h-4 w-4 text-green-600'
            else:
                field.widget.attrs[
                    'class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500'

        # Динамически показывать/скрывать поле amount
        self.fields['amount'].widget.attrs['id'] = 'id_amount'
        self.fields['donation_type'].widget.attrs['onchange'] = 'toggleAmountField()'


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
        'placeholder': 'Ваше имя'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
        'placeholder': 'Ваш email'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
        'rows': 4,
        'placeholder': 'Ваше сообщение'
    }))