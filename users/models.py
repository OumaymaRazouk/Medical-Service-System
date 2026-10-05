from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Patient(models.Model):
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    name = models.CharField(max_length=45)
    date_of_birth = models.DateField()
    origin = models.CharField(max_length=45,blank=True, null=True)
    address = models.TextField(max_length=100,blank=True, null=True)
    family_status = models.CharField(max_length=45, choices=[
    ('single', 'Single'),
    ('married', 'Married'),
    ('divorced', 'Divorced'),
    ('widowed', 'Widowed'),
    ],default="Single")
    company = models.CharField(max_length=45, choices=[
    ('Nomac', 'Nomac'),
    ('Sener', 'Sener'),
    ('ACWA Power', 'ACWA Power'),
    ])
    start_date = models.DateField()
    department = models.CharField(max_length=45,blank=True, null=True)
    job_position = models.CharField(max_length=45,blank=True, null=True)
    photo = models.ImageField(upload_to='user_photos/',blank=True, null=True)
    AREA_CHOICES = [
        ('CCR', 'CCR'),
        ('SOLAR FIELD', 'SOLAR FIELD'),
        ('ADMINISTRATION OFFICE', 'ADMINISTRATION OFFICE'),
        ('WTP', 'WTP'),
        ('WORKSHOP', 'WORKSHOP'),
        ('WAREHOUSE', 'WAREHOUSE'),
    ]
        

    area = models.CharField(max_length=45, choices=AREA_CHOICES, blank=True, null=True)
    risk = models.FileField(upload_to='risk_files/', blank=True, null=True)

    def __str__(self):
        return self.name
from django.db import models
from django.utils import timezone
from datetime import date
from datetime import timedelta


class Medicine(models.Model):
    N_lot = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    reception_date = models.DateField(default=date.today)
    expiration_date = models.DateField()
    presentation = models.CharField(max_length=200, blank=True, null=True)
    dosage = models.CharField(max_length=50, blank=True, null=True)

    @property
    def status(self):
        if self.quantity == 0:
            return 'Low Stock'
        if self.expiration_date < timezone.now().date():
            return 'Expired'
        elif self.expiration_date - timezone.now().date() <= timedelta(days=60):
            return 'Expiring Soon'
        else:
            return 'Active'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:  # Check if the instance already exists (update)
            quantity_change = self.quantity
            action = 'Update'
        else:
            quantity_change = self.quantity
            action = 'Add'

        super(Medicine, self).save(*args, **kwargs)
        MedicineStockMovement.objects.create(
            medicine=self,
            action=action,
            quantity_change=quantity_change
        )

    def delete(self, *args, **kwargs):
        quantity_change = -self.quantity  # Subtract the quantity for deletion
        MedicineStockMovement.objects.create(
            medicine=self,
            action='Delete',
            quantity_change=quantity_change
        )
        super(Medicine, self).delete(*args, **kwargs)


class AmbulanceItem(models.Model):
    # Define the fields for the AmbulanceItem model
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    purchase_date = models.DateField()
    est_verifie = models.BooleanField(default=False)  # Champ pour indiquer si l'article a été vérifié

    def __str__(self):
        return self.name


class AmbulanceMedicine(models.Model):
    N_lot = models.CharField(max_length=50, unique=True)  # Serial number of the item
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    reception_date = models.DateField(default=date.today)
    expiration_date = models.DateField()
    presentation = models.CharField(max_length=200, blank=True, null=True)
    dosage = models.CharField(max_length=50, blank=True, null=True)
    est_verifie = models.BooleanField(default=False)  # Champ pour indiquer si l'article a été vérifié

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Expires Soon', 'Expires Soon (2 months)')
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class CheckInHistory(models.Model):
    date_sauvegarde = models.DateTimeField(auto_now_add=True)
    file_pdf = models.FileField(upload_to='check_in_Histories/', blank=True, null=True)
    remark_item = models.CharField(max_length=500, blank=True, null=True)
    remark_medicine = models.CharField(max_length=500, blank=True, null=True)
    other_file = models.FileField(upload_to='other_files/', blank=True, null=True)

    def __str__(self):
        return f"Log {self.pk}"


##############################################################################
from django.db import models


