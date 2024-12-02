from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator

from datetime import timedelta

class SongKey(models.TextChoices):
    NOT_SPECIFIED = ''
    A_Major = 'A'
    Bb_Major = 'B♭'
    B_Major = 'B'
    C_Major = 'C'
    Db_Major = 'D♭'
    D_Major = 'D'
    Eb_Major = 'E♭'
    E_Major = 'E'
    F_Major = 'F'
    Fs_Major = 'F♯'
    G_Major = 'G'
    Ab_Major = 'A♭'
    A_Minor = 'Am'
    Bb_Minor = 'B♭m'
    B_Minor = 'Bm'
    C_Minor = 'Cm'
    Cs_Minor = 'C♯m'
    D_Minor = 'Dm'
    Ds_Minor = 'D♯m'
    E_Minor = 'Em'
    F_Minor = 'Fm'
    Fs_Minor = 'F♯m'
    G_Minor = 'Gm'
    Gs_Minor = 'G♯m'


class TimeSignature(models.TextChoices):
    NOT_SPECIFIED = ''
    Two_Two = '2/2'
    Two_Four = '2/4'
    Three_Four = '3/4'
    Four_Four = '4/4'
    Six_Eight = '6/8'
    Nine_Eight = '9/8'
    Twelve_Eight = '12/8'
    Five_Four = '5/4'
    # Eleven_Four = '11/4'
    # Five_Eight = '5/8'


MIN_BPM = 40
MAX_BPM = 300

class Song(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=256)
    release_date = models.DateTimeField(auto_now=True)
    
    artist = models.ManyToManyField('Artist')
    key = models.CharField(max_length=3, choices=SongKey.choices, default=SongKey.NOT_SPECIFIED)
    time_signature = models.CharField(max_length=4, choices=TimeSignature.choices, default=TimeSignature.Four_Four)
    genres = models.ManyToManyField('Genre')
    bpm = models.IntegerField(validators=[MinValueValidator(MIN_BPM), MaxValueValidator(MAX_BPM)], default=120)

    time_seconds = models.DurationField(
        default=timedelta(minutes=3, seconds=0),
        validators=[MaxValueValidator(timedelta(minutes=60))]
    )

    def __str__(self):
        return self.title
    
    @property
    def length(self):
        """Returns a string of the song's runtime."""
        minutes = int(self.time_seconds.total_seconds()) // 60
        seconds = self.time_seconds.seconds
        ms = self.time_seconds.microseconds
        return f"{minutes}:{seconds}:{ms}"

