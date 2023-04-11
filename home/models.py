from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldRowPanel
from dal import autocomplete
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import InlinePanel, MultiFieldPanel
from home.widgets import ArticleChooser


class HomePage(Page):
    content_panels = [
        MultiFieldPanel(
            [
                InlinePanel("article_source", label="Article", min_num=1),
            ],
            heading="Article(s)",
        ),
    ]


# models.py

class ArticlesOrderable(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey(
        "HomePage", related_name="article_source", blank=True, null=True
    )

    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, blank=True, null=True
    )

    panels = [
        FieldPanel("article", widget=ArticleChooser),
    ]


@register_snippet
class Country(Orderable, ClusterableModel):
    title = models.CharField(max_length=255, blank=False, null=False)

    panels = [
        FieldPanel("title"),
    ]

    def __str__(self):
        """String repr of this class."""
        return self.title

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


@register_snippet
class Article(Orderable, ClusterableModel):
    title = models.CharField(max_length=255, blank=False, null=False)
    countries = models.ManyToManyField("Country", blank=True)

    # If want change view of panels in AdminPanel go to model_admin
    # file and config panel ArticleAdmin!
    panels = [
        FieldPanel("title"),
        FieldRowPanel(
            [
                FieldPanel("countries", widget=autocomplete.ModelSelect2Multiple()),
            ],
            heading="Country(ies)/Continent(s)",
        )
    ]

    def __str__(self):
        """String repr of this class."""
        return self.title

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
