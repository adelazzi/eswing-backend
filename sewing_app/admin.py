from django.contrib import admin
from .models import Client, Atelier, FabricStore, Commandes, Product, DemandeAtelier, DemandeFabricStore

# Register your models here.
admin.site.register(Client)
admin.site.register(Atelier)
admin.site.register(FabricStore)
admin.site.register(Commandes)
admin.site.register(Product)
admin.site.register(DemandeAtelier)
admin.site.register(DemandeFabricStore)