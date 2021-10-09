from odoo.http import request
from odoo import http
import hashlib
from Crypto.Cipher import AES
import logging

_logger = logging.getLogger(__name__)
class HDFCPaymentController(http.Controller):
    
    def pad(self, data):
        length = 16 - (len(data) % 16)
        data = str(data) + chr(length) * length
        return data

    def encrypt_val(self, plainText, workingKey):
        iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        plainText = self.pad(plainText)
        encDigest = hashlib.md5()
        encDigest.update(workingKey.encode())
        enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
        encryptedText = enc_cipher.encrypt(plainText).hex()
        return encryptedText

    def decrypt_val(self, cipherText, workingKey):
        iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        decDigest = hashlib.md5()
        decDigest.update(workingKey.encode())
        encryptedtext = bytes.fromhex(cipherText)
        dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
        decryptedtext = dec_cipher.decrypt(encryptedtext)
        return decryptedtext
    
    @http.route(['/payment/return', '/payment/cancel'], type='http', auth='public', csrf=False,
                website=True)
    def payment_return(self, **post):
        acquirer = request.env['payment.acquirer'].sudo().search([('provider', '=', 'hdfc')], limit=1)
        working_key = acquirer.working_key
        if post.get('encResp'):
            data = post.get('encResp')
            decrypted_text = self.decrypt_val(data, working_key)
            string_value = str(decrypted_text)
            result_obj = {x.split('=')[0]: x.split('=')[1] for x in string_value.split("&")}
            acquirer_id = request.env['payment.acquirer'].sudo().search([('id', '=', int(result_obj.get("merchant_param1") if result_obj.get("merchant_param1") else False))])
            partner_id = request.env['res.partner'].sudo().search([('id', '=', int(result_obj.get("merchant_param2") if result_obj.get("merchant_param2") else False))])
            record = request.env['payment.transaction'].sudo().search([])
            if (result_obj != 'undefined') and isinstance(result_obj,dict):
                if result_obj.get("order_status") == 'Success':
                    
                    val = {"acquirer_id": acquirer_id.id,
                           "amount":0,
                           "partner_id":partner_id.id,
                           
                           
                           'partner_name':partner_id.name,
                           "partner_lang": partner_id.lang,
                           "partner_email": partner_id.email,
                           "partner_zip":  partner_id.zip,
                           "partner_address": partner_id.street,
                           # "partner_city": partner_id.street,
                           "partner_country_id":  partner_id.country_id,
                           "partner_phone":  partner_id.mobile,
                           "payment_mode": result_obj.get("card_name"),
                           "card_name": result_obj.get("card_name"),
                           "bank_ref_no": result_obj.get("bank_ref_no"),
                           "tracking_id": result_obj.get("tracking_id"),
                           "status_code": result_obj.get("status_code"),
                           "currency_id": partner_id.user_id.currency_id if partner_id.user_id.currency_id else 1,
                           'state': 'done',
                           'reference': result_obj.get("bank_ref_no"),
                           }
                    transaction_id = record.sudo().create(val)
                else:
                    val = {
                            "acquirer_id": acquirer_id.id,
                           "amount":0,
                           "partner_id":partner_id.id,
                           'partner_name':partner_id.name,
                           "partner_lang": partner_id.lang,
                           "partner_email": partner_id.email,
                           "partner_zip":  partner_id.zip,
                           "partner_address": partner_id.street,
                           # "partner_city": partner_id.street,
                           "partner_country_id":  partner_id.country_id,
                           "partner_phone":  partner_id.mobile,
                           "payment_mode": result_obj.get("card_name"),
                           "card_name": result_obj.get("card_name"),
                           "bank_ref_no": result_obj.get("bank_ref_no"),
                           "tracking_id": result_obj.get("tracking_id"),
                           "status_code": result_obj.get("status_code"),
                           "currency_id": result_obj.get("merchant_param4"),
                           'state': 'error',
                           'reference': result_obj.get("bank_ref_no"),
                       }
                    transaction_id = record.sudo().create(val) 
            if result_obj.get("order_status") == 'Success':
                transaction_id.sudo().write({
                    'state': 'done'
                    })
                print(result_obj.get("order_id"))
                sale_order_id = request.env['sale.order'].sudo().search([('id', '=', int(result_obj.get("merchant_param3") if result_obj.get("merchant_param3") else False))])
                print(transaction_id.state)
                print(transaction_id.id, "TX.ID")
                if transaction_id is None:
                    tx = request.website.sale_get_transaction()
                else:
                    tx = request.env['payment.transaction'].browse(transaction_id)
        
                if transaction_id and transaction_id.state == 'draft':
                    return request.redirect('/shop')
        
                return request.render("website_sale.confirmation", {'order': sale_order_id})
            else:
                transaction_id.state = 'error'
                return request.redirect('/shop')
