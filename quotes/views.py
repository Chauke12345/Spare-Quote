from django.shortcuts import render, redirect, get_object_or_404

from django.views.decorators.http import require_POST

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from datetime import timedelta

from django.utils import timezone

from django.db import transaction

from .forms import PartRequestForm, QuoteForm, ShopRegistrationForm

from .models import PartRequest, Quote, Shop


# =========================================================
# CUSTOMER - REQUEST A PART
# =========================================================
def request_part(request):
    if request.method == 'POST':
        form = PartRequestForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            part_request = form.save()

            return redirect(
                'request_detail',
                public_id=part_request.public_id
            )

    else:
        form = PartRequestForm()

    return render(
        request,
        'quotes/request_part.html',
        {
            'form': form
        }
    )
# =========================================================
# REQUEST SUCCESS
# =========================================================

def request_success(request):
    return render(
        request,
        'quotes/request_success.html'
    )


# =========================================================
# CUSTOMER - REQUEST DETAILS
# =========================================================

def request_detail(request, public_id):
    part_request = get_object_or_404(
        PartRequest,
        public_id=public_id
    )

    # Check whether the current 24-hour round has expired
    expiry_time = timezone.now() - timedelta(hours=24)

    if (
        part_request.status in ['pending', 'quoted']
        and part_request.created_at < expiry_time
    ):
        part_request.status = 'expired'
        part_request.save()

    return render(
        request,
        'quotes/request_detail.html',
        {
            'part_request': part_request,
            'quotes': part_request.quotes.all(),
        }
    )


# =========================================================
# CUSTOMER - ACCEPT QUOTE
# =========================================================
# =========================================================
# CUSTOMER - ACCEPT QUOTE
# =========================================================
@require_POST
def accept_quote(request, public_id, quote_id):

    with transaction.atomic():

        part_request = get_object_or_404(
            PartRequest.objects.select_for_update(),
            public_id=public_id
        )

        quote = get_object_or_404(
            Quote,
            id=quote_id,
            part_request=part_request
        )

        # Check whether request has expired
        expiry_time = timezone.now() - timedelta(hours=24)

        if (
            part_request.status in ['pending', 'quoted']
            and part_request.created_at < expiry_time
        ):
            part_request.status = 'expired'
            part_request.save()

        # Block acceptance after expiry or completion
        if part_request.status in ['expired', 'completed']:
            return redirect(
                'request_detail',
                public_id=part_request.public_id
            )

        # Block old-round quotations
        if quote.quote_round != part_request.request_round:
            return redirect(
                'request_detail',
                public_id=part_request.public_id
            )

        # If a quote is already accepted,
        # do not allow another one
        existing_accepted_quote = Quote.objects.filter(
            part_request=part_request,
            is_accepted=True
        ).first()

        if existing_accepted_quote:

            if part_request.status != 'accepted':
                part_request.status = 'accepted'
                part_request.save()

            return redirect(
                'request_detail',
                public_id=part_request.public_id
            )

        # Accept this quote
        quote.is_accepted = True
        quote.save()

        part_request.status = 'accepted'
        part_request.save()

    return redirect(
        'request_detail',
        public_id=part_request.public_id
    )
# =========================================================
# SHOP DASHBOARD
# =========================================================

@login_required(login_url='shop_login')
def shop_dashboard(request):
    shop = get_object_or_404(
        Shop,
        user=request.user
    )

    # Expire requests whose current round is older than 24 hours
    expiry_time = timezone.now() - timedelta(hours=24)

    PartRequest.objects.filter(
        status__in=['pending', 'quoted'],
        created_at__lt=expiry_time
    ).update(
        status='expired'
    )

    # Active requests
    open_requests = PartRequest.objects.filter(
        status__in=['pending', 'quoted']
    ).order_by(
        '-created_at'
    )

    # -----------------------------------------------------
    # QUOTES SUBMITTED IN CURRENT ROUND
    # -----------------------------------------------------

    current_round_quote_ids = []

    update_quote_request_ids = []

    for part_request in open_requests:

        existing_quote = Quote.objects.filter(
            part_request=part_request,
            shop=shop
        ).first()

        if existing_quote:

            # Shop has already submitted/updated in this round
            if (
                existing_quote.quote_round
                == part_request.request_round
            ):
                current_round_quote_ids.append(
                    part_request.id
                )

            # Shop quoted in an older round
            elif (
                existing_quote.quote_round
                < part_request.request_round
            ):
                update_quote_request_ids.append(
                    part_request.id
                )

    # Keep this name for the current dashboard template
    quoted_request_ids = current_round_quote_ids

    # -----------------------------------------------------
    # NOTIFICATION COUNT
    # -----------------------------------------------------

    # Anything not quoted in the current round
    # needs supplier attention.
    new_request_count = open_requests.exclude(
        id__in=current_round_quote_ids
    ).count()

    # =====================================================
    # REQUEST HISTORY FILTER
    # =====================================================

    history_filter = request.GET.get(
        'history',
        'today'
    )

    request_history = PartRequest.objects.filter(
        status__in=[
            'accepted',
            'expired',
            'completed'
        ],
        quotes__shop=shop
    ).distinct()

    if history_filter == 'today':

        request_history = request_history.filter(
            created_at__date=timezone.localdate()
        )

    elif history_filter == '7':

        request_history = request_history.filter(
            created_at__gte=(
                timezone.now()
                - timedelta(days=7)
            )
        )

    elif history_filter == '30':

        request_history = request_history.filter(
            created_at__gte=(
                timezone.now()
                - timedelta(days=30)
            )
        )

    elif history_filter == 'all':
        pass

    else:
        history_filter = 'today'

        request_history = request_history.filter(
            created_at__date=timezone.localdate()
        )

    request_history = request_history.order_by(
        '-created_at'
    )

    return render(
        request,
        'quotes/shop_dashboard.html',
        {
            'open_requests': open_requests,
            'request_history': request_history,

            'quoted_request_ids': quoted_request_ids,

            'update_quote_request_ids':
                update_quote_request_ids,

            'new_request_count':
                new_request_count,

            'history_filter':
                history_filter,
        }
    )


