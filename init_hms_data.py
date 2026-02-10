import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import Role, User, Hospital

roles = ['SUPER_ADMIN', 'HOSPITAL_ADMIN', 'DOCTOR', 'NURSE', 'PHARMACIST', 'RECEPTIONIST']
for r_name in roles:
    role, created = Role.objects.get_or_create(name=r_name)
    if created:
        print(f"Created role: {r_name}")

if not User.objects.filter(email='admin@chikitsaone.com').exists():
    User.objects.create_superuser('admin@chikitsaone.com', 'admin')
    print("Created superuser: admin@chikitsaone.com / admin")
else:
    print("Superuser exists.")

# Demo Hospital
hospital, created = Hospital.objects.get_or_create(
    name="ChikitsaOne Demo Hospital",
    defaults={
        'address': "123 Health St",
        'contact_details': "555-0199",
        'admin_email': "admin@demohospital.com",
        'phone': "555-1234",
        'license_number': "LIC-DEMO-001",
        'domain': "demo.chikitsaone.com",
        'status': "ACTIVE"
    }
)
if created:
    print(f"Created demo hospital: {hospital.name}")
