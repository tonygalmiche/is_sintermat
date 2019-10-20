# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import base64


class IsFicheReportingGraphique(models.Model):
    _name = 'is.fiche.reporting.graphique'
    _order='mois'

    fiche_id    = fields.Many2one('is.fiche.reporting', 'Fiche reporting', required=True, ondelete='cascade', readonly=True)
    mois        = fields.Char('Mois')
    prevision   = fields.Float(u'Prévision', digits=(12,2))
    realise     = fields.Float(u'Réalisé'  , digits=(12,2))
    cumul       = fields.Float(u'Cumul'    , digits=(12,2))


class IsFicheReporting(models.Model):
    _name = 'is.fiche.reporting'
    _description = u"Fiche reporting Comité stratégique"
    _order = 'name desc'

    name                  = fields.Char("N°", readonly=True, index=True)
    date_debut            = fields.Date(u"Date de début", required=True)
    date_fin              = fields.Date("Date de fin", required=True)
    realise               = fields.Text("Réalisé")
    objectif_debut        = fields.Integer("Objectif de début (k€)")
    objectif_fin          = fields.Integer("Objectif de fin (k€)")
    graphique             = fields.Binary('Graphique')
    photo_rh              = fields.Binary('Photo RH')
    nouveaux_arrivants    = fields.Text("Nouveaux arrivants")
    vie_sintermat_gauche  = fields.Text("Vie de Sintermat (gauche)")
    vie_sintermat_droite  = fields.Text("Vie de Sintermat (droite)")
    destinataire_mail_ids = fields.Many2many("res.users", "is_fiche_reporting_users_rel", "fiche_id", "user_id", "Destinataire du mail")
    donnees_graphique_ids = fields.One2many('is.fiche.reporting.graphique', 'fiche_id', u"Données du graphique")
    attachment_ids        = fields.Many2many('ir.attachment', 'is_fiche_reporting_attachment_rel', 'fiche_id', 'attachment_id', string='Fiche reporting')


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('is.fiche.reporting')
        res = super(IsFicheReporting, self).create(vals)
        return res


    @api.multi
    def get_commandes(self):
        filtre=[('state','not in',['cancel'])]
        commandes = self.env['sale.order'].search(filtre,limit=10,order='id desc')
        return commandes


    @api.multi
    def get_realise(self, date_debut,date_fin):
        cr = self._cr
        for obj in self:
            SQL="""
                SELECT sum(amount_untaxed)
                FROM sale_order
                WHERE 
                    confirmation_date>='"""+str(date_debut)+"""' and
                    confirmation_date<'"""+str(date_fin)+"""' and
                    state not in ('cancel')
            """
            cr.execute(SQL)
            rows = cr.fetchall()
            realise = 0
            for row in rows:
                realise = row[0]
            return realise


    @api.multi
    def get_destinataires(self):
        mails=[]
        for obj in self:
            for dest in obj.destinataire_mail_ids:
                mails.append(dest.partner_id.email)
        mail=','.join(mails)
        return mail


    @api.multi
    def envoyer_mail_cron(self):
        fiche = self.env['is.fiche.reporting'].search([])[0]
        fiche.envoyer_mail()


    @api.multi
    def envoyer_mail(self):
        for obj in self:

            #** Enregistrer le PDF en piece jointe *****************************
            obj.attachment_ids.unlink()
            report = self.env['ir.actions.report'].search([('report_name', '=', 'is_sintermat.is_fiche_reporting_report')])[0]
            pdf = report.render_qweb_pdf([obj.id])
            datas = base64.b64encode(pdf[0])
            name='Fiche reporting.pdf'
            vals = {
                'name':        name,
                'datas_fname': name,
                'type':        'binary',
                'res_model':   'is.fiche.reporting',
                'res_id':      obj.id,
                'datas':       datas,
            }
            attachment = self.env['ir.attachment'].create(vals)
            vals={
                'attachment_ids': [(4, attachment.id)],
            }
            obj.write(vals)
            #*******************************************************************


            # Mails aux destinataires (ARS, CD..) avec pièce jointe ************
            template = self.env.ref('is_sintermat.is_fiche_reporting_mail_template', False)
            # Ajout des pièces jointes au modèle ***********************
            template.write({'attachment_ids': [(6, 0, [attachment.id])]})
            template.send_mail(obj.id, force_send=True, raise_exception=True)
            # Suppression des pièces jointes du modèle
            template.write({'attachment_ids': [(6, 0, [])]})


    @api.multi
    def actualiser(self, vals):
        for obj in self:

            date_debut = obj.date_debut
            date_fin   = obj.date_fin
            if date_fin>date_debut:
                days       = obj.date_debut.day - 1
                debut_mois = obj.date_debut - timedelta(days=days)
                mois       = debut_mois
                obj.donnees_graphique_ids.unlink()
                nb_mois = 0
                while mois < date_fin:
                    mois = mois + relativedelta(months=+1)
                    nb_mois+=1
                if nb_mois>1:
                    prevision = obj.objectif_debut
                    delta = (obj.objectif_fin-obj.objectif_debut)/(nb_mois-1)
                    mois = debut_mois
                    fin_mois = debut_mois
                    cumul = 0
                    while mois < date_fin:
                        fin_mois = fin_mois + relativedelta(months=+1)
                        realise = self.get_realise(mois,fin_mois) or 0
                        cumul += realise
                        vals={
                            'fiche_id'  : obj.id,
                            'mois'      : mois.strftime('%m/%y'),
                            'prevision' : prevision,
                            'realise'   : realise/1000.0,
                            'cumul'     : cumul/1000.0,
                        }
                        self.env['is.fiche.reporting.graphique'].create(vals)
                        prevision = prevision + delta
                        mois = mois + relativedelta(months=+1)

            #** Création du graphique ******************************************
            plt.rcParams.update({'font.size': 22})
            width = .35 # width of a bar
            prevision = []
            realise   = []
            cumul     = []
            labels    = []
            for row in obj.donnees_graphique_ids:
                prevision.append(row.prevision)
                realise.append(row.realise)
                cumul.append(row.cumul)
                labels.append(row.mois)
            m1_t = pd.DataFrame({
             'Prévision' : prevision,
             'Cumul'     : cumul,
             'Réalisé'   : realise,
            })
            m1_t['Prévision'].plot(color='green')
            m1_t['Cumul'].plot(kind='bar', width = 2*width, color='green')
            m1_t['Réalisé'].plot(kind='bar', width = width, color='red')


            ax = plt.gca()
            plt.xlim([-width, len(m1_t['Réalisé'])-width])
            ax.set_xticklabels(labels)
            #plt.xlabel('Mois')
            plt.ylabel("Chiffre d'affaire en k€")
            #plt.title("Indicateur")
            plt.legend()
            fig = plt.gcf()
            fig.set_size_inches(18.5, 10.5)
            filename = '/tmp/fiche_reporting.png'
            fig.savefig(filename,dpi=46)
            image = open(filename, 'rb')
            image_read = image.read()
            image_64_encode = base64.encodestring(image_read)
            obj.graphique = image_64_encode


