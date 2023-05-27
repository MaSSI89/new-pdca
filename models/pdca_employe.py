from odoo import models,fields,api

class Employe(models.Model):
    _name='pdca.employe'
    _description='Action'
    _inherits = {'res.users': 'user_id'}
    
    user_id=fields.Many2one('res.users','Employe',ondelete='cascade',delegate=True,required=True)
    
    matricule_cnas=fields.Integer('Matricule CNAS')
    post_occupe = fields.Char('Poste Occupe')
    direction_id=fields.Many2one('pdca.direction','Direction')
    action_ids = fields.One2many('pdca.action','pilote_id','Actions Fait')

    @api.onchange('login')
    def onchnge_login(self):
        if self.login :
            self.email = self.login
        else :
            self.email = False
    
    