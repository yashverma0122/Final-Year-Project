from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

class UserAccountTests(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', 'password', full_name='Test User')
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.full_name, 'Test User')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertTrue(str(super_user), "full_name")

        with self.assertRaises(ValueError):
            db.objects.create_superuser( email='testuser@super.com', full_name='Test User',password='password', is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser( email='testuser@super.com', full_name='Test User',password='password', is_staff=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser( email='testuser@super.com', full_name='Test User',password='password', is_admin=False)

    
    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'password', full_name='Test User'
        )

        self.assertEqual(user.email, 'testuser@user.com')
        self.assertEqual(user.full_name, 'Test User')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)

        with self.assertRaises(ValueError):
            db.objects.create_user(email='', password='password',)
        
        with self.assertRaises(ValueError):
            db.objects.create_user(email='testuser@user.com', password='password', )
        
        

