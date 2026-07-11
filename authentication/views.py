from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model


from django.views.generic import TemplateView

User = get_user_model()

# ------------------------------------------------------
# REGISTER USER
# ------------------------------------------------------
@api_view(["POST"])
def register_user(request):
    name = request.data.get("name")
    email = request.data.get("email")
    role = request.data.get("role")
    password1 = request.data.get("password1")
    password2 = request.data.get("password2")

    # Check all fields
    if not all([name, email, role, password1, password2]):
        return Response({"error": "All fields are required"}, status=400)

    # Password mismatch
    if password1 != password2:
        return Response({"error": "Passwords do not match"}, status=400)

    # Email exists
    if User.objects.filter(email=email).exists():
        return Response({"email": ["Email already exists"]}, status=400)

    # Create user
    user = User.objects.create_user(
        name=name,
        email=email,
        password=password1,
        role=role
    )

    # Generate tokens
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "message": "User registered successfully",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role,
        },
        status=status.HTTP_201_CREATED,
    )


# ------------------------------------------------------
# LOGIN USER
# ------------------------------------------------------
@api_view(["POST"])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password required"}, status=400)

    # Find user
    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid login credentials"}, status=400)

    # Authenticate using email
    user = authenticate(username=user_obj.email, password=password)

    if not user:
        return Response({"error": "Invalid login credentials"}, status=400)

    # Generate tokens
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role,
        }
    )




class ForgotPasswordView(TemplateView):
    template_name = "auth/forgot_password.html"