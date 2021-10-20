# import unittest
import datetime as dt

from django.test import TestCase
from django.core.exceptions import ValidationError

# from django.utils import timezone

# Create your tests here.

from .models import User, Group, Genre, Location

some_date = dt.date(1980, 1, 1)


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.jim = User.objects.create(first_name='Jim', last_name='Halpert',
                 display_name='OfficeJimmy123', birth_date=some_date,
                 description="One cool guy", bio="Meet Jim...")

        cls.location = Location.objects.create(state='California', city='Beverly Hills', postal_code='90210')

    def test_clean_model(self):
        """
        Check clean model.
        """
        u = User(first_name='Bill', last_name='Nye',
                 display_name='bill_nye', birth_date=some_date,
                 location=self.location )
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

    def test_can_add_genres(self):
        g1 = Genre.objects.create(name="Rock")
        self.jim.genres.add(g1)
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(1, self.jim.genres.count())

        g2 = Genre.objects.create(name="Pop")
        self.jim.genres.add(g2)
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(2, self.jim.genres.count())

        # Entries are unique
        self.jim.genres.add(g2)
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(2, self.jim.genres.count())

    def test_can_add_location(self):
        self.jim.location = self.location
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(self.jim.location, self.location)


class GroupModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.jim = User.objects.create(first_name='Jim', last_name='Halpert',
                 display_name='OfficeJimmy123', birth_date=some_date)
        cls.rose = User.objects.create(first_name='Rose', last_name='Thorn',
                 display_name='rthorn88', birth_date=some_date)

        cls.group = Group.objects.create(name="Supergroup", description='A super group',
                                         bio='A band started so long ago...')

        cls.location = Location.objects.create(state='California', city='Beverly Hills', postal_code='90210')


    def test_clean_model(self):
        """
        Check clean model.
        """
        g = Group(name='The Beatless', location = self.location)
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

    def test_can_add_genres_to_group(self):
        g1 = Genre.objects.create(name="Rock")
        self.group.genres.add(g1)
        self.assertEqual(None, self.group.full_clean())
        self.assertEqual(1, self.group.genres.count())

        g2 = Genre.objects.create(name="Pop")
        self.group.genres.add(g2)
        self.assertEqual(None, self.group.full_clean())
        self.assertEqual(2, self.group.genres.count())

        # Entries are unique
        self.group.genres.add(g2)
        self.assertEqual(None, self.group.full_clean())
        self.assertEqual(2, self.group.genres.count())

    def test_can_add_location(self):
        self.group.location = self.location
        self.assertEqual(None, self.group.full_clean())
        self.assertEqual(self.group.location, self.location)


class GenreModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rock = Genre.objects.create(name="Rock")

    def test_clean_model(self):
        """
        Check clean model.
        """
        g = Genre(name="Pop")
        self.assertEqual(None, g.full_clean())

    def test_name_is_unique(self):
        g = Genre(name=self.rock.name)
        with self.assertRaisesRegexp(ValidationError, "name"):
            g.full_clean()


class LocationModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.beverly_hills = Location.objects.create(state='California', city='Beverly Hills', postal_code='90210')
        cls.nashville = Location.objects.create(state='Tenneesee', city='Nashville', postal_code='37203')
        cls.toronto = Location.objects.create(country='Canada', state='Ontario', city='Toronto', postal_code='M4C 3C5')

    def test_clean_model(self):
        """
        Check clean model.
        """
        loc = Location(state='Some State', city='My City', postal_code='12345')
        self.assertEqual(None, loc.full_clean())

    def test_is_unique_for_country_state_and_city(self):
        loc = Location(state=self.beverly_hills.state, city=self.beverly_hills.city,
                       postal_code=self.beverly_hills.postal_code)
        with self.assertRaisesRegexp(ValidationError, "already exists"):
            loc.full_clean()

    def test_can_create_with_different_postal_code(self):
        loc = Location(state=self.beverly_hills.state, city=self.beverly_hills.city, postal_code='12345')
        self.assertEqual(None, loc.full_clean())

    def test_can_create_with_different_city(self):
        loc = Location(state=self.beverly_hills.state, city='Another City', postal_code=self.beverly_hills.postal_code)
        self.assertEqual(None, loc.full_clean())

    def test_can_create_with_different_state(self):
        loc = Location(state='Another State', city=self.beverly_hills.city, postal_code=self.beverly_hills.postal_code)
        self.assertEqual(None, loc.full_clean())
