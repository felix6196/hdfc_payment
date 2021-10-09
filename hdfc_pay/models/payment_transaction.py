import logging

from odoo import fields, models, _
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    payment_mode = fields.Char(string='Invoice')
    card_name = fields.Char(string='Care Name')
    bank_ref_no = fields.Char(string='Banf Ref No')
    tracking_id = fields.Char(string='Tracking ID')
    status_code = fields.Char(string="Status Code")
    
