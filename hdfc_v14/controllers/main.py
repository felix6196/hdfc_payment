from odoo import http
from odoo.http import request
import hashlib
from Crypto.Cipher import AES

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
    
    @http.route(['/shop/onlinepayment/validate'], type='http', auth='public', csrf=False, website=True)
    def website_hdfc_payment(self, **post):
        print(post)
        acquirer = request.env['payment.acquirer'].sudo().browse(eval(post.get('acquirer')))
        currency = request.env['res.currency'].sudo().browse(eval(post.get('currency_id')))
        partner_id = request.env['res.partner'].sudo().search([('id', '=', int(post.get('billing_partner_id')))])
        print(partner_id)
        sale_order_id = request.env['sale.order'].sudo().search([('name', '=', post.get("reference").split('-')[0])])
        print(sale_order_id)
        # if currency not in ['CAD', 'GBP', 'USD']:
        #     return request.redirect('/shop/cart')
        merchant_id = acquirer.merchant_id
        working_key = acquirer.working_key
        accesscode = acquirer.access_code
        redirect_to = acquirer.redirect_url
        website_security = acquirer.website_security
        web_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if website_security == 'http':
            base_url = web_base_url
        elif website_security == 'https':
            base_url = web_base_url
            base_url = base_url.replace('http:', 'https:') if 'http:' in base_url else base_url
        else:
            base_url = web_base_url
            base_url = base_url.replace('http:', 'https:') if 'http:' in base_url else base_url
        success_url = '/payment/return'
        failure_url = '/payment/cancel'
        values = {
            'merchant_id': merchant_id,
            'order_id': post.get('reference'),
            'currency': "INR",
            'amount': post.get('amount'),
            'redirect_url': base_url+success_url,
            'cancel_url': base_url+failure_url,
            'language': "EN",
            'billing_name':post.get('partner_name'),
            'billing_address': post.get('billing_partner_address'),
            'billing_city': post.get('billing_partner_city'),
            'billing_state': "Test",
            'billing_zip': post.get('billing_partner_zip'),
            'billing_country': post.get('billing_partner_country_id'),
            'billing_tel': 'Test',
            'billing_email': post.get('partner_email'),

            #                     Shipping information(optional):
            'delivery_name': post.get('partner_name'),
            'delivery_address': post.get('billing_partner_address'),
            'delivery_city':  post.get('billing_partner_city'),
            'delivery_state':  "Test",
            'delivery_zip': post.get('billing_partner_zip'),
            'delivery_country': post.get('billing_partner_country_id'),
            'delivery_tel': 'Phone',
            'merchant_param1': str(acquirer.id) if str(acquirer.id) else '',
            'merchant_param2': str(partner_id.id),
            'merchant_param3': str(sale_order_id.id),
            'merchant_param4': str(currency),
            'merchant_param5': '',
            # 'integration_type': 'iframe_normal',
            'promo_code': '',
            # 'workingkey': working_key,
            'redirect_to': redirect_to,
        }
        datas = ""
        print(values)
        for key in values:
            if (key != 'csrf_token'):
                datas = datas + (key + '=' + values.get(key)) + '&'
        encryptedtext = self.encrypt_val(datas, working_key)
        payload = {
            'encRequest': encryptedtext,
            'access_code': accesscode,
            'redirect_to': redirect_to,
        }
        return request.render('HDFC.HDFC_payment_pay', payload)
