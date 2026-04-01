"""Unit tests for AnonymousUser model and Permission system."""
import unittest
from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission


class AnonymousUserTestCase(unittest.TestCase):
    """Tests for the AnonymousUser model's can() and is_administrator() methods."""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_can_returns_false_for_follow(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))

    def test_can_returns_false_for_comment(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.COMMENT))

    def test_can_returns_false_for_write(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.WRITE))

    def test_can_returns_false_for_moderate(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.MODERATE))

    def test_can_returns_false_for_admin(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.ADMIN))

    def test_can_returns_false_for_zero_permission(self):
        u = AnonymousUser()
        self.assertFalse(u.can(0))

    def test_can_returns_false_for_combined_permissions(self):
        u = AnonymousUser()
        combined = Permission.FOLLOW | Permission.COMMENT | Permission.WRITE
        self.assertFalse(u.can(combined))

    def test_can_returns_false_for_all_permissions(self):
        u = AnonymousUser()
        all_perms = (Permission.FOLLOW | Permission.COMMENT |
                     Permission.WRITE | Permission.MODERATE | Permission.ADMIN)
        self.assertFalse(u.can(all_perms))

    def test_can_returns_false_for_negative_value(self):
        u = AnonymousUser()
        self.assertFalse(u.can(-1))

    def test_can_returns_false_for_large_integer(self):
        u = AnonymousUser()
        self.assertFalse(u.can(99999))

    def test_is_administrator_returns_false(self):
        u = AnonymousUser()
        self.assertFalse(u.is_administrator())

    def test_can_always_returns_bool_false(self):
        u = AnonymousUser()
        result = u.can(Permission.ADMIN)
        self.assertIs(result, False)

    def test_is_administrator_always_returns_bool_false(self):
        u = AnonymousUser()
        result = u.is_administrator()
        self.assertIs(result, False)


class PermissionTestCase(unittest.TestCase):
    """Tests for the Permission class constants."""

    def test_permission_values_are_power_of_two(self):
        self.assertEqual(Permission.FOLLOW, 1)
        self.assertEqual(Permission.COMMENT, 2)
        self.assertEqual(Permission.WRITE, 4)
        self.assertEqual(Permission.MODERATE, 8)
        self.assertEqual(Permission.ADMIN, 16)

    def test_permissions_are_distinct(self):
        perms = [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE,
                 Permission.MODERATE, Permission.ADMIN]
        self.assertEqual(len(set(perms)), len(perms))

    def test_permission_combination(self):
        combined = Permission.FOLLOW | Permission.COMMENT | Permission.WRITE
        self.assertTrue(combined & Permission.FOLLOW)
        self.assertTrue(combined & Permission.COMMENT)
        self.assertTrue(combined & Permission.WRITE)
        self.assertFalse(combined & Permission.MODERATE)
        self.assertFalse(combined & Permission.ADMIN)


class UserCanEdgeCaseTestCase(unittest.TestCase):
    """Tests for User.can() edge cases."""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_can_returns_false_when_role_is_none(self):
        u = User(email='test@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        self.assertIsNone(u.role_id)
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_can_returns_true_when_role_has_permission(self):
        Role.insert_roles()
        u = User(email='test@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(u.can(Permission.FOLLOW))

    def test_can_returns_false_when_role_lacks_permission(self):
        Role.insert_roles()
        u = User(email='test@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        self.assertFalse(u.can(Permission.ADMIN))

    def test_is_administrator_returns_false_for_user_role(self):
        Role.insert_roles()
        u = User(email='test@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        self.assertFalse(u.is_administrator())

    def test_is_administrator_returns_true_for_admin_role(self):
        Role.insert_roles()
        r = Role.query.filter_by(name='Administrator').first()
        u = User(email='admin@example.com', password='cat', role=r)
        db.session.add(u)
        db.session.commit()
        self.assertTrue(u.is_administrator())
