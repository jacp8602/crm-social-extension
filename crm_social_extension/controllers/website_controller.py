from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website


class CustomerPromotionController(http.Controller):
    
    @http.route('/customers-promotion', type='http', auth="public", website=True)
    def customers_promotion(self, search='', **kwargs):
        """Página para promocionar clientes"""
        customer = request.env['res.partner']
        
        # Dominio base para buscar clientes
        domain = [
            # ('customer_rank', '>', 0),  # Solo clientes
            ('active', '=', True),      # Solo activos
        ]

        if 'customer_rank' in customer.fields_get(['customer_rank']):
            domain += [('customer_rank', '>', 0)] # Solo clientes

        # Agregar búsqueda si hay término
        if search:
            domain += [
                '|', '|', '|',
                ('name', 'ilike', search),
                ('facebook_url', 'ilike', search),
                ('linkedin_url', 'ilike', search),
                ('twitter_url', 'ilike', search)
            ]
        
        # Buscar clientes
        customers = customer.search(domain)
        
        return request.render('crm_social_extension.customers_promotion_template', {
            'customers': customers,
            'search': search,
            'page_name': 'customers_promotion'
        })

    @http.route('/customers-promotion/search', type='json', auth="public", website=True)
    def customers_search(self, search_term, **kwargs):
        """Búsqueda AJAX para clientes"""
        customer = request.env['res.partner']
        domain = [
            # ('customer_rank', '>', 0),
            ('active', '=', True),
            '|', '|', '|',
            ('name', 'ilike', search_term),
            ('facebook_url', 'ilike', search_term),
            ('linkedin_url', 'ilike', search_term),
            ('twitter_url', 'ilike', search_term)
        ]
        
        if 'customer_rank' in customer.fields_get(['customer_rank']):
            domain += [('customer_rank', '>', 0)] # Solo clientes
            
        customers = customer.search_read(
            domain,
            ['name', 'email', 'phone', 'facebook_url', 'linkedin_url', 'twitter_url']
        )
        
        return {'customers': customers}