from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    RegisterSerializer, LoginSerializer,
    PatientSerializer, DoctorSerializer,
    MappingSerializer, MappingReadSerializer,
)

User = get_user_model()


# ── Auth Views ────────────────────────────────────────────────────────────────

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'message': 'User registered successfully.', 'user': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)


# ── Patient ViewSet ───────────────────────────────────────────────────────────

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users only see their own patients
        return Patient.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        # Ensure ownership on detail actions
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj


# ── Doctor ViewSet ────────────────────────────────────────────────────────────

class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # LIST returns all doctors; write actions restricted to owner
        return Doctor.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        obj = get_object_or_404(Doctor, pk=self.kwargs['pk'])
        # For mutating actions, verify ownership
        if self.request.method not in ('GET', 'HEAD', 'OPTIONS'):
            if obj.user != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You do not have permission to modify this doctor.")
        return obj


# ── Patient-Doctor Mapping Views ──────────────────────────────────────────────

class MappingListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MappingReadSerializer
        return MappingSerializer

    def get_queryset(self):
        # Only mappings for the authenticated user's patients
        return PatientDoctorMapping.objects.filter(
            patient__user=self.request.user
        ).select_related('patient', 'doctor').order_by('-created_at')

    def perform_create(self, serializer):
        patient = serializer.validated_data['patient']
        # Ensure the patient belongs to the requesting user
        if patient.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only create mappings for your own patients.")
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                MappingReadSerializer(serializer.instance).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MappingByPatientView(generics.ListAPIView):
    serializer_class = MappingReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        # Verify the patient exists and belongs to the user
        patient = get_object_or_404(Patient, pk=patient_id, user=self.request.user)
        return PatientDoctorMapping.objects.filter(
            patient=patient
        ).select_related('patient', 'doctor').order_by('-created_at')


class MappingDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        mapping = get_object_or_404(
            PatientDoctorMapping,
            pk=self.kwargs['pk'],
            patient__user=self.request.user
        )
        return mapping

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response({'message': 'Mapping deleted successfully.'}, status=status.HTTP_200_OK)
