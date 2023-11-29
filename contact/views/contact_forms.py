from typing import Any
from django.shortcuts import (  # type: ignore
    render, get_object_or_404, redirect)
from django.db.models import Q  # type: ignore
from contact.models import Contact
from django.core.paginator import Paginator  # type: ignore
from django import forms
from django.core.exceptions import ValidationError


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name', 'phone',
            )
        
    def clean(self) -> dict[str, Any]:
        cleaned_data = self.cleaned_data
        self.add_error(
            None, 
            ValidationError(
                'Mensagem de erro', code='invalid'
            )
        )
        self.add_error(
            None, 
            ValidationError(
                'Mensagem de erro2', code='invalid'
            )
        )
        return super().clean()


def create(request):
    if request.method == 'POST':
        context = {
            'form': ContactForm(data=request.POST)
        }
        return render(
            request,
            'contact/create.html',
            context
            )
    
    context = {
        'form': ContactForm()
    }
    return render(
        request,
        'contact/create.html',
        context
        )


