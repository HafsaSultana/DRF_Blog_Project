from django.db.models import Q
from django.shortcuts import render
from .serializers import UserSerializers, UserLoginSerializer, BlogPostSerializer
from .models import User, BlogPost
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.http import Http404
from django.contrib.auth import authenticate

# Create your views here.


class UserRegister(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (AllowAny,)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        # email = "Hafsa@Gmail.com"
        # print('---------------', self.normalize_email(email))

        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        response = {
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'User Login Successfully',
            'email': serializer.data['email'],
            'role': serializer.data['role'],
            'token': token.key
        }
        return Response(response)

class BlogPostViewset(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class BlogPostList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        return Response({'statusCode': status.HTTP_200_OK})
    # def post(self, request, formate=None):
    #     try:
    #         serializer = BlogPostSerializer(data=request.data)
    #
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response({'Data': serializer.data,
    #                             'message': 'Blog created Successfully',
    #                              'statusCode': status.HTTP_200_OK})
    #
    #         return Response({'Data': serializer.errors,
    #                          'message': 'Something went wrong',
    #                          'statusCode': status.HTTP_400_BAD_REQUEST})
    #
    #     except Exception as e:
    #         print(e)
    #         return Response({'Data': e,
    #                          'message': 'Something went wrong',
    #                          'statusCode': status.HTTP_400_BAD_REQUEST})

    def get(self, request, formate=None):
        try:
            blog = BlogPost.objects.filter(author=request.user)
            if request.GET.get('search'):
                search = request.GET.get('search')
                blog = blog.filter(Q(title__icontains = search) | Q(blog_text__icontains=search))

            serializer = BlogPostSerializer(blog, many=True)
            return Response({'Data': serializer.data,
                            'message': 'Blog Successfully',
                             'statusCode': status.HTTP_200_OK})


        except Exception as e:
            print(e)
            return Response({'Data': e,
                             'message': 'Something went wrong',
                             'statusCode': status.HTTP_400_BAD_REQUEST})


class BlogPostDetail(APIView):
    def get_object(self, pk):
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        blog = self.get_object(pk)
        serializer = BlogPostSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        blog = self.get_object(pk)
        serializer = BlogPostSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