class VisiteMedicaleSpontanee(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visit_date = models.DateField()
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    blood_pressure = models.CharField(max_length=20)
    oxygen_saturation = models.DecimalField(max_digits=5, decimal_places=2)
    heart_rate = models.PositiveIntegerField()
    blood_glucose = models.DecimalField(max_digits=6, decimal_places=2)
    symptoms = models.TextField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.pk


#################Out#########################
class OutStockMedicine(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    remark = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(OutStockMedicine, self).save(*args, **kwargs)
        # Update the medicine's quantity
        self.medicine.quantity -= self.quantity
        self.medicine.save()  # Save the updated quantity
        MedicineStockMovement.objects.create(
            medicine=self.medicine,
            action='OUT',
            quantity_change=-self.quantity  # Note the negative sign here
        )

    def __str__(self):
        return f"{self.patient.name} - {self.medicine.name}"
    ###########Dossier medcial#######################"""


class DossierMedical(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.numero} - {self.patient.name}"


class info(models.Model):
    singuins = (
        ('O-', 'O-'),
        ('O+', 'O+'),
        ('B-', 'B-'),
        ('B+', 'B+'),
        ('A-', 'A-'),
        ('A+', 'A+'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    groupe_singuins = models.CharField(max_length=3, choices=singuins, default='RAS')
    situation_militaire = models.CharField(max_length=40, default='RAS')
    maladies = models.CharField(max_length=40, default='RAS')
    intervention_chirurgicales = models.CharField(max_length=10, default='RAS')
    accidents = models.CharField(max_length=40, default='RAS')
    accidents_travail = models.CharField(max_length=40, default='RAS')
    maladies_prof = models.CharField(max_length=40, default='RAS')
    compagnes = models.CharField(max_length=40, default='RAS')
    blessures = models.CharField(max_length=40, default='RAS')
    IPP = models.CharField(max_length=40, default='RAS')
    ant_pere = models.CharField(max_length=40, default='RAS')
    ant_mere = models.CharField(max_length=40, default='RAS')
    ant_freres = models.CharField(max_length=40, default='RAS')
    ant_soeurs = models.CharField(max_length=40, default='RAS')
    ant_conjoint = models.CharField(max_length=40, default='RAS')
    ant_enfant = models.CharField(max_length=40, default='RAS')
    ant_professionneles = models.CharField(max_length=100, default='RAS')
    # vaccination
    variole = models.CharField(max_length=10, default='RAS')
    diphterie = models.CharField(max_length=10, default='RAS')
    tetanos = models.CharField(max_length=10, default='RAS')
    tab = models.CharField(max_length=10, default='RAS')
    tabdt = models.CharField(max_length=10, default='RAS')
    autres = models.CharField(max_length=10, default='RAS')
    serum = models.CharField(max_length=10, default='RAS')


class Analyse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Radio(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# EXAMEN INITIAL
class systematique(models.Model):
    SANG_CHOICES = (
        ('GB', 'GB'),
        ('HB', 'HB'),
        ('plq', 'plq'),
        ('lympho', 'lympho'),
    )

    SITUATION_CHOICES = (
        ('apte', 'apte'),
        ('inapte', 'inapte'),
        ('inapte_temp', 'inapte temporairement'),
    )

    SURVEILLANCE_CHOICES = (
        ('1mois', '1 month'),
        ('2mois', '2 months'),
        ('3mois', '3 months'),
        ('4mois', '4 months'),
        ('5mois', '5 months'),
        ('6mois', '6 months'),
        ('7mois', '7 months'),
        ('8mois', '8 months'),
        ('9mois', '9 months'),
        ('10mois', '10 months'),
        ('11mois', '11 months'),
        ('12mois', '12 months'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    analyses = models.ManyToManyField(Analyse, blank=False)
    radios = models.ManyToManyField(Radio, blank=False)
    date = models.DateField(default=timezone.now)
    denture = models.CharField(max_length=20, default='RAS')
    audition_od = models.CharField(max_length=20, default='RAS')
    audition_og = models.CharField(max_length=20, default='RAS')
    vision_od = models.CharField(max_length=20, default='RAS')
    vision_og = models.CharField(max_length=20, default='RAS')
    taille = models.CharField(max_length=20, default='RAS')
    poids = models.CharField(max_length=20, default='RAS')
    per_thor = models.CharField(max_length=20, default='RAS')
    cap_resp = models.CharField(max_length=20, default='RAS')
    peau_phaneres = models.CharField(max_length=20, default='RAS')
    locomateur = models.CharField(max_length=20, default='RAS')
    dynamometre = models.CharField(max_length=20, default='RAS')
    respiratoire = models.CharField(max_length=20, default='RAS')
    radioscopique = models.CharField(max_length=20, default='RAS')
    controle = models.CharField(max_length=20, default='RAS')
    vaisseaux = models.CharField(max_length=20, default='RAS')
    varices = models.CharField(max_length=20, default='RAS')
    coeur = models.CharField(max_length=20, default='RAS')
    gangalions = models.CharField(max_length=20, default='RAS')
    pouls = models.CharField(max_length=20, default='RAS')
    TA = models.CharField(max_length=20, default='RAS')
    abdomen = models.CharField(max_length=20, default='RAS')
    foie = models.CharField(max_length=20, default='RAS')
    bouche = models.CharField(max_length=20, default='RAS')
    rate = models.CharField(max_length=20, default='RAS')
    amygdales = models.CharField(max_length=20, default='RAS')
    hernies = models.CharField(max_length=20, default='RAS')
    cicatrice = models.CharField(max_length=20, default='RAS')
    blenno = models.CharField(max_length=20, default='RAS')
    regles = models.CharField(max_length=20, default='RAS')
    albumine = models.CharField(max_length=20, default='RAS')
    sucre = models.CharField(max_length=20, default='RAS')
    neuro_psychisme = models.CharField(max_length=20, default='RAS')
    nervosisme = models.CharField(max_length=20, default='RAS')
    tremblement = models.CharField(max_length=20, default='RAS')
    equilibre = models.CharField(max_length=20, default='RAS')
    romberg = models.CharField(max_length=20, default='RAS')
    reflxes_oc = models.CharField(max_length=20, default='RAS')
    reflexes_trend = models.CharField(max_length=20, default='RAS')
    cutt = models.CharField(max_length=20, default='RAS')
    sedimenation = models.CharField(max_length=20, default='RAS')
    crachat = models.CharField(max_length=20, default='RAS')
    selle = models.CharField(max_length=20, default='RAS')
    urines = models.CharField(max_length=20, default='RAS')
    sang = models.CharField(max_length=20, choices=SANG_CHOICES, default='RAS')
    GB = models.CharField(max_length=20, default='RAS')
    HB = models.CharField(max_length=20, default='RAS')
    lympho = models.CharField(max_length=20, default='RAS')
    plq = models.CharField(max_length=20, default='RAS')
    situation = models.CharField(max_length=20, choices=SITUATION_CHOICES, default='RAS')
    surveiller = models.CharField(max_length=20, choices=SURVEILLANCE_CHOICES, default='RAS')
    commentaire = models.TextField(max_length=100, default='RAS')


from django.db import models
from django.utils import timezone


class MedicineStockMovement(models.Model):
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=20)  # Add/Delete/Update/Assignment
    quantity_change = models.IntegerField()

    def __str__(self):
        return f"{self.medicine.name} - {self.action} - {self.timestamp}"


class VisiteReprise(models.Model):
    CHOICES = (
        #('apte', 'L\'employé est apte à reprendre son travail'),
        #('Inapte_t', 'L\'employé est Inapte temporairement à reprendre son travail'),
        #('Inapte_d', 'L\'employé est Inapte définitivement à reprendre son travail'),
        ('fit', 'The employee is fit to return to work'),
        ('unfit_temporary', 'The employee is unfit temporarily to return to work'),
        ('unfit_permanent', 'The employee is unfit permanently to return to work'),
    )
    date = models.DateField(default=timezone.now)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visites_reprise')
    choix = models.CharField(max_length=50, choices=CHOICES)
    date = models.DateField(default=timezone.now)
    texte_certificat = models.TextField()

    # Add other fields as needed
    def month(self):
        return self.date.month

    def __str__(self):
        return f"{self.choix} - {self.date}"


class surveillance(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    taille = models.DecimalField(max_digits=8, decimal_places=3)
    poids = models.DecimalField(max_digits=8, decimal_places=3)
    T_A = models.DecimalField(max_digits=8, decimal_places=3)
    A_V = models.DecimalField(max_digits=8, decimal_places=3)
    pouls = models.DecimalField(max_digits=8, decimal_places=3)
    Glycemie = models.DecimalField(max_digits=8, decimal_places=3)
    Albumin = models.DecimalField(max_digits=8, decimal_places=3)
    Glucose = models.DecimalField(max_digits=8, decimal_places=3)
    Medecin_de_travail = models.CharField(max_length=20)


# models.py
class Laboratoire(models.Model):
    systematique = models.ForeignKey(systematique, on_delete=models.CASCADE)
    analyse = models.ForeignKey(Analyse, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='analyses/')


class LaboratoireRad(models.Model):
    systematique = models.ForeignKey(systematique, on_delete=models.CASCADE)
    radio = models.ForeignKey(Radio, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='analyses/')


class Notes(models.Model):
    STATUS = (
        ("new", "NEWEST"),
        ("old", "OLDEST"),
        ("title", "TITLE"),
    )
    heading = models.CharField(max_length=200)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS, default="old")

    def __str__(self):
        return self.heading


# Create your models here.


class User(AbstractUser):
    is_medecin = models.BooleanField('Is medecin', default=False)
    is_infirmier = models.BooleanField('Is infirmier', default=False)
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)




class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'user'
