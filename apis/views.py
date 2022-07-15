import profile
from venv import create
from django.shortcuts import render

# Create your views here.
from .models import User,Profile
from .serializer import RegisterSerializer,MyTokenObtainPairSerializer,ProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import  JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework import generics,mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication ,BasicAuthentication,TokenAuthentication
from rest_framework import viewsets
from django.shortcuts import get_object_or_404




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class   = RegisterSerializer

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class   = MyTokenObtainPairSerializer


#function based api with request
#two way to create function based apis 


# @csrf_exempt
@api_view(['GET','POST'])
def ProfileFunView(request):

    if request.method == 'GET':
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
            # return JsonResponse(serializer.data,status=201)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


# @csrf_exempt
@api_view(['GET','PUT','DELETE'])
def UpdateProfileView(request, pk):
    try:
        profle  = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        serializer =  ProfileSerializer(profle)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = ProfileSerializer(profle,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status = status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        profle.delete()
        return Response(status=status.HTTP_201_CREATED)



#class based apis start


#create api with ApiView
class ApiViewProfile(APIView):

    def get(self,request):

        data =  Profile.objects.all()
        serializer =  ProfileSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self,request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateProfile(APIView):

    def get_object(self,id):
        return Profile.objects.get(id=id)
        # return HttpResponse(status)

    def get(self,request,id):
        data = self.get_object(id)
        print(data)
        serializer = ProfileSerializer(data)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,id):
        profile_id =self.get_object(id)
        print(profile_id)
        serializer = ProfileSerializer(profile_id,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self,request,id):
        profile_id = self.get_object(id)
        profile_id.delete()
        return Response(status=status.HTTP_200_OK)



#create api to Generic mixins view 
class GenricApiProfileView(generics.CreateAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    
    serializer_class =ProfileSerializer
    queryset =Profile.objects.all()

    lookup_field = 'id'
    authentication_classes = [SessionAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated]
    #to create an token use this and add  (rest_framework.authtoken) in setting.py file and get token add in postman than run
    # authentication_classes = [TokenAuthentication]

    def get(self,request,id=None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request)

    def put(self,request,id = None):
        return self.update(request,id)

    def delete(self,request,id):
        return self.destroy(request,id)

# create api using Viewsets class based view 

class ViewsetsApi(viewsets.ViewSet):

    def list(self,request):
        profile_data = Profile.objects.all()
        serializer = ProfileSerializer(profile_data, many =True)
        return Response(serializer.data ,status=status.HTTP_200_OK)

    def create(self,request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

    def retrieve(self,request,pk = None):
        queryset =Profile.objects.all()
        profile_data = get_object_or_404(queryset,pk=pk)
        serializer = ProfileSerializer(profile_data)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def update(self,request, pk):
        profile_id = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(profile_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors)

    def destroy(Self,request,pk):
        profile_id = Profile.objects.get(pk=pk)
        profile_id.delete()
        return Response(status=status.HTTP_200_OK)


#create api using genericviewset mixin 
#there urls in router register only
class GenricviewsetProfileView(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


#create apis using model viewset

class ModelViewsetAPi(viewsets.ModelViewSet):

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


        

