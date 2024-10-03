from api.models import CustomUser, Inbound, Outbound, Inventory
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password' : {'write_only' : True}}
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['username'] = user.username
        token['role'] = user.role
            
        return token

class InboundSerializer(serializers.ModelSerializer):
    category = serializers.CharField(required=False, allow_blank = True)
    location = serializers.CharField(required=False, allow_blank = True)
    name = serializers.CharField(required=False, allow_blank = True)
    
    class Meta:
        model = Inbound
        fields = ['id', 'ref', 'date', 'sku', 'quantity', 'supplier', 'status', 'category', 'location', 'name']
        
    def validate(self, data):
        required_fields = ['date', 'sku', 'quantity', 'supplier']
        
        if data.get('status') == 'received':
            required_fields.extend(['category', 'location', 'name'])
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise serializers.ValidationError(f"Insufficient data received: {', '.join(missing_fields)} are required")
        
        return data
    
    def create(self, validated_data):
        inbound_count = Inbound.objects.count() + 1
        validated_data['ref'] = f"INBOUND{inbound_count:03d}"
        category = validated_data.pop('category', None,)
        location = validated_data.pop('location', None)
        name = validated_data.pop('name', None)
        inbound_entry = super().create(validated_data)
        
        if inbound_entry.status == 'received':
            Inventory.objects.create(
                sku=inbound_entry.sku,
                category=category,
                name=name,
                location=location,
                quantity=inbound_entry.quantity,
                supplier=inbound_entry.supplier
            )
        return inbound_entry
    
    def update(self, instance, validated_data):
        
        # Ensure status is being updated to "received"
        if instance.status != 'received' and validated_data['status'] == 'received':
            category = validated_data.get('category', None)
            location = validated_data.get('location', None)
            name = validated_data.get('name', None)
            
            Inventory.objects.create(
                sku=instance.sku,
                category=category,
                name=name,
                location=location,
                quantity=instance.quantity,
                supplier=instance.supplier
            )
        
        return super().update(instance, validated_data)

            
            
       
class OutboundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outbound
        fields = ['id', 'ref', 'date', 'sku', 'quantity', 'destination', 'status']
    
    def validate(self, data):
        required_fields = ['date', 'sku', 'quantity', 'destination']
    
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise serializers.ValidationError(f"Insufficient data received: {', '.join(missing_fields)} are required")
        
        return data

    def create(self, validated_data):
        
        sku = validated_data['sku']
        quantity = validated_data['quantity']
        
        try:
            inventory = Inventory.objects.get(sku=sku)
        except Inventory.DoesNotExist:
            raise serializers.ValidationError(f"No inventory found for SKU {sku}.")
        
        if quantity > inventory.quantity:
            raise serializers.ValidationError("Insufficient inventory to fulfill the outbound request.")
        
        inventory.quantity -= quantity
        if inventory.quantity <= 0:
            inventory.delete()  
        else:
            inventory.save()
        
        outbound_count = Outbound.objects.count() + 1
        validated_data['ref'] = f"OUTBOUND{outbound_count:03d}"
        
            
        return super().create(validated_data)
    
class InventorySerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=False)
    
    class Meta:
        model = Inventory
        fields = ['id','sku', 'category', 'name', 'location', 'quantity', 'supplier', 'date']
        
    def validate(self, data):
        required_fields = ['sku', 'category', 'name', 'location', 'quantity', 'supplier']
        
        if self.context['request'].method == 'POST':
           required_fields.append('date')

        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise serializers.ValidationError(f"Insufficient data received: {', '.join(missing_fields)} are required")

        return data
    
    def create(self, validated_data):
        date = validated_data.pop('date')
        
        inventory_entry = super().create(validated_data)
        
        inbound_count = Inbound.objects.count() + 1
        ref = f"INBOUND{inbound_count:03d}"
        status = 'received'
        
        inbound_item = Inbound.objects.create(
            ref = ref,
            date = date,
            sku = inventory_entry.sku,
            quantity = inventory_entry.quantity,
            supplier = inventory_entry.supplier,
            status = status
        )
        
        return inventory_entry
    
    def delete(self, instance):
        sku_to_delete = instance.sku
        Inbound.objects.filter(sku=sku_to_delete).delete()
        instance.delete()

    