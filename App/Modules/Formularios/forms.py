from django.forms import TextInput, EmailInput, PasswordInput, ModelForm
from App.models import Avance,ListaVerificacion, Proyecto, Tribunal, Tutoria
from Usuarios.models import Facultad, Carrera, SeguimientoDocumentacion, Usuarios, Documento
from django import forms


class formularioFacultades(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Facultad
        fields = '__all__'


class formularioCarreras(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Carrera
        fields = '__all__'


class formularioListaVerificaciones(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    # i.field.widget.attrs['class'] = 'form-check-input'
                    pass
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = ListaVerificacion
        fields = ('nombre','observacion', 'idProyecto', 'archivo') 
class formActualizarfirma(ModelForm):
    class Meta:
        model = SeguimientoDocumentacion
        fields = ('archivo','estado') 
class formularioArchivoListaVerificacion(ModelForm):
    class Meta:
        model = ListaVerificacion
        fields = ('archivo',)


class formularioProyectos(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5
        self.fields['idCarrera'].widget.attrs['autofocus'] = True

    class Meta:
        model = Proyecto
        fields = '__all__'


class formularioEstudiantes(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5
        self.fields['username'].widget.attrs['autofocus'] = True

    class Meta:
        model = Usuarios
        fields = '__all__'


class formularioTutorias(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 30
                i.field.widget.attrs['rows'] = 10
        self.fields['idProyecto'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tutoria
        fields = '__all__'


class formularioGrupoExperto(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = None
        fields = '__all__'

class formularioTribunal(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5
        self.fields['idProyecto'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tribunal
        fields = '__all__'

class formularioAvances(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5
        self.fields['idProyecto'].widget.attrs['autofocus'] = True

    class Meta:
        model = Avance
        fields = ('idProyecto', 'nombreAvance', 'fechaEntrega')

class formularioAvancesEstudiante(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5

    class Meta:
        model = Avance
        fields = ('archivo',)

class formularioDocumentos(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Documento
        fields = '__all__'
class formularioFirma(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5

    class Meta:
        model = Usuarios
        fields = ('firma',)


class formularioUsuarios(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['idNivel'].widget.attrs['required'] = True
        self.fields['modalidad'].widget.attrs['required'] = True

    class Meta:
        modalidades = [
            ('Trabajo de Integración Curricular','Trabajo de Integración Curricular'),
            ('Examen con Carácter Complexivo','Examen con Carácter Complexivo')
        ]
        model = Usuarios
        widgets = {
            'password': forms.PasswordInput(),
            'username': forms.TextInput(attrs={'placeholder':'cédula'}),
    	    'email' : forms.EmailInput(attrs={'required': True}),
    	    'imagen' : forms.FileInput(attrs={'required': True}),
            'perfil' : forms.ChoiceField(widget=forms.RadioSelect, choices=modalidades)  
        }
        labels = {
            'first_name' : 'Nombres',
            'username' : 'Cédula'
        }
        fields = ('username', 'first_name', 'last_name', 'idCarrera', 'celular', 'email', 'password', 'imagen','modalidad','idNivel','genero', 'cohorte', 'esExtranjero')
class formularioDocentes(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5
        self.fields['perfil'].initial = 2
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['perfil'].widget.attrs['hidden'] = True

    class Meta:
        model = Usuarios
        widgets = {
            'password': forms.PasswordInput(),
            'username': forms.TextInput(attrs={'placeholder':'cédula'}),
            'perfil': forms.TextInput(),
    	    'email' : forms.EmailInput(attrs={'required': True}),
    	    'imagen' : forms.FileInput(attrs={'required': True})
        }
        labels = {
            'perfil' : '',
            'first_name' : 'Nombres',
            'username' : 'Cédula'
        }

        fields = ('username', 'first_name', 'last_name', 'idCarrera', 'celular', 'email', 'password', 'imagen', 'perfil')


class formularioPerfilUsuario(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            try:
                if i.field.widget.input_type == 'checkbox':
                    i.field.widget.attrs['class'] = 'form-check-input'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                elif i.field.widget.input_type == 'select':
                    i.field.widget.attrs['class'] = 'form-control form-control-sm select2'
                else:
                    i.field.widget.attrs['class'] = 'form-control form-control-sm'
                    i.field.widget.attrs['autocomplete'] = 'off'
            except Exception as e:
                i.field.widget.attrs['cols'] = 20
                i.field.widget.attrs['rows'] = 5
        self.fields['celular'].widget.attrs['autofocus'] = True

    class Meta:
        model = Usuarios
        fields = ('celular', 'email', 'imagen')


class resetPasswordForm(forms.Form):
    username = forms.CharField(
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el usuario a resetear',
            'autocomplete': 'off'
        }), label='Usuario'
    )
    email = forms.EmailField(
        widget=EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el email de este usuario',
            'autocomplete': 'off'
        }), label='Email'
    )


class resetPasswordFormLink(forms.Form):
    password1 = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nueva contraseña',
            'autocomplete': 'off'
        }), label='Nueva Contraseña'
    )
    password2 = forms.EmailField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repita Contraseña',
            'autocomplete': 'off'
        }), label='Confirmar Contraseña'
    )
