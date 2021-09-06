import os
import tempfile
from datetime import date
from io import BytesIO

import pypdftk
from django.conf import settings

from invoices.models import Invoice


def generate_id(partner):
    invoice_id = str(date.today().year) + "-"
    invoice_id += partner.partner_id + "-"
    invoices = [
        int(invoice.invoice_id[-3:])
        for invoice in Invoice.objects.filter(partner=partner)
        if invoice.invoice_id[:4] == str(date.today().year)
    ]

    if invoices:
        invoices.sort()
        invoice_id += f"{(invoices[-1] + 1):03}"
    else:
        invoice_id += "001"
    return invoice_id


def generate_pdf(invoice):
    pdf_invoice = tempfile.NamedTemporaryFile()

    if not os.path.isfile(settings.TEMPLATE_FILE):
        return None

    if invoice.status == 4:
        invoice_date = "VOID"
    elif invoice.bill_date:
        invoice_date = invoice.bill_date.strftime("%m/%d/%Y")
    else:
        invoice_date = "DRAFT"

    items = ""
    hours = ""
    rate = ""
    amount = ""

    for item in invoice.items.all():
        items = items + item.description + "\n"

        if item.hours and item.rate:
            hours += str(item.hours) + "\n"
            rate += "$" + f"{item.rate:,.2f}" + "\n"
        else:
            hours += "\n"
            rate += "\n"

        amount += "$" + f"{item.amount:,.2f}" + "\n"

    invoice_data = {
        "INVOICE_ID": invoice.invoice_id,
        "BILL_DATE": invoice_date,
        "PARTNER": invoice.partner.company,
        "ADDRESS1": invoice.partner.get_address1(),
        "ADDRESS2": invoice.partner.get_address2(),
        "ITEMS": items,
        "HOURS": hours,
        "RATE": rate,
        "AMOUNT": amount,
        "TOTAL": "$" + f"{invoice.get_total():,.2f}",
    }

    pypdftk.fill_form(
        settings.TEMPLATE_FILE, invoice_data, pdf_invoice.name, flatten=True
    )

    stream = BytesIO(pdf_invoice.read())
    pdf_invoice.close()

    return stream.getvalue()
