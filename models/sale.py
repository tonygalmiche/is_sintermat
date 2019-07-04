# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    is_conseiller_scientifique_id = fields.Many2one('res.partner', u"Conseillé scientifique")
    is_intitule                   = fields.Char(u"Intitulé")
    is_introduction               = fields.Text(u"Texte d'introduction")
    is_delai_realisation          = fields.Text(u"Délai de réalisation")
    is_condition_paiement         = fields.Text(u"Conditions de paiement particulières")

