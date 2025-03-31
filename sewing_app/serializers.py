from rest_framework import serializers
from .models import (
    Client, Atelier, FabricStore, Commandes, DemandeAtelier,
    CommandeAtelierFabricStore, DemandeFabricStore, Product, AdvertisementsAtelier,

)

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class AtelierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atelier
        fields = '__all__'

class FabricStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = FabricStore
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commandes
        fields = '__all__'

class DemandeAtelierSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeAtelier
        fields = '__all__'

class CommandeAtelierFabricStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandeAtelierFabricStore
        fields = '__all__'

class DemandeFabricStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeFabricStore
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    image_list = serializers.ListField(required=False, write_only=True)
    images = serializers.SerializerMethodField()
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    primary_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'product_id', 'name', 'owner', 'disponible', 'description', 
            'category', 'price', 'promo', 'promo_price', 'image',
            'rating', 'total_ratings', 'rating_sum',
            'created_at', 'updated_at', 'image_list', 'images',
            'current_price', 'discount_percentage', 'primary_image_url'
        ]
        read_only_fields = ['rating', 'total_ratings', 'rating_sum', 'created_at', 'updated_at']
    
    def get_images(self, obj):
        return obj.get_image_list()
    
    def get_primary_image_url(self, obj):
        request = self.context.get('request', None)
        primary_image = obj.primary_image
        if request is not None and primary_image:
            return request.build_absolute_uri(primary_image)
        return None
        
    def validate(self, data):
        """
        Validate that promo_price is less than regular price if promo is True
        """
        if data.get('promo') and data.get('promo_price') and data.get('price'):
            if data['promo_price'] >= data['price']:
                raise serializers.ValidationError({"promo_price": "Promotional price must be less than regular price"})
        return data
    
    def create(self, validated_data):
        # Remove image_list from data before creating product
        image_list = validated_data.pop('image_list', [])
        product = Product.objects.create(**validated_data)
        
        # Add images if provided
        for image_path in image_list:
            product.add_image(image_path)
            
        return product
    
    def update(self, instance, validated_data):
        # Handle image_list separately
        image_list = validated_data.pop('image_list', None)
        
        # Update regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update image list if provided
        if image_list is not None:
            instance.set_image_list(image_list)
            
        instance.save()
        return instance

class AdvertisementsAtelierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementsAtelier
        fields = '__all__'
