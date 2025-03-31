from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import models
from .models import (
    Client, Atelier, FabricStore, Commandes, DemandeAtelier,
    CommandeAtelierFabricStore, DemandeFabricStore, Product, AdvertisementsAtelier,

)
from .serializers import (
    ClientSerializer, AtelierSerializer, FabricStoreSerializer, CommandeSerializer,
    DemandeAtelierSerializer, CommandeAtelierFabricStoreSerializer, DemandeFabricStoreSerializer,
    ProductSerializer, AdvertisementsAtelierSerializer, 
)
from .pagination import CustomPagination 
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import check_password
from rest_framework.parsers import JSONParser
import logging
from .utils import create_response

from rest_framework.authentication import TokenAuthentication

# ============ Creation APIs ============

class CommandeCreateView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        serializer = CommandeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(
                data=serializer.data,
                message="Command created successfully",
                status_code=status.HTTP_201_CREATED
            )
        
        # Enhanced error messages
        error_message = "Failed to create command due to validation errors"
        if 'client' in serializer.errors:
            error_message = "Invalid or missing client information"
        elif 'atelier' in serializer.errors:
            error_message = "Invalid or missing workshop information"
        elif 'date_livraison' in serializer.errors:
            error_message = "Invalid delivery date format or missing delivery date"
        
        return create_response(
            message=error_message,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class DemandeAtelierCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        serializer = DemandeAtelierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(
                data=serializer.data,
                message="Workshop request created successfully",
                status_code=status.HTTP_201_CREATED
            )
        return create_response(
            message="Failed to create workshop request",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class CommandeAtelierFabricStoreCreateView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        serializer = CommandeAtelierFabricStoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(
                data=serializer.data,
                message="Workshop-fabric store command created successfully",
                status_code=status.HTTP_201_CREATED
            )
        
        # Enhanced error messages
        error_message = "Failed to create workshop-fabric store command"
        if 'atelier' in serializer.errors:
            error_message = "Invalid or missing workshop information"
        elif 'fabric_store' in serializer.errors:
            error_message = "Invalid or missing fabric store information"

        elif 'date_livraison' in serializer.errors:
            error_message = "Invalid delivery date format or missing delivery date"
        
        return create_response(
            message=error_message,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class DemandeFabricStoreCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        serializer = DemandeFabricStoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(
                data=serializer.data,
                message="Fabric store request created successfully",
                status_code=status.HTTP_201_CREATED
            )
        return create_response(
            message="Failed to create fabric store request",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class AdvertisementsAtelierCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        serializer = AdvertisementsAtelierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(
                data=serializer.data,
                message="Workshop advertisement created successfully",
                status_code=status.HTTP_201_CREATED
            )
        return create_response(
            message="Failed to create workshop advertisement",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

# =============== View List APIs ===============
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = CustomPagination
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    authentication_classes = [TokenAuthentication]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return create_response(
                data=serializer.data,
                message="Client created successfully",
                status_code=status.HTTP_201_CREATED
            )
        return create_response(
            message="Failed to create client",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return create_response(
                data=serializer.data,
                message="Client updated successfully",
                status_code=status.HTTP_200_OK
            )
        return create_response(
            message="Failed to update client",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return create_response(
                data=self.get_paginated_response(serializer.data).data,
                message="Clients retrieved successfully",
                status_code=status.HTTP_200_OK
            )
        serializer = self.get_serializer(queryset, many=True)
        return create_response(
            data=serializer.data,
            message="Clients retrieved successfully",
            status_code=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return create_response(
            data=serializer.data,
            message="Client retrieved successfully",
            status_code=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return create_response(
            message="Client deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )
    
class AtelierViewSet(viewsets.ModelViewSet):
    queryset = Atelier.objects.all()
    serializer_class = AtelierSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by atelier_id if provided in query parameters
        atelier_id = self.request.query_params.get('atelier_id', None)
        if atelier_id:
            queryset = queryset.filter(user_id=atelier_id).only('user_id', 'store_name', 'phone', 'address',)

        # Filter by name if provided
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(store_name__icontains=name)
            
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return create_response(
                data=serializer.data,
                message="Workshop created successfully",
                status_code=status.HTTP_201_CREATED
            )
        return create_response(
            message="Failed to create workshop",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return create_response(
                data=self.get_paginated_response(serializer.data).data,
                message="Workshops retrieved successfully",
                status_code=status.HTTP_200_OK
            )
        serializer = self.get_serializer(queryset, many=True)
        return create_response(
            data=serializer.data,
            message="Workshops retrieved successfully",
            status_code=status.HTTP_200_OK
        )

class FabricStoreViewSet(viewsets.ModelViewSet):
    queryset = FabricStore.objects.all().order_by('user_id')
    serializer_class = FabricStoreSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return create_response(
                data=serializer.data,
                message="Fabric store created successfully",
                status_code=status.HTTP_201_CREATED
            )
        return create_response(
            message="Failed to create fabric store",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

@csrf_exempt
def delete_client(request, client_id):
    if request.method == "DELETE":
        try:
            client = Client.objects.get(user_id=client_id)
            client_name = client.name
            client.delete()
            return JsonResponse({
                'status': 'success',
                'message': f'Client {client_name} deleted successfully',
                'data': {'client_id': client_id}
            }, status=200)
        except Client.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'Client with ID {client_id} not found',
                'errors': {'client_id': 'CLIENT_NOT_FOUND'}
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'Internal server error occurred',
                'errors': {'server': str(e)}
            }, status=500)
    return JsonResponse({
        'status': 'error',
        'message': f'Method {request.method} not allowed. Use DELETE instead.',
        'errors': {'method': 'METHOD_NOT_ALLOWED'}
    }, status=405)

@csrf_exempt
def delete_atelier(request, atelier_id):
    if request.method == "DELETE":
        try:
            atelier = Atelier.objects.get(user_id=atelier_id)
            store_name = atelier.store_name
            atelier.delete()
            return JsonResponse({
                'status': 'success',
                'message': f'Atelier {store_name} deleted successfully',
                'data': {'atelier_name': store_name}
            }, status=200)
        except Atelier.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'Atelier with ID {atelier_id} not found',
                'errors': {'atelier_id': 'ATELIER_NOT_FOUND'}
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'Internal server error occurred',
                'errors': {'server': str(e)}
            }, status=500)
    return JsonResponse({
        'status': 'error',
        'message': f'Method {request.method} not allowed. Use DELETE instead.',
        'errors': {'method': 'METHOD_NOT_ALLOWED'}
    }, status=405)

def update_atelier(request, atelier_name):
    if request.method == "PUT":
        try:
            atelier = Atelier.objects.get(store_name=atelier_name)
            atelier.store_name = request.data.get('store_name', atelier.store_name)
            atelier.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Atelier updated successfully',
                'data': {'store_name': atelier.store_name}
            }, status=200)
        except Atelier.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Atelier not found',
                'errors': {'atelier_name': 'ATELIER_NOT_FOUND'}
            }, status=404)
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method',
        'errors': {'method': 'METHOD_NOT_ALLOWED'}
    }, status=400)

@csrf_exempt
def delete_fabric_store(request, fabric_store_id):
    if request.method == "DELETE":
        try:
            fabric_store = FabricStore.objects.get(user_id=fabric_store_id)
            store_name = fabric_store.store_name  # Store fabric store name before deletion
            fabric_store.delete()
            return JsonResponse({
                'status': 'success',
                'message': f'Fabric Store {store_name} deleted successfully',
                'fabric_store_name': store_name
            }, status=200)
        except FabricStore.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'Fabric Store with name {store_name} not found',
                'error_code': 'FABRIC_STORE_NOT_FOUND'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'Internal server error occurred',
                'error': str(e),
                'error_code': 'SERVER_ERROR'
            }, status=500)
    return JsonResponse({
        'status': 'error',
        'message': f'Method {request.method} not allowed. Use DELETE instead.',
        'error_code': 'METHOD_NOT_ALLOWED'
    }, status=405)

