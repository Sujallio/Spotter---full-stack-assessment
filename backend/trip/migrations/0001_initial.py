# Generated migration file for trip app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_location', models.CharField(max_length=255)),
                ('current_lat', models.FloatField(blank=True, null=True)),
                ('current_lng', models.FloatField(blank=True, null=True)),
                ('pickup_location', models.CharField(max_length=255)),
                ('pickup_lat', models.FloatField(blank=True, null=True)),
                ('pickup_lng', models.FloatField(blank=True, null=True)),
                ('dropoff_location', models.CharField(max_length=255)),
                ('dropoff_lat', models.FloatField(blank=True, null=True)),
                ('dropoff_lng', models.FloatField(blank=True, null=True)),
                ('current_cycle_used', models.FloatField(default=0)),
                ('route_distance', models.FloatField(blank=True, null=True)),
                ('estimated_duration', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ELDLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_date', models.DateField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('OFF', 'Off Duty'), ('SB', 'Sleeper Berth'), ('DRIVING', 'Driving'), ('ON', 'On Duty (Not Driving)')], max_length=10)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('miles_driven', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eld_logs', to='trip.trip')),
            ],
            options={
                'ordering': ['log_date', 'start_time'],
            },
        ),
    ]
