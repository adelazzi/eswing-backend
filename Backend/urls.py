from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sewing_app.views import (
    ClientViewSet, 
    AtelierViewSet, 
    FabricStoreViewSet,
    CommandeViewSet, 
    DemandeAtelierViewSet, 
    CommandeAtelierFabricStoreViewSet, 
    DemandeFabricStoreViewSet, 
    ProductViewSet, SimpleLoginView,
    AdvertisementsAtelierViewSet,
        delete_fabric_store, 
    delete_product,
    home_view,delete_atelier,delete_client,

)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# Création d'un routeur pour les ViewSets
router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'ateliers', AtelierViewSet, basename='atelier')
router.register(r'fabric-stores', FabricStoreViewSet, basename='fabricstore')
router.register(r'commandes', CommandeViewSet, basename='commande')
router.register(r'demandes-ateliers', DemandeAtelierViewSet, basename='demandeatelier')
router.register(r'commandes-atelier-fabric-store', CommandeAtelierFabricStoreViewSet, basename='commandeatelierfabricstore')
router.register(r'demandes-fabric-store', DemandeFabricStoreViewSet, basename='demandefabricstore')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'advertisements-ateliers', AdvertisementsAtelierViewSet, basename='advertisementsatelier')

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    # Routes ViewSets (gérées automatiquement)
    path('api/', include(router.urls)),
    path('api/ateliers/delete/<int:atelier_id>/', delete_atelier, name='delete_atelier'),
    path('api/clients/delete/<int:client_id>/', delete_client, name='delete_client'),
    path('api/fabric-stores/delete/<int:fabric_store_id>/', delete_fabric_store, name='delete_fabric_store'),
    path('api/auth/login/', SimpleLoginView.as_view(), name='login'),
    path('api/products/delete/<int:product_id>/', delete_product, name='delete_product'),
    
    # Product specific endpoints
    path('api/products/<int:pk>/apply-promo/', ProductViewSet.as_view({'post': 'apply_promo'}), name='product-apply-promo'),
    path('api/products/<int:pk>/remove-promo/', ProductViewSet.as_view({'post': 'remove_promo'}), name='product-remove-promo'),
    path('api/products/<int:pk>/add-rating/', ProductViewSet.as_view({'post': 'add_rating'}), name='product-add-rating'),
    path('api/products/<int:pk>/add-image/', ProductViewSet.as_view({'post': 'add_image'}), name='product-add-image'),
    path('api/products/<int:pk>/set-primary-image/', ProductViewSet.as_view({'post': 'set_primary_image'}), name='product-set-primary-image'),
    path('api/products/<int:pk>/remove-image/<int:image_id>/', ProductViewSet.as_view({'delete': 'remove_image'}), name='product-remove-image'),
    path('api/products/<int:pk>/images/', ProductViewSet.as_view({'get': 'get_images'}), name='product-images'),

    ]

# Servir les fichiers médias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ProductViewSet
"""

# Endpoints:
# Clients:
#   GET /api/clients/
#   POST /api/clients/
#   GET /api/clients/{id}/
#   PUT /api/clients/{id}/
#   DELETE /api/clients/{id}/
#   POST /api/client/login/
#   DELETE /api/clients/delete/<str:client_id>/

# Ateliers:
#   GET /api/ateliers/
#   POST /api/ateliers/
#   GET /api/ateliers/{id}/
#   PUT /api/ateliers/{id}/
#   DELETE /api/ateliers/{id}/
#   POST /api/atelier/login/
#   DELETE /api/ateliers/delete/<str:atelier_name>/

# Fabric Stores:
#   GET /api/fabric-stores/
#   POST /api/fabric-stores/
#   GET /api/fabric-stores/{id}/
#   PUT /api/fabric-stores/{id}/
#   DELETE /api/fabric-stores/{id}/
#   POST /api/fabric_store/login/
#   DELETE /api/fabric-stores/delete/<str:fabric_store_name>/

# Commandes:
#   GET /api/commandes/
#   POST /api/commandes/
#   GET /api/commandes/{id}/
#   PUT /api/commandes/{id}/
#   DELETE /api/commandes/{id}/

# Demandes Ateliers:
#   GET /api/demandes-ateliers/
#   POST /api/demandes-ateliers/
#   GET /api/demandes-ateliers/{id}/
#   PUT /api/demandes-ateliers/{id}/
#   DELETE /api/demandes-ateliers/{id}/

# Commandes Atelier Fabric Store:
#   GET /api/commandes-atelier-fabric-store/
#   POST /api/commandes-atelier-fabric-store/
#   GET /api/commandes-atelier-fabric-store/{id}/
#   PUT /api/commandes-atelier-fabric-store/{id}/
#   DELETE /api/commandes-atelier-fabric-store/{id}/

# Demandes Fabric Store:
#   GET /api/demandes-fabric-store/
#   POST /api/demandes-fabric-store/
#   GET /api/demandes-fabric-store/{id}/
#   PUT /api/demandes-fabric-store/{id}/
#   DELETE /api/demandes-fabric-store/{id}/

# Products:
#   GET /api/products/
#   POST /api/products/
#   GET /api/products/{id}/
#   PUT /api/products/{id}/
#   DELETE /api/products/{id}/
#   POST /api/products/{id}/apply-promo/
#   POST /api/products/{id}/remove-promo/
#   POST /api/products/{id}/add-rating/
#   POST /api/products/{id}/add-image/
#   POST /api/products/{id}/set-primary-image/image
#   DELETE /api/products/{id}/remove-image/{image_id}/
#   GET /api/products/{id}/images/

# Advertisements Ateliers:
#   GET /api/advertisements-ateliers/
#   POST /api/advertisements-ateliers/
#   GET /api/advertisements-ateliers/{id}/
#   PUT /api/advertisements-ateliers/{id}/
#   DELETE /api/advertisements-ateliers/{id}/

# Messages:
#   GET /api/messages/
#   POST /api/messages/
#   GET /api/messages/{id}/
#   PUT /api/messages/{id}/
#   DELETE /api/messages/{id}/
#   GET /api/messages/conversation/?user1_id=X&user1_role=Y&user2_id=Z&user2_role=W
#   GET /api/messages/conversations/?user_id=X&user_role=Y
#   POST /api/messages/mark-read/
#   GET /api/messages/unread-count/?user_id=X&user_role=Y

# Conversations:
#   GET /api/conversations/
#   GET /api/conversations/?user_id=X&user_role=Y
#   GET /api/conversations/{id}/
#   POST /api/conversations/{id}/mark-as-read/
"""