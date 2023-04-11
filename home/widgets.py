from generic_chooser.widgets import AdminChooser
from django.contrib.admin.utils import quote
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


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
