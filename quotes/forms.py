from django import forms
from django.contrib.auth.models import User

from .models import PartRequest, Quote


class PartRequestForm(forms.ModelForm):
    class Meta:
        model = PartRequest

        fields = [
            'customer_name',
            'phone_number',
            'location',
            'vin_number',
            'vehicle_make',
            'vehicle_model',
            'vehicle_year',
            'engine_details',
            'part_name',
            'part_description',
            'part_image',
        ]

        widgets = {
            'customer_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Eddie Chauke'
            }),

            'phone_number': forms.TextInput(attrs={
                'placeholder': 'e.g. 071 234 5678'
            }),

            'location': forms.TextInput(attrs={
                'placeholder': 'e.g. Randburg, Johannesburg'
            }),

            'vin_number': forms.TextInput(attrs={
                'placeholder': 'Enter VIN number if available'
            }),

            'vehicle_make': forms.TextInput(attrs={
                'placeholder': 'e.g. Volkswagen'
            }),

            'vehicle_model': forms.TextInput(attrs={
                'placeholder': 'e.g. Polo'
            }),

            'vehicle_year': forms.NumberInput(attrs={
                'placeholder': 'e.g. 2021'
            }),

            'engine_details': forms.TextInput(attrs={
                'placeholder': 'e.g. 1.6 Petrol'
            }),

            'part_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Front brake pads'
            }),

            'part_description': forms.Textarea(attrs={
                'placeholder': 'Describe the part you need or the vehicle problem...'
            }),

            'part_image': forms.ClearableFileInput(attrs={
                'accept': 'image/*'
            }),
        }


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote

        fields = [
            'price',
            'availability',
            'notes',
        ]

        widgets = {
            'price': forms.NumberInput(attrs={
                'placeholder': 'e.g. 850.00',
                'step': '0.01'
            }),

            'availability': forms.TextInput(attrs={
                'placeholder': 'e.g. In stock'
            }),

            'notes': forms.Textarea(attrs={
                'placeholder': 'e.g. Front brake pad set available for collection today.'
            }),
        }


class ShopRegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Choose a username'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a password'
        })
    )

    shop_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. AutoZone Randburg'
        })
    )

    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. 071 234 5678'
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'e.g. shop@example.com'
        })
    )

    location = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. Randburg, Johannesburg'
        })
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Physical shop address'
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                'This username is already taken. Please choose another.'
            )

        return username