from odoo import models, fields

class Unite(models.Model):
    _name = "pdca.unite"
    _description = "UNite"

    name = fields.Char('Nom De Unite', required=True)
    direction= fields.Many2one('pdca.direction','Direction')
    directeur = fields.Many2one('pdca.employe', ondelete='set null')
    processus_ids=fields.One2many('pdca.processus','unite','Processus',domain="[('unite','=',name)]")
   