class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commandes.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return create_response(
                data=serializer.data,
                message="Command created successfully",
                status_code=status.HTTP_201_CREATED
            )
        
        # Enhanced error messages
        error_message = "Failed to create command due to validation errors"
        if 'client' in serializer.errors:
            error_message = "Invalid or missing client information"
        elif 'atelier' in serializer.errors:
            error_message = "Invalid or missing workshop information"

        elif 'date_livraison' in serializer.errors:
            error_message = "Invalid delivery date format or missing delivery date"
            
        return create_response(
            message=error_message,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return create_response(
                data=serializer.data,
                message="Command updated successfully",
                status_code=status.HTTP_200_OK
            )
        
        # Enhanced error messages for update
        error_message = "Failed to update command due to validation errors"
        if 'client' in serializer.errors:
            error_message = "Invalid client information provided"
        elif 'atelier' in serializer.errors:
            error_message = "Invalid workshop information provided"

        elif 'date_livraison' in serializer.errors:
            error_message = "Invalid delivery date format provided"
        elif 'status' in serializer.errors:
            error_message = "Invalid status value provided"
            
        return create_response(
            message=error_message,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def list(self, request, *args, **kwargs):
        # Get queryset and apply initial ordering
        queryset = self.filter_queryset(self.get_queryset().order_by('-id_commande'))
        
        # Filter by client_id if provided in query parameters
        user_id = request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(client=user_id)
            
        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return create_response(
                data=self.get_paginated_response(serializer.data).data,
                message="Commands retrieved successfully",
                status_code=status.HTTP_200_OK
            )
        
        # If pagination is not enabled
        serializer = self.get_serializer(queryset, many=True)
        return create_response(
            data=serializer.data,
            message="Commands retrieved successfully",
            status_code=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return create_response(
                data=serializer.data,
                message="Command retrieved successfully",
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return create_response(
                message="Failed to retrieve command",
                errors={"detail": str(e)},
                status_code=status.HTTP_404_NOT_FOUND
            )
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return create_response(
                message="Command deleted successfully",
                status_code=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return create_response(
                message="Failed to delete command",
                errors={"detail": str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        serializer.save()

class DemandeAtelierViewSet(viewsets.ModelViewSet):
    queryset = DemandeAtelier.objects.all()
    serializer_class = DemandeAtelierSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    

class CommandeAtelierFabricStoreViewSet(viewsets.ModelViewSet):
    queryset = CommandeAtelierFabricStore.objects.all()
    serializer_class = CommandeAtelierFabricStoreSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return create_response(
                data=serializer.data,
                message="Workshop-fabric store command created successfully",
                status_code=status.HTTP_201_CREATED
            )
        
        # Enhanced error messages
        error_message = "Failed to create workshop-fabric store command"
        if 'atelier' in serializer.errors:
            error_message = "Invalid or missing workshop information"
        elif 'fabric_store' in serializer.errors:
            error_message = "Invalid or missing fabric store information"

        elif 'date_livraison' in serializer.errors:
            error_message = "Invalid delivery date format or missing delivery date"
        
        return create_response(
            message=error_message,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

@csrf_exempt
def delete_commande_atelier_fabric_store(request, commande_id):
    if request.method == "DELETE":
        try:
            commande = CommandeAtelierFabricStore.objects.get(id=commande_id)
            commande.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Command deleted successfully',
                'data': {'command_id': commande_id}
            }, status=200)
        except CommandeAtelierFabricStore.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'Command with ID {commande_id} not found',
                'errors': {
                    'command_id': 'COMMAND_NOT_FOUND',
                    'detail': f'The command with ID {commande_id} does not exist in the database'
                }
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'Internal server error occurred',
                'errors': {
                    'server': str(e),
                    'detail': 'An unexpected error occurred while processing your request',
                    'suggestion': 'Please try again later or contact support if the issue persists'
                }
            }, status=500)
    return JsonResponse({
        'status': 'error',
        'message': f'Method {request.method} not allowed. Use DELETE instead.',
        'errors': {
            'method': 'METHOD_NOT_ALLOWED',
            'allowed_methods': ['DELETE'],
            'detail': f'The {request.method} method is not supported for this endpoint'
        }
    }, status=405)

class DemandeFabricStoreViewSet(viewsets.ModelViewSet):
    queryset = DemandeFabricStore.objects.all()
    serializer_class = DemandeFabricStoreSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = Product.objects.only('product_id', 'name', 'price', 'category', 'disponible', 'promo','image','rating','promo_price',)
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
                # Filter by category
        product_specific = self.request.query_params.get('product_id', None)
        if category:
            queryset = queryset.filter(product_id=product_specific)
               
        # Filter by owner
        owner = self.request.query_params.get('owner', None)
        if owner:
            queryset = queryset.filter(owner=owner)
            
        # Filter by availability
        disponible = self.request.query_params.get('disponible', None)
        if disponible is not None:
            disponible_bool = disponible.lower() == 'true'
            queryset = queryset.filter(disponible=disponible_bool)
            
        # Filter by promo
        promo = self.request.query_params.get('promo', None)
        if promo is not None:
            promo_bool = promo.lower() == 'true'
            queryset = queryset.filter(promo=promo_bool)
            
        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        # Sort by price, rating, or newest
        sort_by = self.request.query_params.get('sort', None)
        if sort_by:
            if sort_by == 'price_asc':
                queryset = queryset.order_by('price')
            elif sort_by == 'price_desc':
                queryset = queryset.order_by('-price')
            elif sort_by == 'rating':
                queryset = queryset.order_by('-rating')
            elif sort_by == 'newest':
                queryset = queryset.order_by('-product_id')
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return create_response(
                data=serializer.data,
                message="Product created successfully",
                status_code=status.HTTP_201_CREATED
            )
        return create_response(
            message="Failed to create product",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return create_response(
                data=serializer.data,
                message="Product updated successfully",
                status_code=status.HTTP_200_OK
            )
        return create_response(
            message="Failed to update product",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'], url_path='apply-promo')
    def apply_promo(self, request, pk=None):
        product = self.get_object()
        new_price = request.data.get('promo_price')
        
        if not new_price:
            return create_response(
                message="Promo price is required",
                errors={"promo_price": "This field is required"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            new_price = float(new_price)
            # Convert product.price to float for comparison
            if new_price >= float(product.price):
                return create_response(
                    message="Promo price must be less than regular price",
                    errors={"promo_price": "Value must be less than regular price"},
                    status_code=status.HTTP_400_BAD_REQUEST
                )
                
            # Apply the promotion
            product.promo = True
            product.promo_price = new_price
            product.save()
            
            # Get fresh data after save and return
            product = self.get_object()
            serializer = self.get_serializer(product)
            return create_response(
                data=serializer.data,
                message="Promotion applied successfully",
                status_code=status.HTTP_200_OK
            )
        except ValueError:
            return create_response(
                message="Invalid promo price",
                errors={"promo_price": "Must be a valid number"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], url_path='remove-promo')
    def remove_promo(self, request, pk=None):
        product = self.get_object()
        product.remove_promo()
        serializer = self.get_serializer(product)
        return create_response(
            data=serializer.data,
            message="Promotion removed successfully",
            status_code=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'], url_path='add-rating')
    def add_rating(self, request, pk=None):
        product = self.get_object()
        rating = request.data.get('rating')
        
        if not rating:
            return create_response(
                message="Rating is required",
                errors={"rating": "This field is required"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            rating_value = float(rating)
            if not 0 <= rating_value <= 5:
                return create_response(
                    message="Rating must be between 0 and 5",
                    errors={"rating": "Value must be between 0 and 5"},
                    status_code=status.HTTP_400_BAD_REQUEST
                )
                
            product.add_rating(rating_value)
            serializer = self.get_serializer(product)
            return create_response(
                data=serializer.data,
                message="Rating added successfully",
                status_code=status.HTTP_200_OK
            )
        except ValueError:
            return create_response(
                message="Invalid rating value",
                errors={"rating": "Must be a valid number between 0 and 5"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], url_path='add-image', parser_classes=[MultiPartParser, FormParser])
    def add_image(self, request, pk=None):
        product = self.get_object()
        image_file = request.data.get('image')
        is_primary = request.data.get('is_primary', 'false').lower() == 'true'
        
        if not image_file:
            return create_response(
                message="Image file is required",
                errors={"image": "This field is required"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product_image = product.add_image(image_file, is_primary)
            return create_response(
                data={
                    "id": product_image.id,
                    "is_primary": product_image.is_primary,
                    "image_url": request.build_absolute_uri(product_image.image.url)
                },
                message="Image added successfully",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return create_response(
                message="Failed to add image",
                errors={"detail": str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], url_path='set-primary-image')
    def set_primary_image(self, request, pk=None):
        product = self.get_object()
        image_id = request.data.get('image_id')
        
        if not image_id:
            return create_response(
                message="Image ID is required",
                errors={"image_id": "This field is required"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        success = product.set_primary_image(image_id)
        if success:
            serializer = self.get_serializer(product)
            return create_response(
                data=serializer.data,
                message="Primary image set successfully",
                status_code=status.HTTP_200_OK
            )
        else:
            return create_response(
                message="Image not found",
                errors={"image_id": f"No image found with ID {image_id}"},
                status_code=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['delete'], url_path='remove-image/(?P<image_id>[^/.]+)')
    def remove_image(self, request, pk=None, image_id=None):
        product = self.get_object()
        
        if not image_id:
            return create_response(
                message="Image ID is required",
                errors={"image_id": "This field is required"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        success = product.remove_image(image_id)
        if success:
            serializer = self.get_serializer(product)
            return create_response(
                data=serializer.data,
                message="Image removed successfully",
                status_code=status.HTTP_200_OK
            )
        else:
            return create_response(
                message="Image not found",
                errors={"image_id": f"No image found with ID {image_id}"},
                status_code=status.HTTP_404_NOT_FOUND
            )

@csrf_exempt
def delete_product(request, product_id):
    if request.method == "DELETE":
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return JsonResponse({'message': 'Product deleted successfully'}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product not found'}, status=404)
    return JsonResponse({'message': 'Invalid request method'}, status=400)

class AdvertisementsAtelierViewSet(viewsets.ModelViewSet):
    queryset = AdvertisementsAtelier.objects.all()
    serializer_class = AdvertisementsAtelierSerializer
    authentication_classes = [TokenAuthentication]
    pagination_class = CustomPagination

# =============== Messaging APIs ===============

# =============== Login APIs ===============
from django.contrib.auth.hashers import check_password

# Simple Unified Login View
class SimpleLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user_type = request.data.get("user_type")
        
        if not email or not password or not user_type:
            return create_response(
                message="Missing required login credentials",
                errors={"fields": "Email, password, and user type are required"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if user_type == "client":
                user = Client.objects.get(email=email)
                role = "client"
            elif user_type == "atelier":
                user = Atelier.objects.get(email=email)
                role = "atelier"
            elif user_type == "fabric_store":
                user = FabricStore.objects.get(email=email)
                role = "fabric_store"
            else:
                return create_response(
                    message="Invalid user type",
                    errors={"user_type": "User type must be client, atelier, or fabric_store"},
                    status_code=status.HTTP_400_BAD_REQUEST
                )
                
            if not user.check_password(password):
                return create_response(
                    message="Authentication failed",
                    errors={"credentials": "Invalid email or password"},
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
            
            # Generate token
            import datetime
            
            # Get or create Django user for authentication
            django_user, created = User.objects.get_or_create(
                username=str(user.user_id),
                defaults={"email": email}
            )
            
            # Create or get token
            token, created = Token.objects.get_or_create(user=django_user)
            token_value = token.key
            
            return create_response(
                data={
                    "user_id": user.user_id,
                    "token": token_value,
                    "role": role,
                    "phone": user.phone,
                    "address": user.address,
                    
                    "store_name": user.store_name,
                    "name": getattr(user, "name", None) or getattr(user, "store_name", None),
                    "register_commerce": request.build_absolute_uri(user.register_commerce.url) if user.register_commerce else None,
                    "expires": (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat()
                },
                message="Login successful",
                status_code=status.HTTP_200_OK
            )
            
        except (Client.DoesNotExist, Atelier.DoesNotExist, FabricStore.DoesNotExist):
            return create_response(
                message="User not found",
                errors={"user": "No user found with the provided email"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return create_response(
                message="Authentication error",
                errors={"server": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Page d'accueil de l'API
def home_view(request):
    return JsonResponse({
        "status": "success",
        "message": "Welcome to the Sewing App API!",
        "data": {
            "version": "0.0.2",
            "documentation": "/api/docs/"  # If you have documentation endpoint
        }
    })

