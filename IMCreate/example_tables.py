import django_tables2 as tables
from .models import User

class ExampleTable(tables.Table):
    # property_name = tables.Column(verbose_name="Desired Name", orderable=False,)

    class Meta:
        model = User
        template_name = "django_tables2/bootstrap5.html"
        fields = ("other_column_names",)
