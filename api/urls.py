from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, LoginView,
    PatientViewSet, DoctorViewSet,
    MappingListCreateView, MappingByPatientView, MappingDeleteView,
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),

    # Patients & Doctors via router
    path('', include(router.urls)),

    # Mappings
    path('mappings/', MappingListCreateView.as_view(), name='mapping-list-create'),
    path('mappings/<int:patient_id>/', MappingByPatientView.as_view(), name='mapping-by-patient'),
    path('mappings/<int:pk>/delete/', MappingDeleteView.as_view(), name='mapping-delete'),
]
