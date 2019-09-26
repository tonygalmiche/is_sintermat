# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"


    @api.depends('date_order')
    def _compute_is_confirmation_date(self):
        for obj in self:
            obj.is_confirmation_date = str(obj.confirmation_date)


    @api.depends('is_phase_id','is_phase_id.probabilite')
    def _compute_is_phase_id(self):
        for obj in self:
            obj.is_probabilite = obj.is_phase_id.probabilite


    @api.depends('amount_untaxed','is_phase_id','is_phase_id.probabilite')
    def _compute_is_ca_pondere(self):
        for obj in self:
            obj.is_ca_pondere = obj.amount_untaxed*obj.is_phase_id.probabilite/100


    is_confirmation_date          = fields.Date(u"Date de confirmation", compute='_compute_is_confirmation_date', readonly=True, store=False)
    is_date_decisionnelle         = fields.Date(u"Date décisionnelle")
    is_phase_id                   = fields.Many2one('is.phase', 'Phase')
    is_probabilite                = fields.Integer(u"Probabilité (%)"  , compute='_compute_is_phase_id', readonly=True, store=True)
    is_ca_pondere                 = fields.Float(u"CA Pondéré HT"  , compute='_compute_is_ca_pondere', readonly=True, store=True)
    is_conseiller_scientifique_id = fields.Many2one('res.partner', u"Conseillé scientifique")
    is_intitule                   = fields.Char(u"Intitulé")
    is_introduction               = fields.Text(u"Texte d'introduction")
    is_delai_realisation          = fields.Text(u"Délai de réalisation")
    is_condition_paiement         = fields.Text(u"Conditions de paiement particulières")



