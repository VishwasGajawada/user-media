from django import forms
from userapp.models import UserProfile,Post,Comment
from django.contrib.auth.forms import UserCreationForm as UCF
from django.contrib.auth.models import User

class UserCreationForm(UCF):
    class Meta:
        fields =('username','email','password1','password2')
        model = User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic',]
        help_texts = {
            'profile_pic' : '(optional)'
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

class PostForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea,required=False)
    class Meta:
        model = Post
        fields = ('title','picture','description')
class PostUpdateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea,required=False)
    class Meta:
        model = Post
        fields = ['description',]
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Enter your comment'}),
        }
        labels = {
            'text':'Comment',
        }