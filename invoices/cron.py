import datetime
from configparser import ConfigParser
from django.conf import settings
from invoices.models import Invoice

config = ConfigParser(interpolation=None)
config.read(settings.CONFIG_FILE)


def update_invoices_status():
    print("Updating invoices...")
    if config.getint("invoices", "OVERDUE_DAYS") != 0:
        for invoice in Invoice.objects.filter(status=1):
            if (
                invoice.bill_date
                + datetime.timedelta(days=config.getint("invoices", "OVERDUE_DAYS"))
                < datetime.date.today()
            ):
                invoice.status = 2
                invoice.save()
                print(f"Invoice {invoice.invoice_id} marked OVERDUE.")
    print("Update completed!")
