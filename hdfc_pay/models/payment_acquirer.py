from odoo import fields, models, api, tools, _
from odoo.exceptions import ValidationError

class HDFC(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(
        selection=[('manual', 'Manual Configuration'), ('hdfc', 'HDFC')], string='Provider',
        default='manual')
    merchant_id = fields.Char('Merchant ID')
    access_code = fields.Char('Access Code')
    working_key = fields.Char('Working Key')
    redirect_url = fields.Char('Redirect URL')
    website_security = fields.Selection([('http', 'HTTP'), ('https', 'HTTPS')], string="Domain", default='http')
    # acquirer_code = fields.Char('code')
