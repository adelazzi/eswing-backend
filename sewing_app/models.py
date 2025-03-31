import datetime
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Group, Permission
from django.db import models
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        if password:
            user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, password, **extra_fields)

def client_register_commerce_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Return path with preserved extension
    return f"register_commerce/Client/{instance.user_id}_{instance.name}.{ext}"

class Client(AbstractBaseUser):
    ROLE_CHOICES = [
        ("client", "Client"),  
    ]

    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Django handles hashing
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)
    register_commerce = models.ImageField(upload_to=client_register_commerce_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    business_info = models.TextField(blank=True, null=True)
    
    def check_password(self, raw_password):
        return raw_password.__eq__(self.password)
    
    def __str__(self):
        return f"Client: {self.name}"

def atelier_register_commerce_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Return path with preserved extension
    return f"register_commerce/Atelier/{instance.id}_{instance.name}.{ext}"

class Atelier(models.Model):
    ROLE_CHOICES = [
        ("atelier", "Atelier"), 
    ]

    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Django handles hashing
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)
    register_commerce = models.ImageField(upload_to=atelier_register_commerce_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    specialization = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    def check_password(self, raw_password):
        return raw_password.__eq__(self.password)
    def __str__(self):
        return f"Atelier: {self.name}"

def fabric_store_register_commerce_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Return path with preserved extension
    return f"register_commerce/Fabric_Store/{instance.user_id}_{instance.name}.{ext}"

class FabricStore(models.Model):
    ROLE_CHOICES = [
        
        ("fabric_store", "Fabric Store"),
    ]

    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Django handles hashing
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)
    materials_available = models.TextField(blank=True, null=True)
    register_commerce = models.ImageField(upload_to=fabric_store_register_commerce_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    materials_available = models.TextField(blank=True, null=True)
    def check_password(self, raw_password):
        return raw_password.__eq__(self.password)
    def __str__(self):
        return f"Fabric Store: {self.name}"
    
    

from django.db import models
from django.utils.timezone import now

class Commandes(models.Model):
    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("pending", "Pending"),
        ("validated", "Validated"),
        ("completed", "Completed"),
        ("refused", "Refused"),
    ]



    id_commande = models.AutoField(primary_key=True)
    client = models.IntegerField( null=True, blank=True, )
    atelier = models.IntegerField( null=True, blank=True)
    description = models.CharField(max_length=255)
    product = models.IntegerField( null=True, blank=True )
    quantity = models.IntegerField()
    image_command = models.ImageField(upload_to="orders/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in_progress", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    address = models.TextField()

    class Meta:
        unique_together = ("id_commande", "client", "atelier")

    def __str__(self):
        return f"Commande {self.id_commande} - {self.get_status_display()}"

from django.db import models
from django.utils.timezone import now

class DemandeAtelier(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    demande_id = models.AutoField(primary_key=True)
    atelier_id = models.IntegerField()  # Handled in frontend
    commande_id = models.IntegerField(db_index=True)  # Indexed for admin queries
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande {self.demande_id} - {self.get_status_display()}"

    @staticmethod
    def assign_first_atelier(commande_id):
        """Assigns the first atelier that requested the order."""
        first_request = DemandeAtelier.objects.filter(
            commande_id=commande_id, status="pending"
        ).order_by("created_at").first()

        if first_request:
            # Update Commande table
            from .models import Commande  # Avoid circular import

            commande = Commande.objects.get(commande_id=commande_id)
            commande.atelier_id = first_request.atelier_id
            commande.status = "validated"
            commande.save()

            # Mark this demande as accepted
            first_request.status = "accepted"
            first_request.save()

    @staticmethod
    def reset_commande_on_refusal(commande_id):
        """Resets the commande if the atelier refuses after being assigned."""
        from .models import Commande  # Avoid circular import

        # Remove all demandes for this commande
        DemandeAtelier.objects.filter(commande_id=commande_id).delete()

        # Reset the commande
        commande = Commande.objects.get(commande_id=commande_id)
        commande.atelier_id = None
        commande.status = "pending"
        commande.save()

from django.db import models
from django.utils.timezone import now

class CommandeAtelierFabricStore(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    MATERIAL_CHOICES = [
        ("cotton", "Cotton"),
        ("silk", "Silk"),
        ("denim", "Denim"),
        ("polyester", "Polyester"),
        ("wool", "Wool"),
        ("custom", "Custom Material"),  # Allows additional flexibility
    ]

    commande_fabric_id = models.AutoField(primary_key=True)
    atelier_id = models.IntegerField()  # Handled in frontend
    fabric_store_id = models.IntegerField(null=True, blank=True)  # Optional selection
    quantity = models.IntegerField()
    description = models.CharField(max_length=50, choices=MATERIAL_CHOICES, default="custom")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fabric Order {self.commande_fabric_id} - {self.get_status_display()}"

    @staticmethod
    def assign_fabric_store(commande_fabric_id, fabric_store_id):
        """Assigns a fabric store to a pending order."""
        commande = CommandeAtelierFabricStore.objects.get(commande_fabric_id=commande_fabric_id)
        if commande.status == "pending":
            commande.fabric_store_id = fabric_store_id
            commande.status = "accepted"
            commande.save()

    @staticmethod
    def reject_order(commande_fabric_id):
        """Marks an order as rejected."""
        commande = CommandeAtelierFabricStore.objects.get(commande_fabric_id=commande_fabric_id)
        commande.status = "rejected"
        commande.save()

class DemandeFabricStore(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    demande_fabric_id = models.AutoField(primary_key=True)
    commande_fabric_id = models.ForeignKey(
        "CommandeAtelierFabricStore",
        on_delete=models.CASCADE,
        related_name="demandes",
    )
    fabric_store_id = models.IntegerField()  # Handled in frontend
    price = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fabric Store {self.fabric_store_id} - {self.get_status_display()} (Commande {self.commande_fabric_id})"

    def accept(self):
        """Atelier accepts the price, assigns fabric store to the order."""
        self.status = "accepted"
        self.save()
        # Update CommandeAtelierFabricStore status
        self.commande_fabric_id.fabric_store_id = self.fabric_store_id
        self.commande_fabric_id.status = "accepted"
        self.commande_fabric_id.save()

    def reject(self):
        """Atelier rejects the offer, keeps the order open."""
        self.status = "rejected"
        self.save()


from django.db import models
import json
from django.core.validators import MinValueValidator, MaxValueValidator

def product_image_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Create a unique filename with better organization
    return f"products/{instance.category}/{instance.product_id}_{instance.owner}_{filename}"

class Product(models.Model):
    CATEGORY_CHOICES = [
        ("tshirt", "T-Shirt"),
        ("pants", "Pants"),
        ("dress", "Dress"),
        ("jacket", "Jacket"),
        ("other", "Other"),
    ]   
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="Product")  # This is the field causing the error
    owner = models.IntegerField(db_index=True)  # Better indexing
    disponible = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    promo = models.BooleanField(default=False)
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    image_list = models.JSONField(default=list, blank=True)  # Use JSONField instead of TextField
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, 
                                validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_ratings = models.IntegerField(default=0)
    rating_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Track creation time
    updated_at = models.DateTimeField(auto_now=True)  # Track updates
    
    def get_image_list(self):
        """Returns the list of image paths"""
        return self.image_list or []
    
    def set_image_list(self, images):
        """Sets the list of image paths"""
        self.image_list = images
    
    def add_image(self, image_path, make_primary=False):
        """Add an image path to the image list"""
        images = self.get_image_list()
        # Mark first image or requested image as primary
        is_primary = make_primary or len(images) == 0
        
        # If making this primary, unmark any other image
        if is_primary and images:
            # Check if the other images in the list have 'is_primary' attribute
            for i, img in enumerate(images):
                if isinstance(img, dict) and img.get('is_primary'):
                    img['is_primary'] = False
        
        # Add image as dict with is_primary flag
        if isinstance(image_path, str):
            image_entry = {'path': image_path, 'is_primary': is_primary}
        else:
            image_entry = image_path
            image_entry['is_primary'] = is_primary
            
        images.append(image_entry)
        self.set_image_list(images)
        self.save()
        return len(images) - 1  # Return index of added image
    
    def remove_image(self, index):
        """Remove an image at the specified index"""
        images = self.get_image_list()
        if 0 <= index < len(images):
            removed = images.pop(index)
            
            # If we removed the primary image, set first remaining image as primary
            was_primary = isinstance(removed, dict) and removed.get('is_primary', False)
            if was_primary and images:
                # Mark the first image as primary
                if isinstance(images[0], dict):
                    images[0]['is_primary'] = True
                else:
                    # Convert to dict if it's a string
                    images[0] = {'path': images[0], 'is_primary': True}
                    
            self.set_image_list(images)
            self.save()
            return removed
        return None
    
    def set_primary_image(self, index):
        """Set the primary image by index"""
        images = self.get_image_list()
        if 0 <= index < len(images):
            # Unmark all images
            for i, img in enumerate(images):
                if isinstance(img, dict):
                    img['is_primary'] = False
                else:
                    # Convert string to dict
                    images[i] = {'path': img, 'is_primary': False}
                    
            # Mark the selected image as primary
            if isinstance(images[index], dict):
                images[index]['is_primary'] = True
            else:
                images[index] = {'path': images[index], 'is_primary': True}
                
            self.set_image_list(images)
            self.save()
            return True
        return False
    
    @property
    def primary_image(self):
        """Returns the primary image path or legacy image"""
        images = self.get_image_list()
        if images:
            # Look for image with is_primary flag
            for img in images:
                if isinstance(img, dict) and img.get('is_primary'):
                    return img.get('path')
            
            # Default to first image if no primary found
            if isinstance(images[0], dict):
                return images[0].get('path')
            return images[0]
        
        return self.image.url if self.image else None
    
    def add_rating(self, new_rating):
        """Add a customer rating to this product"""
        if not 0 <= new_rating <= 5:
            raise ValueError("Rating must be between 0 and 5")
            
        self.total_ratings += 1
        self.rating_sum += new_rating
        self.calculate_rating()
        return self.rating
        
    def calculate_rating(self):
        """Recalculate product rating based on total ratings and sum"""
        if self.total_ratings > 0:
            self.rating = self.rating_sum / self.total_ratings
            self.save()
        return self.rating

    def apply_promo(self, new_price):
        """Applies a promotional price to the product."""
        if new_price >= self.price:
            raise ValueError("Promotional price must be lower than regular price")
            
        self.promo = True
        self.promo_price = new_price
        self.save()
        return True

    def remove_promo(self):
        """Removes the promotional price."""
        self.promo = False
        self.promo_price = None
        self.save()
        return True
        
    @property
    def current_price(self):
        """Returns the current effective price (promo or regular)"""
        return self.promo_price if self.promo and self.promo_price else self.price
        
    @property
    def discount_percentage(self):
        """Returns the discount percentage if on promotion"""
        if self.promo and self.promo_price and self.price:
            return round((1 - (self.promo_price / self.price)) * 100)
        return 0

    class Meta:
        indexes = [
            models.Index(fields=["promo"], name="product_promo_idx"),
            models.Index(fields=["owner"], name="product_owner_idx"),
            models.Index(fields=["category"], name="product_category_idx"),
            models.Index(fields=["rating"], name="product_rating_idx"),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.category}) - {self.product_id}"

from django.db import models

def advertisement_image_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Return path with preserved extension
    return f"atelier_ads/{instance.advertisement_id}_{instance.title}.{ext}"

class AdvertisementsAtelier(models.Model):
    advertisement_id = models.CharField(max_length=10, primary_key=True)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="ads")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.IntegerField()
    image = models.ImageField(upload_to=advertisement_image_path, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title

