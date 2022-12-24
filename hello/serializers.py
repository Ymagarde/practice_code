from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import* 
from urllib.parse import urlencode as original_urlencode

from django.utils.encoding import smart_str, force_bytes,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util




class UserRegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['name','email','password','password2',]
        extra_kwargs ={
            'password':{'write_only':True},
            'password2':{'write_only':True}
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
        
        

        
           
class UserchangepasswordSerializer(serializers.Serializer):
    
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and confirm password doesn't match")
        user.set_password(password)
        user.save()
        return attrs
        
    class Meta:
        model = User
        fields = ['password','password2']
        
        
        
        
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token',token)
            link = 'http://127.0.0.1:8000/reset-pasword/'+uid+'/'+token +'/'
            
            print('password Reset link',link)
            
            email_body = 'click Following Link toReset Your password \n'+link
            data = {'email_body':email_body,'to_email':user.email,'email_subject':'Reset your password'}
            
            Util.send_email(data)
        return Response({r'success': 'we have sent you a link to reset your password'},status=status.HTTP_200_OK)
            
        
    class Meta:
        model = User
        fields = ['email']




class UserPasswordResetSerializar(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['password','password2']
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("password and confirm password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Token is not valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not valid or Expired')

   
            
    
        
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = "__all__"


class UserPikSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profilepik
        fields =  ['User','background_image','images','postby_name']
        
class BlogSerializer(serializers.ModelSerializer):
    pik = UserPikSerializer(many=True,read_only=True)
    class Meta:
        model = Blog
        fields =  ['tag_name','blog_name','created_date','update_date','post_by','images','pik']
