from odoo import http
from odoo.http import request


class AllController(http.Controller):

    @http.route('/posunit/home', type='http', auth='user')
    def posUnitHome(self, config_id=False, **kwargs):
        return request.render('pos_unit.index')

    @http.route('/posunit/show/receipts', type='http', auth='user')
    def posUnitShowReceipts(self, config_id=False, **kwargs):
        return request.render('pos_unit.show_receipts')