# =========================================================
# SHOP - SUBMIT / UPDATE QUOTE
# =========================================================

@login_required(login_url='shop_login')
def submit_quote(request, request_id):
    part_request = get_object_or_404(
        PartRequest,
        id=request_id
    )

    # Check whether current round has expired
    expiry_time = timezone.now() - timedelta(hours=24)

    if (
        part_request.status in ['pending', 'quoted']
        and part_request.created_at < expiry_time
    ):
        part_request.status = 'expired'
        part_request.save()

    # Block quoting on closed or expired requests
    if part_request.status in [
        'accepted',
        'expired',
        'completed'
    ]:
        return redirect(
            'shop_dashboard'
        )

    shop = get_object_or_404(
        Shop,
        user=request.user
    )

    # Check whether this shop already has a quote
    existing_quote = Quote.objects.filter(
        part_request=part_request,
        shop=shop
    ).first()

    # -----------------------------------------------------
    # ALREADY QUOTED IN CURRENT ROUND
    # -----------------------------------------------------

    if (
        existing_quote
        and existing_quote.quote_round
        == part_request.request_round
    ):
        return redirect(
            'shop_dashboard'
        )

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    if request.method == 'POST':

        # Existing old-round quote:
        # update the same quote instead of creating another.
        if existing_quote:

            form = QuoteForm(
                request.POST,
                instance=existing_quote
            )

        else:

            form = QuoteForm(
                request.POST
            )

        if form.is_valid():

            quote = form.save(
                commit=False
            )

            quote.part_request = part_request
            quote.shop = shop

            # Mark quote as confirmed for current round
            quote.quote_round = (
                part_request.request_round
            )

            quote.save()

            return redirect(
                'shop_dashboard'
            )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    else:

        # Pre-fill old quote so supplier can change
        # price, stock and notes.
        if existing_quote:

            form = QuoteForm(
                instance=existing_quote
            )

        else:

            form = QuoteForm()

    return render(
        request,
        'quotes/submit_quote.html',
        {
            'form': form,
            'part_request': part_request,
            'shop': shop,

            # Template can use this to display
            # "Update Quote" instead of "Send Quote"
            'is_update': bool(existing_quote),
        }
    )


# =========================================================
# SHOP REGISTRATION
# =========================================================
def shop_register(request):
    if request.method == 'POST':

        form = ShopRegistrationForm(
            request.POST
        )

        if form.is_valid():

            username = form.cleaned_data[
                'username'
            ]

            password = form.cleaned_data[
                'password'
            ]

            shop_name = form.cleaned_data[
                'shop_name'
            ]

            phone_number = form.cleaned_data[
                'phone_number'
            ]

            email = form.cleaned_data[
                'email'
            ]

            location = form.cleaned_data[
                'location'
            ]

            address = form.cleaned_data[
                'address'
            ]

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            Shop.objects.create(
                user=user,
                shop_name=shop_name,
                phone_number=phone_number,
                email=email,
                location=location,
                address=address
            )

            # Log the new shop in immediately
            login(
                request,
                user
            )

            return redirect(
                'shop_dashboard'
            )

    else:
        form = ShopRegistrationForm()

    return render(
        request,
        'quotes/shop_register.html',
        {
            'form': form
        }
    )

# =========================================================
# SHOP LOGIN
# =========================================================

def shop_login(request):
    error_message = None

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if hasattr(
                user,
                'shop_profile'
            ):
                login(
                    request,
                    user
                )

                return redirect(
                    'shop_dashboard'
                )

            error_message = (
                'This account is not '
                'registered as a shop.'
            )

        else:
            error_message = (
                'Invalid username or password.'
            )

    return render(
        request,
        'quotes/shop_login.html',
        {
            'error_message':
                error_message
        }
    )


# =========================================================
# SHOP LOGOUT
# =========================================================

def shop_logout(request):
    logout(request)

    return redirect(
        'shop_login'
    )


# =========================================================
# CUSTOMER - REOPEN REQUEST
# =========================================================
@require_POST
def reopen_request(request, public_id):
    part_request = get_object_or_404(
        PartRequest,
        public_id=public_id
    )

    # Only expired requests can be reopened
    if part_request.status != 'expired':
        return redirect(
            'request_detail',
            public_id=part_request.public_id
        )

    # Start next round
    part_request.request_round += 1

    # If previous quotes exist, request remains quoted.
    # Otherwise it becomes pending again.
    if part_request.quotes.exists():
        part_request.status = 'quoted'
    else:
        part_request.status = 'pending'

    # Start a fresh 24-hour window
    part_request.created_at = timezone.now()

    part_request.save()

    return redirect(
        'request_detail',
        public_id=part_request.public_id
    )