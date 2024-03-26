from django.shortcuts import render

from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action



from api.models import Movie
from api.serializers import MovieSerialzer

# Create your views here.


# url: localhost:8000/helloworld
# get
# response {"message":"helloworld"}
class HelloworldView(APIView):

    def get(self,request,*args,**kwargs):

        context={"message":"helloworld"}
        return Response(data=context)


class MorningView(APIView):

    def get(self,request,*args,**kwargs):

        context={"message":"goodmorning"}
        return Response (data=context)
    

# url loclhost:8000/addition/
# method post
# data("num1","num2")
class AdditionView(APIView):

    def post (self,request,*args,**kwargs):

        n1=request.data.get("num1")
        n2=request.data.get("num2")

        result=int(n1)+ int(n2)
        context={"result":result}

        return Response(data=context)
    
      
# url localhost:8000/division/
# method  post
# data("num1","num2")
class DivisionView(APIView):

    def post(self,request,*args,**kwargs):

        n1=request.data.get("num1")
        n2=request.data.get("num2")

        result=int(n1)/int(n2)
        context={"result":result}

        return Response(data=context)


# url: localhost:8000/bmi/
# method: post
# data=("height":int, "weight":int)
class BmiView(APIView):

    def post(self,request,*args,**kwargs):

        height_in_cm=request.data.get("height")
        weight_in_kg=request.data.get("weight")

        heigth_in_m=height_in_cm/100

        bmi=weight_in_kg/(heigth_in_m**2)
        context={"bmi":bmi}
        
        return Response(data=context)
    

# url : localhost:8000/bmr/
# method: post
# data("height":160,"weight":50,"gender":"male","age":21)
class CaloryCalculatorView(APIView):

    def post(self,request,*args,**kwargs):

        height=int(request.data.get("height"))
        weight=int(request.data.get("weight"))
        gender=request.data.get("gender")
        age=int(request.data.get("age"))

        bmr=0

        if gender=="male":
            # 10 * weight (kg) + 6.25 * height(cm) - 5 * age(y) + 5 for (man)
            bmr=(10*weight)+(6.25*height)-(5*age)+5
        elif gender=="female":
            # 10 * weight(kg) + 6.25 * height(cm) - 5 * age(y) - 161 for ​(woman)
            bmr=(10*weight)+(6.25*height)-(5*age)-161
        context={"bmr":bmr}
        return Response(data=context)
        

# album CRUD
    
# list all ablum
    # url : localhost:8000/api/ablum/
    # method : get
    # data : nill
# create album
    # url: localhost:8000/api/album/
    # method: post
    # data: {}
class AlbumlistView(APIView):

    def get(self,request,*args,**kwargs):
         
        qs=Movie.objects.all()
        return Response(data=qs)
    
    
    def post(self,request,*args,**kwargs):

        # context={"message":"logic for create album"}

        return Response()
    



class MovieListCreateView(APIView):

    def get(self,request,*args,**kwargs):

        qs=Movie.objects.all()
        serializer_instance=MovieSerialzer(qs,many=True) #serializing

        return Response (data=serializer_instance.data)
    


    def post(self,request,*args,**kwargs):

        data=request.data

        serializer_instance=MovieSerialzer(data=data)

        if serializer_instance.is_valid():
            serializer_instance.save()

            return Response(data= serializer_instance.data)  #deserializing
        else:

            return Response(data=serializer_instance.errors)
        



class MovieDetailUpdateView(APIView):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            qs=Movie.objects.get(id=id)

            serializer_instance=MovieSerialzer(qs)
            return Response(data=serializer_instance.data)
        except:

            context={"message":"requested resource does not exist"}
            return Response(data=context,status=status.HTTP_404_NOT_FOUND)

            

    def delete(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        try:
            Movie.objects.get(id=id).delete()

            return Response(data={"message":"deleted"})
        
        except:

            return Response(data={"messgage":"resource not found"},status=status.HTTP_404_NOT_FOUND)


    def put(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        movie_object=Movie.objects.get(id=id)

        data=request.data

        serializer_instance=MovieSerialzer(data=data,instance=movie_object)

        if serializer_instance.is_valid():
            serializer_instance.save()

            return Response(data=serializer_instance.data,status=status.HTTP_200_OK)
        else:
            return Response(data=serializer_instance.errors,status=status.HTTP_404_NOT_FOUND)




class MovieViewsetView(ViewSet):

    def list(self,request,*args,**kwargs):
        qs=Movie.objects.all()
        serializer_instance=MovieSerialzer(qs,many=True)

        return Response(data=serializer_instance.data,status=status.HTTP_200_OK)

    def create(self,request,*args,**kwargs):
        data=request.data
        serializer_instance=MovieSerialzer(data=data)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data,status=status.HTTP_200_OK)       
        else:
            return Response(data=serializer_instance.errors)

    def retrieve(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        try:
            data=Movie.objects.get(id=id)
            serializer_instance=MovieSerialzer(data)
            return Response(data=serializer_instance.data,status=status.HTTP_200_OK)
        except:
            return Response(data={"message":"not found"},status=status.HTTP_404_NOT_FOUND)

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")

        movie_obj=Movie.objects.get(id=id)
        data=request.data
        serializer_instance=MovieSerialzer(data=data,instance=movie_obj)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data,status=status.HTTP_200_OK)       
        else:
            return Response(data=serializer_instance.errors,status=status.HTTP_404_NOT_FOUND)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Movie.objects.get(id=id).delete()

        return Response(data={"message":"deleted"},status=status.HTTP_200_OK)

    @action(methods=["get"],detail=False)
    def genres(self,request,*args,**kwargs):

        qs=Movie.objects.values_list("genre",flat=True).distinct()
        return Response(data=qs)




class MovieGenreView(APIView):

    def get(self,request,*args,**kwargs):

        qs=Movie.objects.all().values_list("genre",flat=True).distinct()

        return Response(data=qs)




class MovieLanguageView(APIView):

    def get(self,request,*args,**kwargs):

        qs=Movie.objects.all().values_list("language",flat=True).distinct()
        
        return Response(data=qs)



