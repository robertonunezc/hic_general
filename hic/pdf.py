import pdfkit
from django.template.loader import get_template
from django.template import Context
from hic.settings import HIC_HOST, HIC_DIR, HIC_LOCAL_DIR

import os

import random


def get_html_historia(historia_clinica):
    template = get_template("pacientes/historia_clinica_pdf.html")
    context = {
        "STATIC_URL": "{}/static/".format(HIC_HOST),
        "historia_clinica": historia_clinica,
    }
    html = template.render(context)
    return html


def get_historia_pdf(historia):
    """
    :param ticket: recibe un objeto TicketDapp
    :return: file con informacion de pdf
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.25in',
        'margin-right': '0.25in',
        'margin-bottom': '0.25in',
        'margin-left': '0.25in',
        'encoding': "UTF-8",
        'page-width': "1498px",
        'orientation': "Portrait",
    }

    html = get_html_historia(historia_clinica=historia)

    #bin_path = '/home/h3dx0/Programas/wkhtmltox/bin/wkhtmltopdf'
    bin_path = '/home/h3dx0/python_projects/hic_cuba/wkhtmltopdf/bin/wkhtmltopdf'
    bin_path = '/home/h3dx0/python_projects/hic_cuba/wkhtmltox/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=bytes(bin_path, 'utf-8'))

    pdf = pdfkit.from_string("{}".format(html), False, options=options, configuration=config)
    return pdf

