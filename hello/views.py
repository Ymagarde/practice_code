
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import* 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

### filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import filters








def get_tokens_for_user(user):

    ''' THIS FUNCTION PROVIDE TOKEN CREATE MANUALLY '''

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterAPIView(APIView):


    def post(self,request):

        ''' THIS FUNCTION PROVIDE USER REGISTER '''

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user= serializer.save()
            token = get_tokens_for_user(user)
            response_data = {'user':serializer.data}
            return Response({"token":token, "msg":"Registration Succesfull "},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    def post(self,request, format=None):

        ''' THIS FUNCTION PROVIDE USER LOGIN '''

        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.data.get('password')
            email    = serializer.data.get('email')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)

                return Response({"token":token, "msg":"login success"},status = status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':["username or password is not valid"]}},)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ProfiledataView(APIView):
    permission_classes = [IsAuthenticated]

    ''' THIS FUNCTION PROVIDE USER PROFILE DETAILS '''

    def get(self,request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status = status.HTTP_200_OK)
        

class ProfilepikView(APIView):
    permission_classes = [IsAuthenticated]
     

    def post(self,request, format=None):

        ''' THIS FUNCTION PROVIDE POST PRFILEPIK DATA '''

        serializer = UserPikSerializer(data=request.data)
        if serializer.is_valid():
            profile_data= serializer.save()
            print(profile_data)
            return Response((serializer.data),status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
   
    def get(self, request,):
        
        ''' THIS FUNCTION PROVIDE GET PRFILEPIK DATA '''
    
        profile = Profilepik.objects.all()
        serializers = UserPikSerializer(profile, many=True)
        return Response(serializers.data)
    
class uProfilepikView(APIView):
    
    ''' THIS CLASS PROVIDE CRUD OPERATION PRFILEPIK DATA MODEL '''
    
    def get_object(self, pk):
        try:
            return Profilepik.objects.get(pk=pk)
        except Profilepik.DoesNotExist:
            raise Http404
         
    def get(self, request,pk): 
        profile = self.get_object(pk)
        serializers = UserPikSerializer(profile)
        return Response(serializers.data)
    
    
    def put(self, request, pk, format=None):
        u_id = self.get_object(pk)
        serializers = UserPikSerializer(u_id, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user_id = self.get_object(pk)
        user_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class blogView(APIView):


    def post(self,request):

        ''' THIS FUNCTION PROVIDE Blog data post '''

        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
    def get(self,request):
        
        ''' THIS FUNCTION PROVIDE GET DATA '''
        
        blog_data = Blog.objects.all()
        serializers = BlogSerializer(blog_data,many=True)
        return Response(serializers.data)
    
    
    
class blogList(generics.ListAPIView):
    
    ''' THIS FUNCTION PROVIDE filter_by filterset_fields '''
    
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tag_name','blog_name','post_by']       

class blogListView(generics.ListAPIView):
    
    ''' THIS FUNCTION PROVIDE filter_by ordering_fields '''
    
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['tag_name','blog_name','post_by']

class SblogListView(generics.ListAPIView):
    
    ''' THIS FUNCTION PROVIDE filter_by search_fields '''
    
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tag_name','blog_name','post_by']
    
    

