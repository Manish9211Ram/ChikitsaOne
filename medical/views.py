from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Patient, Doctor, Service, Appointment
import datetime
import random

# Quotes from the original script
QUOTES = [
    ("BEAUTIFUL THINGS HAPPEN WHEN YOU DISTANCE YOURSELF FROM NEGATIVITY", "Negativity"),
    ("DREAMS ARE NOT WHAT YOU SEE WHEN YOU SLEEP, DREAMS ARE THOSE WHICH DON'T LET YOU SLEEP", "Dreams"),
    ("YOU ONLY LIVE ONCE. BUT IF YOU DO IT RIGHT, ONCE IS ENOUGH", "YOLO"),
    ("THE EXPERT IN ANYTHING WAS ONCE A BEGINNER", "Growth"),
    ("NOT ALL STORMS COME TO DISRUPT YOUR LIFE SOME COME TO CLEAR YOUR PATH", "Resilience"),
    ("LISTEN TO EVERYONE AND LEARN FROM EVERYONE, BECAUSE NOBODY KNOWS EVERYTHING BUT EVERYONE KNOWS SOMETHING", "Wisdom"),
    ("ONE KIND WORD CAN CHANGE SOMEONE'S ENTIRE DAY", "Kindness"),
    ("GOOD MANNERS AND KINDNESS ARE ALWAYS IN FASHION", "Manners"),
]

def get_common_context():
    quote = random.choice(QUOTES)
    return {
        'date': datetime.date.today(),
        'time': datetime.datetime.now(),
        'quote': quote[0]
    }

def home(request):
    context = get_common_context()
    return render(request, 'medical/index.html', context)

def patient_register(request):
    if request.method == 'POST':
        idno = request.POST.get('idno')
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        bg = request.POST.get('bg')

        if len(idno) != 12:
            messages.error(request, "Adhaar must be 12 digits")
            return redirect('register')
        
        # Check if already exists
        if Patient.objects.filter(idno=idno).exists():
             messages.error(request, "Patient with this Adhaar already exists")
             return redirect('register')

        Patient.objects.create(
            idno=idno, name=name, age=age, gender=gender,
            phone=phone, bg=bg
        )
        messages.success(request, f"Registered successfully! ID: {idno}")
        return redirect('home')

    return render(request, 'medical/register.html', get_common_context())

def doctor_list(request):
    doctors = Doctor.objects.all()
    # If no doctors (first run), populate some
    if not doctors.exists():
        populate_initial_data()
        doctors = Doctor.objects.all()
        
    return render(request, 'medical/doctor_list.html', {'doctors': doctors})

def service_list(request):
    services = Service.objects.all()
    if not services.exists():
        populate_services()
        services = Service.objects.all()
    return render(request, 'medical/service_list.html', {'services': services})

def book_appointment_search(request):
    if request.method == 'POST':
        idno = request.POST.get('idno')
        try:
            patient = Patient.objects.get(idno=idno)
            request.session['patient_id'] = idno
            return redirect('book_appointment_select')
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found. Please register first.")
            return redirect('appointment_search')
            
    return render(request, 'medical/appointment_search.html', get_common_context())

def book_appointment_select(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('appointment_search')
    
    # Get distinct departments
    departments = Doctor.objects.values_list('department', flat=True).distinct()
    
    if request.method == 'POST':
        dept = request.POST.get('department')
        doctors = Doctor.objects.filter(department=dept)
        if doctors.exists():
            doctor = random.choice(doctors)
            appointment_no = random.randint(10, 99)
            
            # Logic from original script
            delays = {
                'Cardiologist': 3,
                'Rheumatologist': 5,
                'Psychiatrist': 3,
                'Neurologist': 6,
                'Otolaryngonologist': 4,
                'MI Room': 1
            }
            # Default to 1 day if not found
            days_offset = delays.get(dept, 1)
            
            appt_date = datetime.date.today() + datetime.timedelta(days=days_offset)
            
            patient = Patient.objects.get(idno=patient_id)
            
            appt = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date=appt_date,
                appointment_no=appointment_no
            )
            
            return render(request, 'medical/appointment_success.html', {'appt': appt})
        else:
            messages.error(request, "No doctors available in this department.")

    return render(request, 'medical/book_appointment.html', {'departments': departments})

