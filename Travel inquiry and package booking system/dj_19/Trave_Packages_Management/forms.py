from django import forms

class SendQuotationForm(forms.Form):
    amount = forms.DecimalField(
        label="Quotation Amount",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',   
            'placeholder': 'Enter amount'
        })
    )
    details = forms.CharField(label="Details", widget=forms.Textarea, required=False)
