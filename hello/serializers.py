from rest_framework import serializers
from django.contrib.auth import (authenticate, get_user_model, password_validation,) 
from .models import Profilepik ,User,Blog 

class UserRegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['name','email','password','password2',]
        extra_kwargs ={
            'password':{'write_only':True},
            #'password2':{'write_only':True}
            }
# validate passworde
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError("Both passwords do not match")
        return attrs
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
 
        
    


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    class Meta:
         model = User
         fields = fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = "__all__"


class UserPikSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profilepik
        fields =  ['User','background_image','images','postby_name']
        
class BlogSerializer(serializers.ModelSerializer):
    
    pik = UserPikSerializer(read_only=True)
    
    class Meta:
        model = Blog
        fields =  ['tag_name','blog_name','created_date','update_date','post_by','images','pik']