def doctor_login(request):
    if request.method == 'POST':
        doc_id = request.POST.get('doctor_id')
        password = request.POST.get('password')
        
        # Simple password check: password must equal '7000' + ID or similar logic from script
        # Script logic: Dr 1 (Varun, 7001) -> password must be 7001. So pwd models ID.
        try:
            doctor = Doctor.objects.get(doctor_id=doc_id)
            if int(password) == int(doc_id): # The script used ID as password basically
                request.session['doctor_id'] = doc_id
                return redirect('doctor_dashboard')
            else:
                messages.error(request, "Invalid Password")
        except Doctor.DoesNotExist:
            messages.error(request, "Invalid Doctor ID")
            
    return render(request, 'medical/doctor_login.html')

def doctor_dashboard(request):
    doc_id = request.session.get('doctor_id')
    if not doc_id:
        return redirect('doctor_login')
    
    doctor = get_object_or_404(Doctor, doctor_id=doc_id)
    # The script showed random fake appointments. 
    # We will show REAL appointments if we have them, or mock ones if we follow the script blindly?
    # Better to show real ones created by users.
    appointments = Appointment.objects.filter(doctor=doctor)
    
    return render(request, 'medical/doctor_dashboard.html', {'doctor': doctor, 'appointments': appointments})

def all_records(request):
    patients = Patient.objects.all()
    return render(request, 'medical/all_records.html', {'patients': patients})

# Helper to populate data if empty
def populate_initial_data():
    docs_data = [
        ("Dr. Varun", "Cardiologist", 201, 7001),
        ("Dr. Hrithik", "Cardiologist", 202, 7002),
        ("Dr. Salman", "Psychiatrist", 203, 7003),
        ("Dr. Shahrukh", "Psychiatrist", 204, 7004),
        ("Dr. Akshay", "Otolaryngonologist", 205, 7005),
        ("Dr. Amir", "Otolaryngonologist", 206, 7006),
        ("Dr. Sidharth", "Rheumatologist", 207, 7007),
        ("Dr. Abhishek", "Rheumatologist", 208, 7008),
        ("Dr. Ajay", "Neurologist", 209, 7009),
        ("Dr. Ranveer", "Neurologist", 200, 7010),
        ("Dr. Irfan", "MI Room", 1, 7011),
        ("Dr. John", "MI Room", 2, 7012),
        ("Dr. Sanjay", "MI Room", 3, 7013),
        ("Dr. Shahid", "MI Room", 4, 7014),
    ]
    for name, dept, room, did in docs_data:
        Doctor.objects.update_or_create(
            doctor_id=did, 
            defaults={'name': name, 'department': dept, 'room_no': room}
        )

def populate_services():
    services_data = [
        ("X-Ray", 101), ("MRI", 102), ("CT Scan", 103), ("Endoscopy", 104),
        ("Dialysis", 105), ("Ultrasound", 301), ("EEG", 302), ("ENMG", 303), ("ECG", 304)
    ]
    for name, room in services_data:
        Service.objects.get_or_create(name=name, defaults={'room_no': room})

def update_patient_search(request):
    if request.method == 'POST':
        idno = request.POST.get('idno')
        try:
            patient = Patient.objects.get(idno=idno)
            request.session['update_patient_id'] = idno
            return redirect('update_patient_form')
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found.")
            return redirect('update_patient_search')
    return render(request, 'medical/update_search.html', get_common_context())

def update_patient_form(request):
    pid = request.session.get('update_patient_id')
    if not pid:
        return redirect('update_patient_search')
    
    patient = get_object_or_404(Patient, idno=pid)
    
    if request.method == 'POST':
        patient.name = request.POST.get('name')
        patient.age = request.POST.get('age')
        patient.gender = request.POST.get('gender')
        patient.phone = request.POST.get('phone')
        patient.bg = request.POST.get('bg')
        patient.save()
        messages.success(request, "Patient details updated successfully!")
        return redirect('home')

    return render(request, 'medical/update_form.html', {'patient': patient})

