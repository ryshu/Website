import csv
import json
from collections import Counter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from . import forms
from . import models
from events.models import Inscription


@login_required
def index(request):
    context = {
        'history': models.BuyingHistory.objects.filter(user=request.user).order_by('date').select_related('user__profile').select_related('seller__profile').all().reverse()
    }

    return render(request, 'shop/index.html', context)


@permission_required('shop.sell_product')
def sells(request):
    if request.method == 'OPTIONS':
        req = json.loads(request.read().decode())
        try:
            user = User.objects.get(id=req.get('uid'))
        except User.DoesNotExist:
            return JsonResponse({'error': 'L\'utilisateur n\'existe pas.'})

        item_type = req.get('type')

        try:
            if item_type == 'pack':
                item = models.Packs.objects.get(id=req.get('pid'))
            else:
                item = models.Product.objects.get(id=req.get('pid'))
        except models.Product.DoesNotExists:
            return JsonResponse({'error': 'Le produit selectionné n\'existe pas.'})

        if req.get('payment_mean') not in [p[0] for p in models.MEANS_OF_PAYMENT]:
            return JsonResponse({'error': 'Le moyen de paiement n\'est pas valide'})

        item.buy(user, req.get('payment_mean'), request.user)

        return JsonResponse({'error': None, 'name': item.name, 'user': str(user.profile)})
    else:
        context = {
            'products': models.Product.objects.filter(enabled=True).all(),
            'packs': models.Packs.objects.filter(enabled=True).all(),
        }
        return render(request, 'shop/sell.html', context)


@permission_required('shop.view_history')
def history(request):
    history = models.BuyingHistory.objects.select_related('user__profile').select_related('seller__profile').select_related('pack').select_related('product').order_by('date').all().reverse()
    paginator = Paginator(history, 25)

    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    context = {
        'history': response
    }

    return render(request, 'shop/history.html', context)


@permission_required('shop.view_history')
def history_export_csv(request):

    history = models.BuyingHistory.objects.select_related('user').select_related('seller__profile').select_related('pack').select_related('product').order_by('date').all().reverse()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="historique.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Produit', 'Type', 'Prix', 'Moyen de paiment', 'Prenom', 'Nom', 'Mail', 'Vendeur'])

    for h in history:
        if h.type == 'pack':
            item = h.pack
        else:
            item = h.product

        writer.writerow([
            h.date.strftime("%d/%m/%Y %H:%M"),
            item.name,
            h.type,
            item.price,
            h.payment_mean,
            h.user.first_name,
            h.user.last_name,
            h.user.email,
            str(h.seller.profile) if h.seller else "",
        ])

    return response


@login_required
def history_detail(request, hid):
    ctx = {
        'item': get_object_or_404(models.BuyingHistory, pk=hid),
    }
    return render(request, 'shop/history_detail.html', ctx)


@permission_required('shop.delete_buyinghistory')
def history_delete(request, hid):
    entry = get_object_or_404(models.BuyingHistory, id=hid)

    with transaction.atomic():
        events = [p.event for p in entry.get_products() if p.event]
        events_cout = Counter(events)

        for event in events:
            if entry.count_event_participations(event, entry.user) <= events_cout[event]:
                Inscription.objects.filter(user=entry.user, event=event).delete()

        entry.delete()
    return redirect(reverse('shop:history'))


@permission_required('shop.manage_product')
def admin(request):

    context = {
        'products': models.Product.objects.filter(enabled=True).all(),
        'packs': models.Packs.objects.filter(enabled=True).all()
    }

    return render(request, 'shop/admin.html', context)


@permission_required('shop.manage_product')
def product_add(request):
    if request.method == "POST":
        form = forms.ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('shop:admin'))
    else:
        form = forms.ProductForm()

    context = {
        'form': form.as_p()
    }

    return render(request, 'shop/product_add.html', context)


@permission_required('shop.manage_product')
def product_delete(request, pid):
    product = get_object_or_404(models.Product, id=pid)
    product.enabled = False
    product.save()
    return redirect(reverse('shop:admin'))


@permission_required('shop.manage_product')
def product_edit(request, pid):
    product = get_object_or_404(models.Product, id=pid)

    if request.method == "POST":
        old_event = product.event
        form = forms.ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            product.update_event_registrations(old_event)
            return redirect(reverse('shop:admin'))
    else:
        form = forms.ProductForm(instance=product)

    context = {
        'form': form.as_p(),
        'product': product,
    }

    return render(request, 'shop/product_edit.html', context)


@permission_required('shop.manage_product')
def pack_add(request):
    if request.method == "POST":
        form = forms.PackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('shop:admin'))
    else:
        form = forms.PackForm()

    context = {
        'form': form
    }

    return render(request, 'shop/pack_add.html', context)


@permission_required('shop.manage_product')
def pack_edit(request, pid):
    pack = get_object_or_404(models.Packs, id=pid)
    if request.method == "POST":
        old_products = list(pack.products.filter(enabled=True).all())
        form = forms.PackForm(request.POST, instance=pack)
        if form.is_valid():
            form.save()
            pack.update_event_registrations(old_products)
            return redirect(reverse('shop:admin'))
    else:
        form = forms.PackForm(instance=pack)

    context = {
        'form': form,
        'pack': pack,
    }

    return render(request, 'shop/pack_edit.html', context)


@permission_required('shop.manage_product')
def pack_delete(request, pid):
    pack = get_object_or_404(models.Packs, id=pid)
    pack.enabled = False
    pack.save()
    return redirect(reverse('shop:admin'))
