from odoo import fields, models,api,_
import logging




class Constat(models.Model):
    _name = "pdca.constat"
    _description = "Constats"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    document = fields.Binary('Document')
    name = fields.Text('Constat')
    code=fields.Char(string='Code',required=True,readonly=True,default=lambda self:_('New'))
    genere_action = fields.Boolean('Genere une action ?:',default=True)
    direction_concerne = fields.Many2one('pdca.direction', string="Direction Concernees")
    origine= fields.Many2one('pdca.origine',string="Origine")
    activite = fields.Many2many('pdca.unite',string="Activite",domain="[('direction','=',direction_pilote)]")
    processus = fields.Many2many('pdca.processus',string='Processus',domain="[('unite','=',activite)]")
    direction_pilote = fields.Many2many('pdca.direction',string="Direction Pilote")
    action_ids=fields.One2many('pdca.action','constat_id','Actions')

    status = fields.Selection([('ouvert','Ouvert'),
                               ('encours','En cours'),
                               ('traite','Traite'),
                               ('solde','Solde'),
                               ('annule','Annule')
                               ,('supprime','Supprime')],default="ouvert")
    
    type_constat = fields.Selection([('fort','Point fort'),
                                     ('progre','Piste de Progres'),
                                     ('sensible','Point Sensible'),
                                     ('recommendation','Recommendation'),
                                     ('recommendation_maj','Recommendation Majeure'),
                                     ('observation','Observation')],string="Type Constat")
    origine = fields.Selection([
                            ('blanc', 'Audit à blanc'),
                            ('ema', 'Audit externe EMA'),
                            ('iso45', 'Audit externe ISO 45001'),
                            ('iso90', 'Audit externe ISO 9001'),
                            ('2iso', 'Audit externe iso 9001 et 45001'),
                            ('externe', 'Audit externe métier'),
                            ('interne', 'Audit interne'),
                            ('bhe', 'BHE'),
                            ('boite', 'Boite à idée'),
                            ('mystere', 'Enquête mystère QdS'),
                            ('satisfactionVOyage', 'Enquête satisfaction voyageurs'),
                            ('satisfactionEMA', 'Enquêtes satisfaction EMA'),
                            ('exercices', 'Exercices / Simulations'),
                            ('fiche', 'Fiche d\'Amélioration et de Progrès'),
                            ('incident', 'incident / Accident'),
                            ('innov', 'Innov & Go'),
                            ('hse', 'Inspection HSE'),
                            ('qualite', 'Inspection Qualité'),
                            ('securite', 'Inspection sécurité ferroviaire'),
                            ('inspectionSecurite', 'Inspection sécurité incendie'),
                            ('inspectionSurete', 'Inspection Sureté'),
                            ('rapportAnnuel', 'Rapport Annuel d\'Activité'),
                            ('rapportMensuel', 'Rapport Mensuel d\'Activité'),
                            ('rapportMetier', 'Rapport Métier'),
                            ('revueDirection', 'Revue de Direction'),
                            ('revueAmelioration', 'Revue du Plan d\'Amélioration'),
                            ('riskManagement', 'Risk management'),
                            ('conformite', 'Conformité légale'),
                            ('auditCertification', 'Audit de certification')],'Origine')
    

    def affecter_pilote(self, **kwargs):
        constat_concerne = self.id
        print(constat_concerne)

        user = self.env.user
        current_user = self.env['pdca.employe'].search([('user_id','=',user.id)])
        direction = current_user.direction_id.id

        domain = ['&',('direction_pilote_id','=',direction),('constat_id','=',constat_concerne)]
        affectation = self.env['pdca.affectation_pilote'].search(domain)
        print('-------------------')
        print(affectation)
        print(affectation.id)
        print('-------------------')
        return {
            'type': 'ir.actions.act_url',
            'url': '/web#id=%d&action=163&model=pdca.affectation_pilote&view_type=form&cids=1&menu_id=153' % (affectation),
            'target': 'self',
        }

                
            

    
    
    def creer_constat_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        constat_form_url = '/web#id=%d&action=159&model=pdca.constat&view_type=form&cids=&menu_id=153' % self.id
        return base_url + constat_form_url
    
    def pass_dir_pilote_emails(self):
        dir_pilote_ids=self.direction_pilote.ids
        dir_pilote_records=self.env['pdca.direction'].search([('id','in',dir_pilote_ids)])
        personnes_concernes=''
        for dir_pilote in dir_pilote_records:
            if dir_pilote.directeur.email not in personnes_concernes:
                personnes_concernes+=dir_pilote.directeur.email+','
            if dir_pilote.referent.email not in personnes_concernes:
                personnes_concernes += dir_pilote.referent.email + ','
        personnes = personnes_concernes.rstrip(",")
        return personnes

    def send_mail_notif(self):
        template_id = self.env.ref('Plan-d-amelioration.creation_constat_template')
        for rec in self:
            self.creer_constat_url()
            template_id.send_mail(rec.id, force_send=True)
        return
    
    def send_mail_constat_fort(self):
        template_id = self.env.ref('Plan-d-amelioration.constat_type_fort_mail')
        for rec in self:
            self.creer_constat_url()
            template_id.send_mail(rec.id, force_send=True)
        return
    
    def supprimer_constat(self):
        self.status='supprime'
        template_id= self.env.ref('Plan-d-amelioration.constat_supprime_template')
        for rec in self:
            self.send_mail_notif()
            template_id.send_mail(rec.id, force_send=True)

    @api.model
    def create(self, vals):
        if vals.get('code',_('New'))==_('New'):
            vals['code']=self.env['ir.sequence'].next_by_code('pdca.constat') or _('New')
        record = super(Constat, self).create(vals)
        if vals['type_constat'] == 'fort':
            if not vals['genere_action']:
                record.send_mail_constat_fort()
                return record
        # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%55')
        # # print('0000000000000000000', self.direction_pilote)
        # print('0000000000000000000', vals['direction_pilote'])
        # print('--------------', record.direction_pilote.ids)

        for rec in vals['direction_pilote'][0][2]:
            # print('************************************')
            # print(rec)
            affectation_pilote = {
                'constat_id': record.id,
                'direction_pilote_id': rec,
                'origine_constat': self.origine,
                'type_constat': self.type_constat, 
            }
            affectation_record = self.env['pdca.affectation_pilote'].create(affectation_pilote)
            # affectation_pilote.send_mail_notif
            action = {
                'direction_id': rec,
                'constat_id': record.id
            }
           
            # print ('--------------------')
            print(affectation_record)
            action_record = self.env['pdca.action'].create(action)
            print(action_record)
            # print ('--------------------')

        record.send_mail_notif()
        return record
    
    def emails(self):
        # print(self.direction_pilote.ids)
        for rec in self.direction_pilote:
            print (rec.id)
    
    @api.onchange('direction_pilote')
    def change_activite(self):
        if self.direction_pilote: 
            unites = self.direction_pilote.ids
            activite_domain = [('direction','=',unites[-1])]
            return {'domain': {'activite': activite_domain}}
        else:
            self.activite = False
        
    @api.onchange('activite')
    def change_processus(self):
        if self.activite:
            processus = self.activite.ids
            processus_domain = [('unite','=',processus[-1])]
            return {'domain': {'processus': processus_domain}}
        else:
            self.processus = False
