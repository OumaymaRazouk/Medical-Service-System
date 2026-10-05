
from django import forms
from .models import Medicine, info, Radio
from .models import Patient
from django.contrib.auth import get_user_model

from django.forms import DateInput, SelectDateWidget, ModelForm

from django.contrib.auth.forms import UserCreationForm
from .models import User, Analyse, surveillance, Laboratoire, VisiteReprise, Notes



User=get_user_model()
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]


class PositionForm(forms.Form):
    position = forms.CharField()


class InfoForm(forms.ModelForm):
    class Meta:
        model = info
        fields = '__all__'
        widgets = {
            'numero': forms.Select(attrs={'class': 'form-select mr-sm-2'}),
        }


from django import forms
from .models import systematique


class SystematiqueForm(forms.ModelForm):
    analyses = forms.ModelMultipleChoiceField(
        queryset=Analyse.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = systematique
        fields = '__all__'


#########PatientForm
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'start_date', 'origin', 'company', 'address', 'job_position',
                  'family_status', 'department', 'photo', 'area', 'risk']
        widgets = {
            'area': forms.Select(attrs={'class': 'form-select mr-sm-2'}),
            'company': forms.Select(attrs={'class': 'form-select mr-sm-2'}),
        }


###Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['N_lot', 'name', 'quantity', 'expiration_date', 'presentation', 'dosage']


# ambulance

from django import forms
from .models import AmbulanceItem, AmbulanceMedicine


class AmbulanceItemForm(forms.ModelForm):
    class Meta:
        model = AmbulanceItem
        fields = ['name', 'quantity', 'purchase_date']


class AmbulanceMedicineForm(forms.ModelForm):
    class Meta:
        model = AmbulanceMedicine
        fields = ['N_lot', 'name', 'quantity', 'expiration_date', 'presentation', 'dosage']


################visite###########################
from django import forms
from .models import VisiteMedicaleSpontanee


class VisiteMedicaleSpontaneeForm(forms.ModelForm):
    class Meta:
        model = VisiteMedicaleSpontanee
        fields = ['patient', 'visit_date', 'temperature', 'blood_pressure', 'oxygen_saturation', 'heart_rate',
                  'blood_glucose', 'symptoms', 'observations']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select mr-sm-2'}),
        }


#############OUT#########################
from django import forms
from .models import OutStockMedicine


class OutStockMedicineForm(forms.ModelForm):
    class Meta:
        model = OutStockMedicine
        fields = ['patient', 'medicine', 'date', 'quantity', 'remark']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select mr-sm-2'}),
            'medicine': forms.Select(attrs={'class': 'form-select mr-sm-2'})
        }
        ###################CheckInHistory#########################


from django import forms
from .models import CheckInHistory


class CheckInHistoryForm(forms.ModelForm):
    remark = forms.CharField(max_length=200, required=False)

    class Meta:
        model = CheckInHistory
        fields = ['file_pdf', 'other_file']


class VisiteRepriseForm(forms.ModelForm):
    class Meta:
        model = VisiteReprise
        fields = ['date', 'choix', 'texte_certificat']
        widgets = {
            'choix': forms.RadioSelect(choices=VisiteReprise.CHOICES),

            'texte_certificat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SurveillanceForm(forms.ModelForm):
    class Meta:
        model = surveillance
        fields = ['date', 'taille', 'poids', 'T_A', 'A_V', 'pouls', 'Glycemie', 'Albumin', 'Glucose',
                  'Medecin_de_travail']

        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 600px'}),
            # Utiliser un sélecteur de date
            'taille': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'style': 'width: 600px'}),
            # Utiliser un champ numérique avec 4 décimales
            'poids': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'style': 'width: 600px'}),
            # Utiliser un champ numérique avec 4 décimales
            'T_A': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'style': 'width: 600px'}),
            # Utiliser un champ numérique avec 4 décimales
            'A_V': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'style': 'width: 600px'}),
            # Utiliser un champ numérique avec 4 décimales
            'pouls': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'style': 'width: 600px'}),
            # Utiliser un champ numérique avec 4 décimales
            'Glycemie': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'style': 'width: 600px'}),
            # Utiliser un champ numérique avec 4 décimales
            'Albumin': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'style': 'width: 600px'}),
            # Utiliser un champ numérique avec 4 décimales
            'Glucose': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'style': 'width: 600px'}),
            # Utiliser un champ numérique avec 4 décimales
            'Medecin_de_travail': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nom du médecin de travail', 'style': 'width: 600px'}),
            # Utiliser un champ de texte avec un placeholder
        }


