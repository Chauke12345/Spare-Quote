from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import uuid


class Shop(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shop_profile'
    )

    shop_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=150)
    address = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    # SHOP PACKAGE OPTIONS
    marketplace_enabled = models.BooleanField(
        default=True
    )

    private_qr_enabled = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name



class PartRequest(models.Model):

    public_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    # =========================================================
    # STATUS OPTIONS
    # =========================================================

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('quoted', 'Quoted'),
        ('accepted', 'Accepted'),
        ('expired', 'Expired'),
        ('completed', 'Completed'),
    ]

    # =========================================================
    # REQUEST SOURCE OPTIONS
    # =========================================================

    REQUEST_SOURCE_CHOICES = [
        ('marketplace', 'Marketplace'),
        ('mechanic_qr', 'Mechanic QR'),
        ('shop_qr', 'Shop QR'),
    ]

    # =========================================================
    # CUSTOMER DETAILS
    # =========================================================

    customer_name = models.CharField(
        max_length=100
    )

    phone_number = models.CharField(
        max_length=20
    )

    location = models.CharField(
        max_length=150
    )

    # =========================================================
    # VEHICLE DETAILS
    # =========================================================

    vin_number = models.CharField(
        max_length=17,
        blank=True,
        help_text="17-character Vehicle Identification Number"
    )

    vehicle_make = models.CharField(
        max_length=100
    )

    vehicle_model = models.CharField(
        max_length=100
    )

    vehicle_year = models.PositiveIntegerField()

    engine_details = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: 1.6 petrol, 2.0 TDI, 1.4 TSI"
    )

    # =========================================================
    # PART DETAILS
    # =========================================================

    part_name = models.CharField(
        max_length=200
    )

    part_description = models.TextField(
        blank=True,
        help_text="Describe the part or problem"
    )

    part_image = models.ImageField(
        upload_to='part_requests/',
        blank=True,
        null=True,
        help_text="Upload a photo of the part if available"
    )

    # =========================================================
    # REQUEST STATUS
    # =========================================================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # =========================================================
    # REQUEST ROUND
    # =========================================================

    request_round = models.PositiveIntegerField(
        default=1
    )

    # =========================================================
    # REQUEST SOURCE
    # =========================================================

    request_source = models.CharField(
        max_length=20,
        choices=REQUEST_SOURCE_CHOICES,
        default='marketplace'
    )

    # Used only when the request comes through
    # a specific shop's private QR code.
    source_shop = models.ForeignKey(
        Shop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='private_requests'
    )

    # =========================================================
    # DATE CREATED
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =========================================================
    # WHATSAPP NUMBER
    # =========================================================

    @property
    def whatsapp_number(self):
        number = (
            self.phone_number
            .replace(' ', '')
            .replace('-', '')
            .replace('(', '')
            .replace(')', '')
            .replace('+', '')
        )

        # Convert local SA number:
        # 0712345678 -> 27712345678
        if number.startswith('0'):
            number = '27' + number[1:]

        return number

    # =========================================================
    # DISPLAY NAME
    # =========================================================

    def __str__(self):
        return (
            f"Request #{self.id} - "
            f"{self.vehicle_make} {self.vehicle_model} - "
            f"{self.part_name}"
        )

class Quote(models.Model):

    part_request = models.ForeignKey(
        PartRequest,
        on_delete=models.CASCADE,
        related_name='quotes'
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='quotes',
        null=True,
        blank=True
    )

    shop_name = models.CharField(
        max_length=150,
        blank=True
    )

    shop_phone = models.CharField(
        max_length=20,
        blank=True
    )

    is_accepted = models.BooleanField(
        default=False
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    availability = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: In stock, 2 days, Order required"
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional information about the quote"
    )

    # REQUEST ROUND THIS QUOTE BELONGS TO
    quote_round = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['part_request', 'shop'],
                name='unique_shop_quote_per_request'
            ),

            models.UniqueConstraint(
                fields=['part_request'],
                condition=Q(is_accepted=True),
                name='one_accepted_quote_per_request'
            ),
        ]

    def save(self, *args, **kwargs):

        if self.shop:
            self.shop_name = self.shop.shop_name
            self.shop_phone = self.shop.phone_number

        super().save(*args, **kwargs)

        if self.part_request.status == 'pending':
            self.part_request.status = 'quoted'
            self.part_request.save()

    def __str__(self):
        return f"{self.shop_name} - R{self.price}"


class Review(models.Model):

    part_request = models.OneToOneField(
        PartRequest,
        on_delete=models.CASCADE,
        related_name='review'
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.shop.shop_name} - "
            f"{self.rating}/5"
        )

class Notification(models.Model):

    NOTIFICATION_TYPE_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('maintenance', 'Maintenance'),
    ]

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=150
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE_CHOICES,
        default='info'
    )

    is_global = models.BooleanField(
        default=False,
        help_text='If enabled, this notification is intended for all shops.'
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        if self.is_global:
            return f"Global - {self.title}"

        if self.shop:
            return f"{self.shop.shop_name} - {self.title}"

        return self.title

class NotificationRead(models.Model):

    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='read_receipts'
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='notification_reads'
    )

    read_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'notification',
                    'shop'
                ],
                name='unique_notification_read_per_shop'
            )
        ]

    def __str__(self):
        return (
            f"{self.shop.shop_name} - "
            f"{self.notification.title}"
        )
    
class SupportTicket(models.Model):

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    CATEGORY_CHOICES = [
        ('technical', 'Technical Problem'),
        ('account', 'Account / Access'),
        ('quotation', 'Quotation Problem'),
        ('request', 'Customer Request Problem'),
        ('billing', 'Billing / Subscription'),
        ('other', 'Other'),
    ]

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='support_tickets'
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='technical'
    )

    subject = models.CharField(
        max_length=150
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.shop.shop_name} - {self.subject}"