from odoo import models, fields

class Users(models.Model):
    _inherit = 'res.users'

    def has_group(self, cr,uid,group_ext_id):
        if '.' in group_ext_id:
            group_administrateur = [x.id for x in self.pool['ir.model.data'].get_object(cr, uid, 'bms', 'group_pdca_administrateur').users]
            group_directeur = [x.id for x in self.pool['ir.model.data'].get_object(cr, uid, 'bms', 'group_pdca_directeur').users]
            group_referent = [x.id for x in self.pool['ir.model.data'].get_object(cr, uid, 'bms', 'group_pdca_referent').users]

            if uid in group_administrateur:
                return super(Users, self).has_group(cr, uid, 'group_pdca_administrateur')
            elif uid in group_directeur:
                return super(Users, self).has_group(cr, uid, 'group_pdca_directeur')
            elif uid in group_referent:
                return super(Users, self).has_group(cr, uid, 'group_pdca_referent')
            else:
                return super(Users,self).has_group(cr, uid, 'base.group_user')
        else: 
            return super(Users, self).has_group(cr, uid, group_ext_id)