class NotesForm(ModelForm):
    heading = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Enter Title"
    }))
    text = forms.CharField(max_length=500, widget=forms.Textarea(attrs={
        "class": "form-control", "placeholder": "Enter Notes", "rows": "8"
    }))

    class Meta:
        model = Notes
        fields = ['heading', 'text']


class LaboratoireForm(forms.ModelForm):
    class Meta:
        model = Laboratoire
        fields = ['fichier']


class InfoForm(forms.ModelForm):
    class Meta:
        model = info
        fields = ['groupe_singuins', 'situation_militaire', 'maladies', 'intervention_chirurgicales', 'accidents',
                  'accidents_travail', 'maladies_prof', 'compagnes',
                  'blessures', 'IPP', 'ant_pere', 'ant_mere', 'ant_freres', 'ant_soeurs', 'ant_conjoint', 'ant_enfant',
                  'ant_professionneles', 'variole', 'diphterie', 'tetanos',
                  'tab', 'tabdt', 'autres', 'serum']
        labels = {
            'groupe_singuins': 'Groupe Sanguin',
            'situation_militaire': 'Situation Militaire',
            'maladies': 'Maladies',
            'intervention_chirurgicales': 'Interventions Chirurgicales',
            'accidents': 'Accidents',
            'accidents_travail': 'Accidents de Travail',
            'maladies_prof': 'Maladies Professionnelles',
            'compagnes': 'Compagnes',
            'blessures': 'Blessures',
            'IPP': 'IPP',
            'ant_pere': 'Antécédents Père',
            'ant_mere': 'Antécédents Mère',
            'ant_freres': 'Antécédents Frères',
            'ant_soeurs': 'Antécédents Sœurs',
            'ant_conjoint': 'Antécédents Conjoint',
            'ant_enfant': 'Antécédents Enfant',
            'ant_professionneles': 'Antécédents Professionnels',
            'variole': 'Variole',
            'diphterie': 'Diphtérie',
            'tetanos': 'Tétanos',
            'tab': 'Tab',
            'tabdt': 'Tab DT',
            'autres': 'Autres',
            'serum': 'Sérum', }
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your numero here',
            }),
            'groupe_singuins': forms.Select(attrs={
                'class': 'form-control',
            }),
            'situation_militaire': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'maladies': forms.TextInput(attrs={
                'class': 'form-control',
                
            }),
            'intervention_chirurgicales': forms.TextInput(attrs={
                'class': 'form-control',
            
            }),
            'accidents': forms.TextInput(attrs={
                'class': 'form-control',
                
            }),
            'accidents_travail': forms.TextInput(attrs={
                'class': 'form-control',
               
            }),
            'maladies_prof': forms.TextInput(attrs={
                'class': 'form-control',
               
            }),
            'compagnes': forms.TextInput(attrs={
                'class': 'form-control',
                
            }),
            'blessures': forms.TextInput(attrs={
                'class': 'form-control',
                
            }),
            'IPP': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'ant_pere': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'ant_mere': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'ant_freres': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'ant_soeurs': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'ant_conjoint': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'ant_enfant': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'ant_professionneles': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'variole': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'diphterie': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'tetanos': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'tab': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'tabdt': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'autres': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'serum': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class SystematiqueForm(forms.ModelForm):
    analyses = forms.ModelMultipleChoiceField(
        queryset=Analyse.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    radios = forms.ModelMultipleChoiceField(
        queryset=Radio.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = systematique
        fields = ['date', 'denture', 'audition_od', 'audition_og', 'vision_od', 'vision_og', 'taille',
                  'poids', 'per_thor', 'cap_resp', 'peau_phaneres',
                  'locomateur', 'dynamometre', 'respiratoire', 'radioscopique', 'vaisseaux', 'varices', 'coeur',
                  'gangalions', 'pouls', 'TA', 'abdomen',
                  'foie', 'bouche', 'rate', 'cicatrice', 'blenno', 'regles', 'neuro_psychisme', 'nervosisme',
                  'tremblement', 'equilibre', 'romberg',
                  'reflxes_oc', 'reflexes_trend', 'cutt', 'sedimenation', 'crachat', 'selle', 'urines', 'sang',
                  'situation', 'surveiller', 'analyses', 'radios', 'commentaire']

        widgets = {
            'radio': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'denture': forms.TextInput(attrs={'class': 'form-control'}),
            'audition_od': forms.TextInput(attrs={'class': 'form-control'}),
            'audition_og': forms.TextInput(attrs={'class': 'form-control'}),
            'vision_od': forms.TextInput(attrs={'class': 'form-control'}),
            'vision_og': forms.TextInput(attrs={'class': 'form-control'}),
            'taille': forms.TextInput(attrs={'class': 'form-control'}),
            'poids': forms.TextInput(attrs={'class': 'form-control'}),
            'per_thor': forms.TextInput(attrs={'class': 'form-control'}),
            'cap_resp': forms.TextInput(attrs={'class': 'form-control'}),
            'peau_phaneres': forms.TextInput(attrs={'class': 'form-control'}),
            'locomateur': forms.TextInput(attrs={'class': 'form-control'}),
            'dynamometre': forms.TextInput(attrs={'class': 'form-control'}),
            'respiratoire': forms.TextInput(attrs={'class': 'form-control'}),
            'radioscopique': forms.TextInput(attrs={'class': 'form-control'}),
            'vaisseaux': forms.TextInput(attrs={'class': 'form-control'}),
            'varices': forms.TextInput(attrs={'class': 'form-control'}),
            'coeur': forms.TextInput(attrs={'class': 'form-control'}),
            'gangalions': forms.TextInput(attrs={'class': 'form-control'}),
            'pouls': forms.TextInput(attrs={'class': 'form-control'}),
            'TA': forms.TextInput(attrs={'class': 'form-control'}),
            'abdomen': forms.TextInput(attrs={'class': 'form-control'}),
            'foie': forms.TextInput(attrs={'class': 'form-control'}),
            'bouche': forms.TextInput(attrs={'class': 'form-control'}),
            'rate': forms.TextInput(attrs={'class': 'form-control'}),
            'cicatrice': forms.TextInput(attrs={'class': 'form-control'}),
            'blenno': forms.TextInput(attrs={'class': 'form-control'}),
            'regles': forms.TextInput(attrs={'class': 'form-control'}),
            'neuro_psychisme': forms.TextInput(attrs={'class': 'form-control'}),
            'nervosisme': forms.TextInput(attrs={'class': 'form-control'}),
            'tremblement': forms.TextInput(attrs={'class': 'form-control'}),
            'equilibre': forms.TextInput(attrs={'class': 'form-control'}),
            'romberg': forms.TextInput(attrs={'class': 'form-control'}),
            'reflxes_oc': forms.TextInput(attrs={'class': 'form-control'}),
            'reflexes_trend': forms.TextInput(attrs={'class': 'form-control'}),
            'cutt': forms.TextInput(attrs={'class': 'form-control'}),
            'sedimenation': forms.TextInput(attrs={'class': 'form-control'}),
            'crachat': forms.TextInput(attrs={'class': 'form-control'}),
            'selle': forms.TextInput(attrs={'class': 'form-control'}),
            'urines': forms.TextInput(attrs={'class': 'form-control'}),
            'analyses': forms.Select(attrs={'class': 'form-control'}),
            'sang': forms.Select(attrs={'class': 'form-control'}),
            'situation': forms.Select(attrs={'class': 'form-control'}),
            'surveiller': forms.Select(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class VisiteRepriseForm(forms.ModelForm):
    class Meta:
        model = VisiteReprise
        fields = ['date', 'choix', 'texte_certificat']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 600px'}),

            'choix': forms.RadioSelect(choices=VisiteReprise.CHOICES),

            'texte_certificat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AnalyseForm(forms.ModelForm):
    class Meta:
        model = Analyse
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
        }


class RadioForm(forms.ModelForm):
    class Meta:
        model = Radio
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
        }