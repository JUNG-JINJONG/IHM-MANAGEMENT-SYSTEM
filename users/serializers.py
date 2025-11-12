from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer, Supplier

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """사용자 기본 Serializer"""
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'user_type', 'company_name', 
                  'contact_phone', 'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CustomerSerializer(serializers.ModelSerializer):
    """고객사 Serializer"""
    user_info = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'user', 'user_info', 'company_name', 'business_number', 
                  'address', 'contact_person', 'contact_phone', 'contact_email',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SupplierSerializer(serializers.ModelSerializer):
    """공급업체 Serializer"""
    user_info = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Supplier
        fields = ['id', 'user', 'user_info', 'company_name', 'business_number',
                  'address', 'contact_person', 'contact_phone', 'contact_email',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """사용자 회원가입 Serializer"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'user_type',
                  'company_name', 'contact_phone', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
