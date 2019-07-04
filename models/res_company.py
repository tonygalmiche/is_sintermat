# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    is_texte_introduction_devis = fields.Text("Texte introduction devis")


