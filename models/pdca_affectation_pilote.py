from odoo import fields,models,api

class AffectationPilote(models.Model):
    _name = "pdca.affectation_pilote"
    _rec_name='pilote_id'
    
    _inherit = ['mail.thread', 'mail.activity.mixin']
    origine_constat = fields.Char('Origine')
    type_constat = fields.Char('Type Constat')
    affecte = fields.Selection([
        ('nonAffecte','Non Affecte'),
        ('affecte', 'Affecte')
    ],default="nonAffecte")
    direction_pilote_id = fields.Many2one('pdca.direction','Direction Pilote')
    pilote_id = fields.Many2one('pdca.employe',"Pilote d'action", domain="[('direction_id','=',direction_pilote_id)]")
    constat_id=fields.Many2one('pdca.constat','Constat')
    action_id=fields.Many2one('pdca.action','Action')
    
    # @api.model
    def write(self, vals):
        # print(*args)
        if not vals['pilote_id']:
            return
        
        record = super(AffectationPilote, self).write(vals)
        # affec = self.env['pdca.affectation_pilote'].search('id',)
        # self.affecte = 'affecte'
        domain = ['&',('direction_id','=',self.direction_pilote_id.id),('constat_id','=', self.constat_id.id)]
        action_concerne = self.env['pdca.action'].search(domain)
        print(action_concerne)

        action_concerne.pilote_id = self.pilote_id
        template = 'Plan-d-amelioration.affectation_pilote_template'
        emails = action_concerne.pilote_id.user_id.login
        self.send_mail_notif(template, emails)
        return record    
        
    def get_affectation_pilote_url(self):
        # base_url = self.env['ir.config_parameter'].sudo().get_param('web.base_url')
        print('***********SELF ID ******',self.id)
        affectation_pilote_url = 'localhost:8069/web#id=%d&action=163&model=pdca.affectation_pilote&view_type=form&cids=1&menu_id=153' % self.id
        print(affectation_pilote_url)
        return  affectation_pilote_url
    
    def ajouter_action(self): 
        self.sudo().constat_id.status = 'encours'
        return {
            'type': 'ir.actions.act_url',
            'url': '/web#id=%d&action=162&model=pdca.action&view_type=form&cids=1&menu_id=153' % (self.action_id.id),
            'target': 'self',
        }
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
    
    def send_mail_notif(self, template, emails):
        template_id = self.env.ref(template)
        for rec in self:
            self.creer_affectation_pilote_url()
            template_id.send_mail(rec.id, force_send=True,email_values={
                'email_to': emails
            })
        return
    
    

    @api.model
    def create(self, vals):
        record = super(AffectationPilote, self).create(vals)
        print('-----------invoked mailing affectaiton pilote---')
        template = 'Plan-d-amelioration.affectation_direction_pilote_template'
        emails = record.direction_pilote_id.directeur.user_id.login + ',' + record.direction_pilote_id.referent.user_id.login
        print('+++++++++EMAILS+++++++',emails)
        record.send_mail_notif(template, emails)
        print('----------sent-----------')
        return record
    
    # @api.onchange('direction_pilote_id')
    # def load_pilotes_direction(self):
    #         pilotes_ids = [('direction_id','=',self.direction_pilote_id.id)]
    #         return {'domain': {'pilote_id': pilotes_ids}}