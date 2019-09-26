# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"


    @api.depends('date_order')
    def _compute_is_confirmation_date(self):
        for obj in self:
            obj.is_confirmation_date = str(obj.confirmation_date)

    is_confirmation_date          = fields.Date(u"Date de confirmation", compute='_compute_is_confirmation_date', readonly=True, store=False)
    is_conseiller_scientifique_id = fields.Many2one('res.partner', u"Conseillé scientifique")
    is_intitule                   = fields.Char(u"Intitulé")
    is_introduction               = fields.Text(u"Texte d'introduction")
    is_delai_realisation          = fields.Text(u"Délai de réalisation")
    is_condition_paiement         = fields.Text(u"Conditions de paiement particulières")



