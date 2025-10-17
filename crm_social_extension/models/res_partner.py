from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Campos para redes sociales
    facebook_url = fields.Char(
        string='Facebook',
        help='URL of Facebook profile',
        default=''
    )
    linkedin_url = fields.Char(
        string='LinkedIn',
        help='URL of LinkedIn profile',
        default=''
    )
    twitter_url = fields.Char(
        string='Twitter',
        help='URL of Twitter profile',
        default=''
    )
    
    # Campo computado para determinar si el perfil está completo
    profile_complete = fields.Boolean(
        compute='_compute_profile_complete',
        store=True,
        readonly=True
    )

    @api.depends('facebook_url', 'linkedin_url', 'twitter_url')
    def _compute_profile_complete(self):
        """Calcula si el perfil está completo (todas las redes sociales están llenas)"""
        for partner in self:
            partner.profile_complete = bool(
                partner.facebook_url and 
                partner.linkedin_url and 
                partner.twitter_url
            )

    @api.constrains('facebook_url', 'linkedin_url', 'twitter_url')
    def _check_social_urls(self):
        """Valida que las URLs tengan formato correcto"""
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// o https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # dominio
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # puerto opcional
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        for partner in self:
            for field_name in ['facebook_url', 'linkedin_url', 'twitter_url']:
                url = getattr(partner, field_name)
                if url and not url_pattern.match(url):
                    raise ValidationError(
                        f'The URL for {field_name.replace("_url", "").title()} is not valid: {url}'
                    )

    def get_social_networks(self):
        """Retorna un diccionario con las redes sociales disponibles"""
        social_networks = {}
        if self.facebook_url:
            social_networks['facebook'] = {
                'url': self.facebook_url,
                'icon': 'fa-facebook',
                'label': 'Facebook'
            }
        if self.linkedin_url:
            social_networks['linkedin'] = {
                'url': self.linkedin_url,
                'icon': 'fa-linkedin',
                'label': 'LinkedIn'
            }
        if self.twitter_url:
            social_networks['twitter'] = {
                'url': self.twitter_url,
                'icon': 'fa-twitter',
                'label': 'Twitter'
            }
        return social_networks