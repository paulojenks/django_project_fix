from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from . import models
from . import forms


def menu_list(request):
    menu_lists = models.Menu.objects.all().prefetch_related('items')
    menu_lists = menu_lists.order_by('-expiration_date')
    paginator = Paginator(menu_lists, 5)
    page = request.GET.get('page')
    menus = paginator.get_page(page)
    return render(request, 'menu/menu_list.html', {'menus': menus})


def menu_detail(request, pk):
    menu = get_object_or_404(models.Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def menu_new(request):
    if request.method == "POST":
        form = forms.MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect(reverse('menu:menu_detail', kwargs={'pk': menu.pk}))
    else:
        form = forms.MenuForm()
    return render(request, 'menu/menu_new.html', {'form': form})


def menu_edit(request, pk):
    menu = get_object_or_404(models.Menu, pk=pk)
    if request.method == "POST":
        edit_form = forms.MenuForm(instance=menu, data=request.POST)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Changes Saved!")
            return redirect(reverse('menu:menu_detail', kwargs={'pk':menu.pk}))
    else:
        edit_form = forms.MenuForm(instance=menu)
    return render(request, 'menu/menu_edit.html', {'edit_form': edit_form})


def item_detail(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    return render(request, 'menu/item_detail.html', {'item': item})


def item_list(request):
    items_list = models.Item.objects.all().order_by('name')
    paginator = Paginator(items_list, 5)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return render(request, 'menu/item_list.html', {'items': items})

