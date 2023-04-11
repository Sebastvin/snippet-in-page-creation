from django.utils.translation import gettext_lazy as _
from django.contrib.admin.utils import quote
from django.urls import reverse
from home.models import Article
from generic_chooser.views import (
    ModelChooserMixin,
    ModelChooserViewSet,
)
from dal import autocomplete
from django import forms


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "countries",
        ]
        widgets = {
            "countries": autocomplete.ModelSelect2Multiple(),
        }


class ArticleChooserViewSet(ModelChooserViewSet):
    icon = "plus"
    model = Article
    page_title = _("Choose a article")
    per_page = 20
    order_by = "-title"

    form_class = ArticleForm
