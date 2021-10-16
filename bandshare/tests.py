# import unittest
import datetime as dt

from django.test import TestCase
from django.core.exceptions import ValidationError
# from django.utils import timezone

# Create your tests here.

from .models import User, Group

some_date = dt.date(1980, 1, 1)


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.jim = User.objects.create(first_name='Jim', last_name='Halpert',
                 display_name='OfficeJimmy123', birth_date=some_date)

    def test_clean_model(self):
        """
        Check clean model.
        """
        u = User(first_name='Bill', last_name='Nye',
                 display_name='bill_nye', birth_date=some_date)
        self.assertEqual(None, u.full_clean())

    def test_required_fields(self):
        """
        Check required fields.
        """
        u = User(first_name=None, last_name='Nye',
                 display_name='bill_nye', birth_date=some_date)
        with self.assertRaisesRegexp(ValidationError, "first_name"):
            u.full_clean()

        u = User(first_name='Bill', last_name=None,
                 display_name='bill_nye', birth_date=some_date)
        with self.assertRaisesRegexp(ValidationError, "last_name"):
            u.full_clean()

        u = User(first_name='Bill', last_name='Nye',
                 display_name=None, birth_date=some_date)
        with self.assertRaisesRegexp(ValidationError, "display_name"):
            u.full_clean()

        u = User(first_name='Bill', last_name='Nye',
                 display_name='bill_nye', birth_date=None)
        with self.assertRaisesRegexp(ValidationError, "birth_date"):
            u.full_clean()

    def test_optional_fields(self):
        """
        Check optional fields.
        """
        pass

    def test_can_add_groups(self):
        g1 =  Group.objects.create(name="Supergroup")
        self.jim.groups.add(g1)
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(1, self.jim.groups.count())

        g2 =  Group.objects.create(name="Local H")
        self.jim.groups.add(g2)
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(2, self.jim.groups.count())

        # Entries are unique
        self.jim.groups.add(g2)
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(2, self.jim.groups.count())

    def test_full_name(self):
        first = self.jim.first_name
        last = self.jim.last_name
        self.assertEqual(self.jim.full_name, f"{first} {last}")

    def test_age(self):
        today = dt.datetime.now().date()
        y, m, d = today.year, today.month, today.day

        for i in range(1, 20):
            new_year = today.year - (i * 3)
            new_date = dt.date(new_year, today.month, today.day)
            u = User(birth_date=new_date)
            self.assertEqual(u.age, i * 3)


class GroupModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.jim = User.objects.create(first_name='Jim', last_name='Halpert',
                 display_name='OfficeJimmy123', birth_date=some_date)
        cls.rose = User.objects.create(first_name='Rose', last_name='Thorn',
                 display_name='rthorn88', birth_date=some_date)

        cls.group = Group.objects.create(name="Supergroup")

    def test_clean_model(self):
        """
        Check clean model.
        """
        g = Group(name='The Beatless')
        self.assertEqual(None, g.full_clean())

    def test_required_fields(self):
        """
        Check required fields.
        """
        g = Group(name=None)
        with self.assertRaisesRegexp(ValidationError, "name"):
            g.full_clean()

    def test_can_add_member_to_group(self):
        "Can add a member (User) to a Group."
        self.group.members.add(self.jim)
        self.assertEqual(None, self.group.full_clean())
        self.assertEqual(1, self.group.members.count())

    def test_can_add_unique_members_to_group(self):
        "Can add additional members (User) to a Group only if they are unique."
        self.group.members.clear()
        self.assertEqual(0, self.group.members.count())

        self.group.members.add(self.jim)
        self.assertEqual(None, self.group.full_clean())
        self.assertEqual(1, self.group.members.count())

        self.group.members.add(self.rose)
        self.assertEqual(None, self.group.full_clean())
        self.assertEqual(2, self.group.members.count())

        # Will be ignored
        self.group.members.add(self.rose)
        self.assertEqual(None, self.group.full_clean())
        self.assertEqual(2, self.group.members.count())
