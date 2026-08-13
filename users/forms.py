from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from users.models import CustomUser
import re


class StyleMixin:
    
    # 1. Standard Inputs (Text, Email, URL, Password, Number, Date, Time)
    text_input_design = "w-full mt-2 mx-2 my-2 border-2 border-gray-100 rounded-lg focus:border-red-600 focus:ring-0"
    
    # 2. Textarea (Allows vertical resizing)
    textarea_design = "w-full mt-2 mx-2 my-2 border-2 border-gray-100 rounded-lg focus:border-red-600 focus:ring-0 resize-y"
    
    # 3. Dropdowns/Selects (Single and Multiple)
    select_design = "w-full mt-2 mx-2 my-2 border-2 border-gray-100 rounded-lg focus:border-red-600 focus:ring-0 bg-white"
    
    # 4. Booleans and Choices (Checkboxes, Radios, Multiple Checkboxes)
    # Prevents them from stretching across the screen; adds red accent color
    check_radio_design = "mt-2 mx-2 border-gray-300 text-red-600 focus:ring-red-600 rounded cursor-pointer inline-block"
    
    # 5. File Uploads (FileInput, ClearableFileInput)
    # Uses Tailwind's `file:` modifier to style the actual "Choose File" button
    file_design = "w-full mt-2 mx-2 my-2 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()

    def apply_styles(self):
        for field_name, field in self.fields.items():
            widget = field.widget
            
            # --- 1. Apply Specific Widget Classes ---
            if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect, forms.CheckboxSelectMultiple)):
                base_class = self.check_radio_design
            elif isinstance(widget, (forms.FileInput, forms.ClearableFileInput)):
                base_class = self.file_design
            elif isinstance(widget, forms.Textarea):
                base_class = self.textarea_design
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                base_class = self.select_design
            else:
                # Catch-all for TextInput, EmailInput, DateInput, NumberInput, PasswordInput, etc.
                base_class = self.text_input_design

            # Safely merge existing classes (like ones defined on the form itself) with the new ones
            existing_classes = widget.attrs.get('class', '')
            widget.attrs['class'] = f"{existing_classes} {base_class}".strip()

            # --- 2. Smart Placeholders ---
            # Exclude widgets where placeholders are invalid HTML or don't make sense
            no_placeholder_widgets = (
                forms.CheckboxInput, forms.RadioSelect, forms.CheckboxSelectMultiple,
                forms.FileInput, forms.ClearableFileInput,
                forms.Select, forms.SelectMultiple,
                forms.HiddenInput
            )
            
            if not isinstance(widget, no_placeholder_widgets):
                # Only set it if you haven't manually set one on the form field already
                if 'placeholder' not in widget.attrs:
                    label_text = field.label or field_name.replace('_', ' ').title()
                    widget.attrs['placeholder'] = f"Enter {label_text.lower()}"



class RegisterModelForm(StyleMixin,UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=CustomUser
        fields=['username','first_name','last_name','email','role','phone','password1','password2']

    def clean_email(self):
        email=self.cleaned_data.get('email')
        email_exist=CustomUser.objects.filter(email=email).exists()

        if email_exist:
            raise forms.ValidationError('Email Alreay Exist')
        return email

    def clean_password1(self):
        password=self.cleaned_data.get('password1')
        errors=[]
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        if not re.search(r'[A-Z]', password):
            errors.append('Password must include at least one uppercase letter.')
        if not re.search(r'[a-z]', password):
            errors.append('Password must include at least one lowercase letter.')
        if not re.search(r'[0-9]', password):
            errors.append('Password must include at least one number.')
        if not re.search(r'[@#$%^&+=]', password):
            errors.append('Password must include at least one special character.')

        if errors:
            raise forms.ValidationError(errors)
        return password

    def clean_first_name(self):
        first_name=self.cleaned_data.get('first_name')

        if first_name and not re.match(r'^[A-Za-z]+$', first_name):
            raise forms.ValidationError(
            'First name can contain letters only.'
            )
        return first_name

    def clean_last_name(self):
        last_name=self.cleaned_data.get('last_name')

        if last_name and not re.match(r'^[A-Za-z]+$', last_name):
                    raise forms.ValidationError(
                    'First name can contain letters only.'
                    )
        return last_name

    
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password1')
        confirm_password=cleaned_data.get('password2')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password Did not same. Both Password Must be Same')
        return cleaned_data



class login_form(StyleMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "w-full px-4 py-3 rounded-lg border border-slate-300 bg-slate-50 text-slate-900 placeholder-slate-400 focus:bg-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200",
            "placeholder": "Enter your username",
        })

        self.fields["password"].widget.attrs.update({
            "class": "w-full px-4 py-3 rounded-lg border border-slate-300 bg-slate-50 text-slate-900 placeholder-slate-400 focus:bg-white focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200",
            "placeholder": "Enter your password",})
