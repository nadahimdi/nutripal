from django.shortcuts import render
from django.contrib.auth import login, logout
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .token import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from orders.models import Order
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode




from .forms import RegistrationForm,UserEditForm
from .models import UserBase
from .token import account_activation_token

# Create your views here.

@login_required
def dashboard(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request,
                  'account/user/dashboard.html', {"orders": orders}
                 )







@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/user/edit_details.html', {'user_form': user_form})

@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')

def account_register(request):
       # if request.user.is_authentificated:
         # return redirect('/')
        if request.method == 'POST':
             registerForm = RegistrationForm(request.POST)
             if registerForm.is_valid():
                    user = registerForm.save(commit=False)
                    user.email = registerForm.cleaned_data['email']
                    user.set_password(registerForm.cleaned_data['password'])
                    user.is_active = False #THIS IS A SECURITY CHECK
                    user.save()
                    # setup email
                    current_site = get_current_site(request) # get current site infos such as the domain
                    subject = 'Activate your Account'
                    message = render_to_string('account/registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    # urlsafe_base64_encode prepare the data to be utilized
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)), #encoding the user's primary key in a way that can be safely used in URLs.
                    'token': account_activation_token.make_token(user),
            })
                    user.email_user(subject=subject, message=message)
                    return  render(request,'account/registration/register_email_confirm.html')
        else :
              registerForm =RegistrationForm()
        return render(request,'account/registration/register.html',{'form': registerForm})
        

def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except():
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
    


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/user/user_orders.html", {"orders": orders})
    




