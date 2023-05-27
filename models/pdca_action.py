from odoo import models,fields,api
from odoo.exceptions import ValidationError

class Action(models.Model):
    _name="pdca.action"
    _description="Action"
    _rec_name="action"

    action = fields.Text(string="Action")
    date_creation = fields.Date("Date de creation",default=fields.Date.today)
    date_fin_previsionelle = fields.Date('Date Fin Previsionelle')
    risque= fields.Text(string='Risque')
    cause=fields.Text(string="Cause")
    oppurtunite=fields.Text(string="Oppurtunite")
    taux_avancement=fields.Integer('Taux d\'avancement',default=0)
    motif_rejet=fields.Text("Motif de rejet")

    pilote_id = fields.Many2one('pdca.employe',"Pilote d'action")
    constat_id=fields.Many2one('pdca.constat',string="Constat")
    direction_id = fields.Many2one('pdca.direction',string="Direction ")
    statut_approbation = fields.Selection([
        ('pasEncore', 'Pas Encore'),
        ('approuve', 'Approuve'),
        ('Disapprouve', 'Disapprouve')
    ],default="pasEncore")
    
    type_risque=fields.Selection([
        ('qualite','Qualite'),
        ('finance', 'Finance')
    ],string="Type Risque")
    type_action = fields.Selection([
        ('corrective','Action Corrective'),
        ('preventive','Action Preventive'),
        ('amelioration','Action Amelioration'),
        ('non_retenue', 'Non Retenue')
    ],string="Type Action")
    status=fields.Selection([('nonentamne','Non entamne'),
                            ('endefinition',"Definition de l'action"),
                            ('enattentevalidation','En attente de validation'),
                            ('encours','Encours'),
                            ('enattenteaproba',"En attente d'approbation"),
                            ('approuve','Approuve'),
                            ('realise','Realise'),
                            ('solde','Solde')],default='nonentamne',string="Statu")

    def approuver_action(self):
        if self.taux_avancement == 100:
            self.status= 'approuve'
        else:
            raise  ValidationError("Taux Avancement n'est pas a 100% pour approuvee cette action")
        
        if self.type_action.name=='Action corrective':
            self.status='realise'
            self.constat_id.status='traite'
        else:
            self.status='solde'
            actions_records=self.env['pdca.action'].search([('constat_id','in',self.constat_id)])
            for action in actions_records:
                if action:
                    if action.status!='solde':
                       return                   
                self.constat_id.status='solde'
                        

    def creer_action_definie_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        action_form_url = '/web#id=%d&action=162&model=pdca.action&view_type=form&cids=&menu_id=153' % self.id
        
        return base_url + action_form_url
    
    def send_mail_notifiction(self,template, email):
        template_id = self.env.ref(template)
        for rec in self:
            self.creer_action_definie_url()
            template_id.send_mail(rec.id, force_send=True,email_values={
                'email_to':email
            })
        return
    
    def redefinir_action(self):
        template = 'Plan-d-amelioration.action_redefinie_template'
        self.send_mail_notifiction(template, self.pilote_id.email)
    
    def valider_action(self):
        template = 'Plan-d-amelioration.validation_template'
        self.send_mail_notifiction(template, self.pilote_id.email)
        self.status='encours'
    
    @api.model
    def create(self, values):
        result = super().create(values)
        result.status='nonentamne'

        # if result.constat_id and result.id not in result.constat_id.action_ids.ids:
        #     result.constat_id.write({'action_ids':[(4,result.id)]})
        template = 'Plan-d-amelioration.action_definie_template'            
        result.send_mail_notifiction(template, self.constat_id.create_uid.email)
        return result
    
    def write(self, values):
        if 'status' not in values:
            values['status'] = 'enattentevalidation'
        res = super().write(values)
        template = 'Plan-d-amelioration.action_definie_template'
        self.send_mail_notifiction(template, self.constat_id.create_uid.email)
        return res
    
 
    def incrementer_taux_avancement(self):
        self.taux_avancement = self.taux_avancement + 10
        if self.taux_avancement == 100 :
            template = 'taux_avancement_100_template'
            self.send_mail_notifiction(template, self.constat_id.create_uid.email)
            self.status = 'enattenteapproba'
        return

   
    
    