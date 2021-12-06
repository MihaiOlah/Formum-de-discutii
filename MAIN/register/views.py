from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm      # Permite crearea usoara a unui forum de inregistrare
from django.contrib.auth.forms import AuthenticationForm    # Permite crearea usoara a unui forum de autentificare
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from register.forms import UpdateForm
from django.contrib.auth import logout as lt


def signup(request):
    context = {}
    form = UserCreationForm(request.POST or None)

    # Daca cererea este valida, atunci vom salva cererea de inregistrare
    if request.method == "POST":
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)                  # Dupa ce am salvat datele, logam utilizatorul instantaneu
            return redirect("update_profile")         # Redirectionam utilizatorul la pagina unde poate sa faca cerere pentru drepturi de autor

    context.update({
        "form": form,
        "title": "Signup" 
    })

    return render(request, "register/signup.html", context)

def signin(request):
    context = {}

    form = AuthenticationForm(request, data=request.POST)

    if request.method == "POST":
        if form.is_valid():
            # Extragem numele si utilizatorul din formular
            user = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # Verificam daca parola si numele de utilizator sunt valide
            user = authenticate(username=user, password=password)       

            # Daca credentialele se potrivesc, atunci redirectionam utilizatorul la pagina principala
            if user is not None:
                login(request, user)
                return redirect("home")

    context.update({
        "form": form,
        "title": "Signin"
    })
    return render(request, "register/signin.html", context)


@login_required
def update_profile(request):
    context = {}
    user = request.user
    form = UpdateForm(request.POST, request.FILES)

    if request.method == "POST":
        if form.is_valid():
            update_profile = form.save(commit=False)        # Nu vrem sa facem inca commit in baza de date
            update_profile.user = user
            update_profile.save()

            return redirect("home")

    context.update({
        "form": form,
        "title": "Update Profile"
    })

    return render(request, "register/update.html", context)

@login_required
def logout(request):
    # Facem cerere de logout
    lt(request) 

    # Redirectionam utilizatorul
    return redirect("home")
