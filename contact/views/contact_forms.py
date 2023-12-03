from django.shortcuts import (  # type: ignore
    render, redirect, get_object_or_404)
from contact.forms import ContactForm
from django.urls import reverse  # type: ignore
from contact.models import Contact
from django.contrib.auth.decorators import login_required  # type: ignore
from django.contrib import messages  # type: ignore


@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('contact:create')
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        context = {
            'form': form,
            'form_action': form_action
        }
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            messages.success(request, 'Contato registrado')
            return redirect('contact:update', contact_id=contact.pk)

        return render(
            request,
            'contact/create.html',
            context
            )

    context = {
        'form': ContactForm(),
        'form_action': form_action
    }
    return render(
        request,
        'contact/create.html',
        context
        )


@login_required(login_url='contact:login')
def update(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id,
                                show=True, owner=request.user)
    form_action = reverse('contact:update', args=(contact_id,))
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        context = {
            'form': form,
            'form_action': form_action
        }
        if form.is_valid():
            contact = form.save()
            messages.success(request, 'Contato atualizado')
            return redirect('contact:update', contact_id=contact.pk)

        return render(
            request,
            'contact/create.html',
            context
            )

    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action
    }
    return render(
        request,
        'contact/create.html',
        context
        )


@login_required(login_url='contact:login')
def delete(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id,
                                show=True, owner=request.user)
    confirmation = request.POST.get('confirmation', 'no')
    print(confirmation)
    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')
    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
        }
    )
