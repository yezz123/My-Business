import datetime
from django.db.models import Q
from invoices.models import Invoice


def review_invoices_processor(request):
    invoices = Invoice.objects.filter(Q(status=2) | Q(status=0) | Q(status=1))
    return {"invoices": invoices}
