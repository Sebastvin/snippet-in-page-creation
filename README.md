## Step-by-step guide how to implement creating a Snippet in a Page with using django-autocomplete-light widget

## Requirements

Wagtail 4.1 or higher

## Installation 

[wagtail-generic-chooser](https://github.com/wagtail/wagtail-generic-chooser)

Run: `pip install wagtail-generic-chooser`

[django-autocomplete-light](https://django-autocomplete-light.readthedocs.io/en/master/index.html#)

Run: `pip install django-autocomplete-light`

1. In views extend the basic ModelChooserViewSet that has the create_tab_mixin_class parameter and modify the very appearance of our form, i.e. what it should look like and what fields it should have directly in the selector when created on Page

```python
# views.py

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
```

2. Define chooser for Article model in selector

```python
# widgets.py

class ArticleChooser(AdminChooser):
    def __init__(self, *args, **kwargs):
        from home.models import Article

        self.model = Article
        super().__init__(*args, **kwargs)

    choose_one_text = _("Choose a article")
    choose_another_text = _("Choose another article")
    link_to_chosen_text = _("Edit this article")
    model = None
    choose_modal_url_name = "article_chooser:choose"
    icon = "user"
```

3. Use of a custom widget

```python
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
```

4. Registration view

```python
# wagtail_hooks.py

@hooks.register("register_admin_viewset")
def register_article_chooser_viewset():
    return ArticleChooserViewSet("article_chooser", url_prefix="article-chooser")
```

5. Add global css and js to django autocomplete light, otherwise the files will not be downloaded in the selector making the widget not work

```python
# wagtail_hooks.py

@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/custom.css to the admin."""
    return format_html(
        """
        <link rel="stylesheet" href="{}">
        <link rel="stylesheet" href="{}">
        <link rel="stylesheet" href="{}">
        """,
        static("autocomplete_light/select2.css"),
        static("admin/css/autocomplete.css"),
        static("admin/css/vendor/select2/select2.css"),
    )


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    """Add /static/css/custom.js to the admin."""
    return format_html(
        """
        <script src="{}"></script>
        <script src="{}"></script>
        <script src="{}"></script>
        """,
        static("autocomplete_light/select2.js"),
        static("autocomplete_light/autocomplete_light.js"),
        static("admin/js/vendor/select2/select2.full.js"),
    )
```

Note. These are just selected pieces of code from the repository