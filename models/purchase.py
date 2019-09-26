# -*- coding: utf-8 -*-
from odoo import api, fields, models, _



class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends('date_order')
    def _compute_is_date_order(self):
        for obj in self:
            obj.is_date_order = str(obj.date_order)

    is_date_order = fields.Date(u"Date commande", compute='_compute_is_date_order', readonly=True, store=False)


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends('date_planned')
    def _compute_is_date_prevue(self):
        for obj in self:
            obj.is_date_prevue = str(obj.date_planned)

    is_date_prevue = fields.Date(u"Date prévue", compute='_compute_is_date_prevue', readonly=True, store=False)




