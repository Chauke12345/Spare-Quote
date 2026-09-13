from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

from .models import (
    PartRequest,
    Quote,
    Review,
    Shop,
    SupportTicket,
)

class PartRequestForm(forms.ModelForm):

    class Meta:
        model = PartRequest

        fields = [
            'customer_name',
            'phone_number',
            'location',

            # Vehicle input choice
            'vehicle_input_method',
            'licence_disc_image',

            # Manual vehicle details
            'vin_number',
            'vehicle_make',
            'vehicle_model',
            'vehicle_year',
            'engine_details',

            # Part details
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

            # =====================================================
            # VEHICLE INPUT METHOD
            # =====================================================

            'vehicle_input_method': forms.RadioSelect(),

            'licence_disc_image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
                'capture': 'environment'
            }),

            # =====================================================
            # MANUAL VEHICLE DETAILS
            # =====================================================

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

            # =====================================================
            # PART DETAILS
            # =====================================================

            'part_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Front brake pads'
            }),

            'part_description': forms.Textarea(attrs={
                'placeholder': (
                    'Describe the part you need or the vehicle problem...'
                )
            }),

            'part_image': forms.ClearableFileInput(attrs={
                'accept': 'image/*'
            }),
        }

    # =========================================================
    # VALIDATE VEHICLE INPUT METHOD
    # =========================================================

    def clean(self):

        cleaned_data = super().clean()

        input_method = cleaned_data.get(
            'vehicle_input_method'
        )

        licence_disc = cleaned_data.get(
            'licence_disc_image'
        )

        vehicle_make = cleaned_data.get(
            'vehicle_make'
        )

        vehicle_model = cleaned_data.get(
            'vehicle_model'
        )

        vehicle_year = cleaned_data.get(
            'vehicle_year'
        )

        # Customer selected manual vehicle details
        if input_method == 'manual':

            if not vehicle_make:
                self.add_error(
                    'vehicle_make',
                    'Please enter the vehicle make.'
                )

            if not vehicle_model:
                self.add_error(
                    'vehicle_model',
                    'Please enter the vehicle model.'
                )

            if not vehicle_year:
                self.add_error(
                    'vehicle_year',
                    'Please enter the vehicle year.'
                )

        # Customer selected licence disc
        elif input_method == 'disc':

            if not licence_disc:
                self.add_error(
                    'licence_disc_image',
                    'Please upload a clear photo of the vehicle licence disc.'
                )

        return cleaned_data

    # =========================================================
    # PHONE NUMBER VALIDATION
    # =========================================================

    def clean_phone_number(self):

        phone_number = self.cleaned_data.get(
            'phone_number',
            ''
        )

        cleaned = (
            phone_number
            .replace(' ', '')
            .replace('-', '')
            .replace('(', '')
            .replace(')', '')
        )

        if cleaned.startswith('+27'):
            local_number = '0' + cleaned[3:]

        elif cleaned.startswith('27'):
            local_number = '0' + cleaned[2:]

        else:
            local_number = cleaned

        if not local_number.isdigit():
            raise forms.ValidationError(
                'Please enter a valid phone number.'
            )

        if len(local_number) != 10:
            raise forms.ValidationError(
                'Please enter a valid 10-digit South African '
                'phone number, e.g. 071 234 5678.'
            )

        if not local_number.startswith('0'):
            raise forms.ValidationError(
                'Please enter a valid South African phone number.'
            )

        return local_number


# =========================================================
# QUOTE FORM
# =========================================================

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
                'placeholder': (
                    'e.g. Front brake pad set available '
                    'for collection today.'
                )
            }),
        }


# =========================================================
# REVIEW FORM
# =========================================================

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
                'placeholder': (
                    'Tell us about your experience with the shop...'
                ),
                'rows': 4
            }),
        }


# =========================================================
# SHOP REGISTRATION FORM
# =========================================================

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

        if User.objects.filter(
            username__iexact=username
        ).exists():
            raise forms.ValidationError(
                'This username is already taken. '
                'Please choose another.'
            )

        return username


# =========================================================
# TRACK REQUEST FORM
# =========================================================

class TrackRequestForm(forms.Form):

    customer_name = forms.CharField(
        label='Customer Name',
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter the name used on your request'
        })
    )

    phone_number = forms.CharField(
        label='Phone Number',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Example: 0712345678'
        })
    )

    def clean_customer_name(self):
        customer_name = self.cleaned_data.get(
            'customer_name',
            ''
        ).strip()

        if not customer_name:
            raise forms.ValidationError(
                'Please enter your customer name.'
            )

        return customer_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get(
            'phone_number',
            ''
        )

        cleaned = (
            phone_number
            .replace(' ', '')
            .replace('-', '')
            .replace('(', '')
            .replace(')', '')
        )

        if cleaned.startswith('+27'):
            cleaned = '0' + cleaned[3:]

        elif cleaned.startswith('27'):
            cleaned = '0' + cleaned[2:]

        if not cleaned.isdigit():
            raise forms.ValidationError(
                'Please enter a valid phone number.'
            )

        if len(cleaned) != 10:
            raise forms.ValidationError(
                'Please enter a valid 10-digit South African '
                'phone number, e.g. 071 234 5678.'
            )

        if not cleaned.startswith('0'):
            raise forms.ValidationError(
                'Please enter a valid South African phone number.'
            )

        return cleaned


# =========================================================
# ADMIN NOTIFICATION FORM
# =========================================================

class AdminNotificationForm(forms.Form):

    SEND_TO_CHOICES = [
        ('all', 'All Shops'),
        ('shop', 'Specific Shop'),
    ]

    send_to = forms.ChoiceField(
        choices=SEND_TO_CHOICES
    )

    shop = forms.ModelChoiceField(
        queryset=Shop.objects.filter(
            is_active=True
        ).order_by(
            'shop_name'
        ),
        required=False
    )

    title = forms.CharField(
        max_length=150
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': (
                'Write your notification message...'
            )
        })
    )

    notification_type = forms.ChoiceField(
        choices=[
            ('info', 'Information'),
            ('warning', 'Warning'),
            ('success', 'Success'),
            ('maintenance', 'Maintenance'),
        ]
    )


# =========================================================
# SUPPORT TICKET FORM
# =========================================================

class SupportTicketForm(forms.ModelForm):

    class Meta:
        model = SupportTicket

        fields = [
            'category',
            'subject',
            'message',
        ]

        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': (
                    'Briefly describe the problem'
                )
            }),

            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': (
                    'Describe what happened, what you were trying '
                    'to do, and any error message you saw.'
                )
            }),
        }


class ShopPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter current password"
            }
        )
    )

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new password"
            }
        )
    )

    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm new password"
            }
        )
    )