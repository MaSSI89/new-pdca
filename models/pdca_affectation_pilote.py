from odoo import fields,models,api

class AffectationPilote(models.Model):
    _name = "pdca.affectation_pilote"
    _rec_name='pilote_id'
    
    _inherit = ['mail.thread', 'mail.activity.mixin']
    origine_constat = fields.Char('Origine')
    type_constat = fields.Char('Type Constat')
    direction_pilote_id = fields.Many2one('pdca.direction','Direction Pilote')
    pilote_id = fields.Many2one('pdca.employe',"Pilote d'action")
    constat_id=fields.Many2one('pdca.constat','Constat')
    action_id=fields.Many2one('pdca.action','Action')
    
    @api.model
    def write(self, vals, *args):
        # print(*args)
        print(vals)
        print(self)
        if not self.pilote_id :
            return
        
        record =  super(AffectationPilote, self).write(*args)
        print(record)
        self.send_mail_notif()
        return record

    # def ajouter_action(self): 
    #     self.constat_id.status='encours'
    #     return {
    #         'res_model': 'pdca.action',
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'view_id': self.env.ref('Plan-d-amelioration.pdca_action_view_form').id,
    #         'context': {'default_pilote_id': self.pilote_id.id,
    #                     'default_constat_id':self.constat_id.id,
    #                     'default_direction_id': self.direction_pilote_id
    #                     }
    #     }
    
    # def creer_taux_avancement_constat_url(self):
    #     base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     action_form_url = '/web#id=%d&action=162&model=pdca.action&view_type=form&cids=&menu_id=153' % self.action_id.id
    #     return base_url + action_form_url
    

    # def send_taux_avancement_notification(self):
    #     template_id = self.env.ref('Plan-d-Amelioration.taux_avancement_template')
    #     for rec in self:
    #         self.creer_taux_avancement_constat_url()
    #         template_id.send_mail(rec.id, force_send=True,email_values={
    #             'email_to':self.constat_id.create_uid.email
    #         })
    #     return
    

    # def update_action(self):
    #     action = self.env['pdca.action'].search([('pilote', '=', self.id)], limit=1)
    #     if action:
    #         if action.taux_avancement==100:
    #             action.status='enattenteaproba'
    #             self.send_taux_avancement_notification()
    #             print('c bon tekfa laction')
    #         else:
    #             action.taux_avancement=action.taux_avancement+10

    def creer_affectation_pilote_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        pilote_form_url = '/web#id=%d&action=163&model=pdca.affectation_pilote&view_type=form&cids=&menu_id=153' % self.id
        return base_url + pilote_form_url
    
    def send_mail_notif(self):
        template_id = self.env.ref('Plan-d-amelioration.affectation_pilote_template')
        for rec in self:
            self.creer_affectation_pilote_url()
            template_id.send_mail(rec.id, force_send=True)
        return
    
    @api.model
    def create(self, vals):
        record = super(AffectationPilote, self).create(vals)
        print('-----------invoked mailing affectaiton pilote---')
        record.send_mail_notif()
        print('----------sent-----------')
        return record
    
    # @api.onchange('direction_pilote_id')
    # def load_pilotes_direction(self):
    #         pilotes_ids = [('direction_id','=',self.direction_pilote_id.id)]
    #         return {'domain': {'pilote_id': pilotes_ids}}