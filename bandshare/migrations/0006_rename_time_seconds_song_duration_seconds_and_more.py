# Generated by Django 5.1.3 on 2024-12-02 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bandshare', '0005_setlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='time_seconds',
            new_name='duration_seconds',
        ),
        migrations.RenameField(
            model_name='song',
            old_name='key',
            new_name='musical_key',
        ),
        migrations.RemoveField(
            model_name='song',
            name='artist',
        ),
        migrations.AlterField(
            model_name='song',
            name='musical_key',
            field=models.CharField(blank=True, choices=[('', 'Not Specified'), ('A', 'A Major'), ('B♭', 'Bb Major'), ('B', 'B Major'), ('C', 'C Major'), ('D♭', 'Db Major'), ('D', 'D Major'), ('E♭', 'Eb Major'), ('E', 'E Major'), ('F', 'F Major'), ('F♯', 'Fs Major'), ('G', 'G Major'), ('A♭', 'Ab Major'), ('Am', 'A Minor'), ('B♭m', 'Bb Minor'), ('Bm', 'B Minor'), ('Cm', 'C Minor'), ('C♯m', 'Cs Minor'), ('Dm', 'D Minor'), ('D♯m', 'Ds Minor'), ('Em', 'E Minor'), ('Fm', 'F Minor'), ('F♯m', 'Fs Minor'), ('Gm', 'G Minor'), ('G♯m', 'Gs Minor')], default='', max_length=3),
        ),
        migrations.AlterField(
            model_name='song',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='time_signature',
            field=models.CharField(blank=True, choices=[('', 'Not Specified'), ('2/2', 'Two Two'), ('2/4', 'Two Four'), ('3/4', 'Three Four'), ('4/4', 'Four Four'), ('6/8', 'Six Eight'), ('9/8', 'Nine Eight'), ('12/8', 'Twelve Eight'), ('5/4', 'Five Four')], default='', max_length=4),
        ),
        migrations.AddField(
            model_name='song',
            name='artist',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='bandshare.artist'),
            preserve_default=False,
        ),
    ]