from rest_framework import serializers
from .models import (
    User, Item, appr_ppmp, PPMP, PR_Items, FileMetadata, PR,
    Pr_identifier, Checkout, CheckoutItems, CSV, Category, 
    VerificationCode
)



class UserSerializer(serializers.ModelSerializer):
    budget = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = User
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    unit_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Item
        fields = '__all__'

class ApprPPMPSerializer(serializers.ModelSerializer):
    unit_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    estimated_budget = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = appr_ppmp
        fields = '__all__'

class PPMPSerializer(serializers.ModelSerializer):
    unit_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    estimate_budget = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = PPMP
        fields = '__all__'

class PRItemsSerializer(serializers.ModelSerializer):
    unit_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = PR_Items
        fields = '__all__'

class FileMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMetadata
        fields = '__all__'

class PRSerializer(serializers.ModelSerializer):
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = PR
        fields = '__all__'

class PrIdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pr_identifier
        fields = '__all__'

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = '__all__'

class CheckoutItemsSerializer(serializers.ModelSerializer):
    unit_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    estimate_budget = serializers.DecimalField(max_digits=10, decimal_places=2)
    checkout = CheckoutSerializer()
    class Meta:
        model = CheckoutItems
        fields = '__all__'

class CSVSerializer(serializers.ModelSerializer):
    Price = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = CSV
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = '__all__'
