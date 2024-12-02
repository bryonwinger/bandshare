# import unittest
import datetime as dt

from django.test import TestCase
from django.core.exceptions import ValidationError

from bandshare.models.group import GroupMembership

# from django.utils import timezone

# Create your tests here.

from .models import (User, Group, GroupMembership, Genre, Location, Instrument, Artist, Song, Setlist,
                    TimeSignature, MusicalKey)

some_date = dt.date(1980, 1, 1)


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.jim = User.objects.create(first_name='Jim', last_name='Halpert',
                 display_name='OfficeJimmy123', birth_date=some_date,
                 description="One cool guy", bio="Meet Jim...")

        cls.group1 = Group.objects.create(name="Supergroup", created_by=cls.jim)
        cls.group2 = Group.objects.create(name="Local H", created_by=cls.jim)

        cls.genre1 = Genre.objects.create(name="Rock")
        cls.genre2 = Genre.objects.create(name="Pop")

        cls.location = Location.objects.create(state='California', city='Beverly Hills', postal_code='90210')
        cls.instrument1 = Instrument.objects.create(name='Guitar')
        cls.instrument2 = Instrument.objects.create(name='Voice')

    def test_clean_model(self):
        """
        Check clean model.
        """
        u = User(first_name='Bill', last_name='Nye',
                 display_name='bill_nye', birth_date=some_date,
                 location=self.location)
        self.assertEqual(None, u.full_clean())

    def test_required_fields(self):
        """
        Check required fields.
        """
        u = User(first_name=None, last_name='Nye',
                 display_name='bill_nye', birth_date=some_date)
        with self.assertRaisesRegex(ValidationError, "first_name"):
            u.full_clean()

        u = User(first_name='Bill', last_name=None,
                 display_name='bill_nye', birth_date=some_date)
        with self.assertRaisesRegex(ValidationError, "last_name"):
            u.full_clean()

        u = User(first_name='Bill', last_name='Nye',
                 display_name=None, birth_date=some_date)
        with self.assertRaisesRegex(ValidationError, "display_name"):
            u.full_clean()

        u = User(first_name='Bill', last_name='Nye',
                 display_name='bill_nye', birth_date=None)
        with self.assertRaisesRegex(ValidationError, "birth_date"):
            u.full_clean()

    def test_can_add_groups(self):
        self.jim.groups.add(self.group1, through_defaults={'role': 'Singer'})
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(1, self.jim.groups.count())

        self.jim.groups.add(self.group2, through_defaults={'role': 'Banjoist'})
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(2, self.jim.groups.count())

        # Entries are unique
        self.jim.groups.add(self.group2)
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
        self.jim.genres.add(self.genre1)
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(1, self.jim.genres.count())

        self.jim.genres.add(self.genre2)
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(2, self.jim.genres.count())

        # Entries are unique
        self.jim.genres.add(self.genre1)
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(2, self.jim.genres.count())

    def test_can_add_location(self):
        self.jim.location = self.location
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(self.jim.location, self.location)

    def test_can_add_instruments(self):
        self.jim.instruments.add(self.instrument1)
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(1, self.jim.instruments.count())

        self.jim.instruments.add(self.instrument2)
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(2, self.jim.instruments.count())

        # Entries are unique
        self.jim.instruments.add(self.instrument2)
        self.assertEqual(None, self.jim.full_clean())
        self.assertEqual(2, self.jim.instruments.count())


class GroupModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.jim = User.objects.create(first_name='Jim', last_name='Halpert',
                 display_name='OfficeJimmy123', birth_date=some_date)
        cls.rose = User.objects.create(first_name='Rose', last_name='Thorn',
                 display_name='rthorn88', birth_date=some_date)

        cls.group = Group.objects.create(name="Supergroup", description='A super group',
                                         bio='A band started so long ago...', created_by=cls.jim)

        cls.location = Location.objects.create(state='California', city='Beverly Hills', postal_code='90210')


    def test_clean_model(self):
        """
        Check clean model.
        """
        g = Group(name='The Beatless', location = self.location, created_by=self.jim)
        self.assertEqual(None, g.full_clean())
        # owned_by is added automatically
        self.assertEqual(g.owned_by, self.jim)

    def test_required_fields(self):
        """
        Check required fields.
        """
        g1 = Group(name=None, created_by=self.jim)
        with self.assertRaisesRegex(ValidationError, "name"):
            g1.full_clean()

        g2 = Group(name='My Group', created_by=None)
        with self.assertRaisesRegex(ValidationError, "created_by"):
            g2.full_clean()

    def test_can_add_member_to_group(self):
        "Can add a member (User) to a Group."
        self.group.members.add(self.jim, through_defaults={'role': 'Banjoist'})
        self.assertEqual(None, self.group.full_clean())
        self.assertEqual(1, self.group.members.count())
        self.assertIn({'user': self.jim, 'role': 'Banjoist'}, self.group.member_roles)

    def test_can_add_unique_members_to_group(self):
        "Can add additional members (User) to a Group only if they are unique."
        self.group.members.clear()
        self.assertEqual(0, self.group.members.count())

        self.group.members.add(self.jim, through_defaults={'role': 'Banjoist'})
        self.assertEqual(None, self.group.full_clean())
        self.assertEqual(1, self.group.members.count())

        self.group.members.add(self.rose, through_defaults={'role': 'Manager'})
        self.assertEqual(None, self.group.full_clean())
        self.assertEqual(2, self.group.members.count())
        self.assertIn({'user': self.rose, 'role': 'Manager'}, self.group.member_roles)

        # Will be ignored
        self.group.members.add(self.rose)
        self.assertEqual(None, self.group.full_clean())
        self.assertEqual(2, self.group.members.count())
        # Role did not change
        self.assertIn({'user': self.jim, 'role': 'Banjoist'}, self.group.member_roles)

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
        with self.assertRaisesRegex(ValidationError, "name"):
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
        loc = Location(name="My Location", state='Some State', city='My City', postal_code='12345')
        self.assertEqual(None, loc.full_clean())

    def test_is_unique_for_country_state_and_city(self):
        loc = Location(name="My Location", state=self.beverly_hills.state, city=self.beverly_hills.city,
                       postal_code=self.beverly_hills.postal_code)
        with self.assertRaisesRegex(ValidationError, "already exists"):
            loc.full_clean()

    def test_can_create_with_different_postal_code(self):
        loc = Location(name="Beverly Hills", state=self.beverly_hills.state, city=self.beverly_hills.city, postal_code='12345')
        self.assertEqual(None, loc.full_clean())

    def test_can_create_with_different_city(self):
        loc = Location(name="Beverly Hills", state=self.beverly_hills.state, city='Another City', postal_code=self.beverly_hills.postal_code)
        self.assertEqual(None, loc.full_clean())

    def test_can_create_with_different_state(self):
        loc = Location(name="Beverly Hills", state='Another State', city=self.beverly_hills.city, postal_code=self.beverly_hills.postal_code)
        self.assertEqual(None, loc.full_clean())


class InstrumentModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guitar = Instrument.objects.create(name='Lead Guitar')

    def test_clean_model(self):
        """
        Check clean model.
        """
        instrument = Instrument(name='Tenor Singer')
        self.assertEqual(None, instrument.full_clean())

    def test_is_unique(self):
        instrument = Instrument(name=self.guitar.name)
        with self.assertRaisesRegex(ValidationError, "already exists"):
            instrument.full_clean()


class ArtistModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dave = Artist.objects.create(name='Dave Matthews Band')

    def test_clean_model(self):
        """
        Check clean model.
        """
        artist = Artist(name='Beastie Boys')
        self.assertEqual(None, artist.full_clean())

    def test_required_fields(self):
        """
        Check required fields.
        """
        artist = Artist(name=None)
        with self.assertRaisesRegex(ValidationError, "name"):
            artist.full_clean()

        artist = Artist(name='')
        with self.assertRaisesRegex(ValidationError, "name"):
            artist.full_clean()

    def test_is_unique(self):
        artist = Artist(name=self.dave.name)
        with self.assertRaisesRegex(ValidationError, "already exists"):
            artist.full_clean()


class SongModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.existing_artist = Artist.objects.create(name="Throwing Muses")
        cls.existing_genre = Genre.objects.create(name="Indie Rock")
        cls.existing_song = Song.objects.create(title='Bright Yellow Gun', artist=cls.existing_artist)

    def test_clean_model(self):
        """
        Check clean model.
        """
        title = 'Somewhere Over The Rainbow'
        song = Song(title=title, artist=self.existing_artist)
        self.assertEqual(None, song.full_clean())
        self.assertEqual(None, song.release_date)
        self.assertEqual(self.existing_artist, song.artist)
        self.assertEqual('', song.musical_key)
        self.assertEqual('', song.time_signature)
        self.assertEqual(120, song.bpm)
        # self.assertEqual([], song.genres) # TODO: Figure this out

    def test_required_fields(self):
        """
        Check required fields.
        """
        song = Song(title=None)
        with self.assertRaisesRegex(ValidationError, "title"):
            song.full_clean()

        song = Song(title='')
        with self.assertRaisesRegex(ValidationError, "title"):
            song.full_clean()

    def test_can_have_many_with_same_title(self):
        song = Song(title=self.existing_song.title, artist=self.existing_artist)
        self.assertEqual(None, song.full_clean())

    def test_other_fields(self):
        title = "Watching Strangers Smile"
        release_date = dt.date(2019, 12, 4)
        musical_key = MusicalKey.F_Major
        time_signature = TimeSignature.Three_Four
        bpm = 118
        duration_seconds = dt.timedelta(minutes=3, seconds=15)

        song = Song(title = title, release_date = release_date, musical_key = musical_key,
                    artist = self.existing_artist, time_signature = time_signature, bpm = bpm,
                    duration_seconds = duration_seconds)
        self.assertEqual(None, song.full_clean())
        #song.genres.add(self.existing_genre)

        self.assertEqual(title, song.title)
        self.assertEqual(release_date, song.release_date)
        self.assertEqual(musical_key, song.musical_key)
        self.assertEqual(time_signature, song.time_signature)
        self.assertEqual(bpm, song.bpm)
        self.assertEqual(duration_seconds, song.duration_seconds)
