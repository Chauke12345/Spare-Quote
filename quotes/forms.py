from django import forms
from django.contrib.auth.models import User

from .models import PartRequest, Quote, Review


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

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', '')

        # Remove common formatting characters
        cleaned = (
            phone_number
            .replace(' ', '')
            .replace('-', '')
            .replace('(', '')
            .replace(')', '')
        )

        # Convert +27 format to local 0 format
        if cleaned.startswith('+27'):
            local_number = '0' + cleaned[3:]

        # Convert 27 format to local 0 format
        elif cleaned.startswith('27'):
            local_number = '0' + cleaned[2:]

        else:
            local_number = cleaned

        # Must contain digits only
        if not local_number.isdigit():
            raise forms.ValidationError(
                'Please enter a valid phone number.'
            )

        # South African local numbers should have 10 digits
        if len(local_number) != 10:
            raise forms.ValidationError(
                'Please enter a valid 10-digit South African phone number, e.g. 071 234 5678.'
            )

        # Local format must begin with 0
        if not local_number.startswith('0'):
            raise forms.ValidationError(
                'Please enter a valid South African phone number.'
            )

        return local_number

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
class ReviewForm(forms.ModelForm):

    RATING_CHOICES = [
        (5, '5 - Excellent'),
        (4, '4 - Very Good'),
        (3, '3 - Good'),
        (2, '2 - Fair'),
        (1, '1 - Poor'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Review

        fields = [
            'rating',
            'comment',
        ]

        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Tell us about your experience with the shop...',
                'rows': 4
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
class TrackRequestForm(forms.Form):

    request_id = forms.IntegerField(
        label='Request Number',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Example: 16'
        })
    )

    phone_number = forms.CharField(
        label='Phone Number',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Example: 0712345678'
        })
    )

    from django import forms
from .models import Shop


class AdminNotificationForm(forms.Form):

    SEND_TO_CHOICES = [
        ('all', 'All Shops'),
        ('shop', 'Specific Shop'),
    ]

    send_to = forms.ChoiceField(
        choices=SEND_TO_CHOICES
    )

    shop = forms.ModelChoiceField(
        queryset=Shop.objects.filter(is_active=True).order_by('shop_name'),
        required=False
    )

    title = forms.CharField(
        max_length=150
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'placeholder': 'Write your notification message...'
            }
        )
    )

    notification_type = forms.ChoiceField(
        choices=[
            ('info', 'Information'),
            ('warning', 'Warning'),
            ('success', 'Success'),
            ('maintenance', 'Maintenance'),
        ]
    )