from django.db import models
from django.conf import settings

class Patient(models.Model):
    hospital = models.ForeignKey('accounts.Hospital', on_delete=models.CASCADE, related_name='patients', null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('B+', 'B+'), ('O+', 'O+'), ('AB+', 'AB+'),
        ('A-', 'A-'), ('B-', 'B-'), ('O-', 'O-'), ('AB-', 'AB-'),
    ]

    idno = models.CharField(max_length=12, primary_key=True, verbose_name="Adhaar No")
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=10)
    bg = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, verbose_name="Blood Group")

    def __str__(self):
        return f"{self.name} ({self.idno})"

class Doctor(models.Model):
    hospital = models.ForeignKey('accounts.Hospital', on_delete=models.CASCADE, related_name='doctors', null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_profile')
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    room_no = models.IntegerField()
    doctor_id = models.IntegerField(unique=True) # e.g. 7001
    
    def __str__(self):
        return f"{self.name} - {self.department}"

class Service(models.Model):
    hospital = models.ForeignKey('accounts.Hospital', on_delete=models.CASCADE, related_name='services', null=True, blank=True)
    name = models.CharField(max_length=50)
    room_no = models.IntegerField()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    hospital = models.ForeignKey('accounts.Hospital', on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    appointment_no = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')

    def __str__(self):
        return f"Appt {self.appointment_no}: {self.patient.name} with {self.doctor.name}"
