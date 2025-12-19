from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.views import LogoutView
from django.contrib import messages

User = get_user_model()


# a function for merging login and registration (validating both username and email for login)
def auth_view(request):
    if request.user.is_authenticated:
        return redirect("todo:task_list")
    login_form = CustomLoginForm()
    register_form = CustomUserCreationForm()

    if request.method == "POST":
        if "login_submit" in request.POST:
            login_form = CustomLoginForm(request.POST)
            if login_form.is_valid():
                identifier = login_form.cleaned_data["identifier"]
                password = login_form.cleaned_data["password"]

                user = None
                if "@" in identifier:
                    try:
                        user_obj = User.objects.get(email=identifier)
                        user = authenticate(
                            request, username=user_obj.email, password=password
                        )

                    except User.DoesNotExist:
                        user = None

                else:
                    try:
                        user_obj = User.objects.get(username=identifier)
                        user = authenticate(
                            request, username=user_obj.email, password=password
                        )
                    except User.DoesNotExist:
                        user = None

                if user is not None:
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.username}!")
                    return redirect("todo:task_list")
                else:
                    login_form.add_error(None, "Invalid credentials")

        elif "register_submit" in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(
                    request,
                    f"{user.username} Your account created successfully! Welcome",
                )
                return redirect("todo:task_list")
            else:
                for field, errors in register_form.errors.items():
                    for error in errors:
                        messages.error(request, error)

    return render(
        request,
        "accounts/auth.html",
        {
            "login_form": login_form,
            "register_form": register_form,
        },
    )


# a custom logout view (redirecting to index page)
class CustomLogoutView(LogoutView):
    next_page = "/"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
