import forms
from .models import Order

class InterestForm(forms.Form):
    CHOICES = [('Yes', 1), ('No', 0)]
    interested = forms.CharField(widget=forms.RadioSelect(choices=CHOICES))
    levels = forms.IntegerField(initial = 1)
    comments = forms.CharField(label='Additional Comments', required=False, widget=forms.Textarea)
    
# Order Form
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order;
        fields = ['Student', 'course', 'levels', 'order_date']
        widgets = {
            'student': forms.RadioSelect
        }
        widgets = {
            'order_date': forms.SelectDateWidget
        }
