from odoo.tests import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestCrmSocialExtension(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.partner_model = self.env['res.partner']
        
        # Crear un partner de prueba
        self.test_partner = self.partner_model.create({
            'name': 'Test Customer',
            'email': 'test@example.com',
        })
    
    def test_social_fields_creation(self):
        """Test that social network fields are created correctly"""
        self.assertEqual(self.test_partner.name, 'Test Customer')
        self.assertFalse(self.test_partner.profile_complete)
        
        # Agregar redes sociales
        self.test_partner.write({
            'facebook_url': 'https://facebook.com/test',
            'linkedin_url': 'https://linkedin.com/in/test',
            'twitter_url': 'https://twitter.com/test',
        })
        
        self.assertTrue(self.test_partner.profile_complete)
    
    def test_profile_complete_computation(self):
        """Test the profile complete computation logic"""
        # Sin redes sociales
        self.test_partner.write({
            'facebook_url': False,
            'linkedin_url': False,
            'twitter_url': False,
        })
        self.test_partner.invalidate_recordset()
        self.assertFalse(self.test_partner.profile_complete)
        
        # Con una red social
        self.test_partner.write({'facebook_url': 'https://facebook.com/test'})
        self.test_partner.invalidate_recordset()
        self.assertFalse(self.test_partner.profile_complete)
        
        # Con todas las redes sociales
        self.test_partner.write({
            'linkedin_url': 'https://linkedin.com/in/test',
            'twitter_url': 'https://twitter.com/test',
        })
        self.test_partner.invalidate_recordset()
        self.assertTrue(self.test_partner.profile_complete)
    
    def test_url_validation(self):
        """Test URL validation"""
        # URL válida
        self.test_partner.write({
            'facebook_url': 'https://facebook.com/test',
        })
        
        # URL inválida
        with self.assertRaises(ValidationError):
            self.test_partner.write({
                'facebook_url': 'invalid-url',
            })
    
    def test_get_social_networks_method(self):
        """Test the get_social_networks method"""
        self.test_partner.write({
            'facebook_url': 'https://facebook.com/test',
            'linkedin_url': 'https://linkedin.com/in/test',
            'twitter_url': False,
        })
        
        social_networks = self.test_partner.get_social_networks()
        
        self.assertIn('facebook', social_networks)
        self.assertIn('linkedin', social_networks)
        self.assertNotIn('twitter', social_networks)
        self.assertEqual(social_networks['facebook']['url'], 'https://facebook.com/test')
    
    def test_search_domain_for_incomplete_profiles(self):
        """Test search domain for incomplete profiles"""
        # Crear partners con diferentes estados
        partner1 = self.partner_model.create({
            'name': 'Incomplete Profile',
            'facebook_url': 'https://facebook.com/test',
        })
        
        partner2 = self.partner_model.create({
            'name': 'Complete Profile',
            'facebook_url': 'https://facebook.com/test',
            'linkedin_url': 'https://linkedin.com/in/test',
            'twitter_url': 'https://twitter.com/test',
        })
        
        # Buscar perfiles incompletos
        incomplete_partners = self.partner_model.search([
            ('profile_complete', '=', False)
        ])
        
        self.assertIn(partner1, incomplete_partners)
        self.assertNotIn(partner2, incomplete_partners)
    
    def test_website_search_functionality(self):
        """Test website search functionality"""
        # Crear partners de prueba
        test_customer = self.partner_model.create({
            'name': 'Website Test Customer',
            'customer_rank': 1,
            'facebook_url': 'https://facebook.com/websitetest',
            'linkedin_url': 'https://linkedin.com/in/websitetest',
            'twitter_url': 'https://twitter.com/websitetest',
        })
        
        # Probar búsqueda por nombre
        domain = [
            ('active', '=', True),
            '|', '|', '|',
            ('name', 'ilike', 'Website Test'),
            ('facebook_url', 'ilike', 'Website Test'),
            ('linkedin_url', 'ilike', 'Website Test'),
            ('twitter_url', 'ilike', 'Website Test')
        ]
        
        results = self.partner_model.search(domain)
        self.assertIn(test_customer, results)
        
        # Probar búsqueda por URL de red social
        domain_url = [
            ('active', '=', True),
            '|', '|', '|',
            ('name', 'ilike', 'websitetest'),
            ('facebook_url', 'ilike', 'websitetest'),
            ('linkedin_url', 'ilike', 'websitetest'),
            ('twitter_url', 'ilike', 'websitetest')
        ]
        
        results_url = self.partner_model.search(domain_url)
        self.assertIn(test_customer, results_url)