from wagtail import hooks
from home.views.views import ArticleChooserViewSet
from django.templatetags.static import static
from django.utils.html import format_html


# wagtail_hooks.py

@hooks.register("register_admin_viewset")
def register_article_chooser_viewset():
    return ArticleChooserViewSet("article_chooser", url_prefix="article-chooser")

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
