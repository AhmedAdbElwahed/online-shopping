from io import BytesIO
from celery import shared_task

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from xhtml2pdf import pisa

from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
        Task to send an e-mail notification when an order is
        successfully paid.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'My Shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'admin@myshop.com',
                         [order.email])
    html = render_to_string('order/pdf.html', {'order': order})
    out = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=out)
    if pisa_status.err:
        raise RuntimeError(f'We had some errors converting html to pdf')

    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'applications/pdf')
    email.send()
