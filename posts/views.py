
from rest_framework.response import Response
from rest_framework import status
from users.serializers import CurrentUserPostsSerializer
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.request import Request
from . models import Post
from .serializers import PostSerializer
from .permissions import ReadOnly, AuthorOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

from rest_framework.pagination import PageNumberPagination

class CustomPaginator(PageNumberPagination):
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "page_size"

@api_view(["GET"])
@permission_classes([AllowAny])
def homepage(request: Request) -> Response:
    """
    This function serves as the homepage endpoint for the application.
    It responds to GET requests and returns a welcome message along with a status code.

    Parameters:
    request (Request): The incoming request object containing information about the request.

    Returns:
    Response: A response object containing the welcome message and a status code of 200 (HTTP_200_OK).
    """
    if request.method == "GET":
        return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)
    

class PostListCreateView(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPaginator

    def get(self, request):
        """
        This function handles GET requests to retrieve a list of all posts.

        Parameters:
        request (Request): The incoming request object containing information about the request.

        Returns:
        Response: A response object containing a list of serialized post data and a status code of 200 (HTTP_200_OK).
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        This function handles POST requests to create a new post.

        Parameters:
        request (Request): The incoming request object containing information about the request.

        Returns:
        Response: A response object containing the serialized post data and a status code of 201 (HTTP_201_CREATED) if the post is successfully created.
        If the post data is not valid, a response object containing the validation errors and a status code of 400 (HTTP_400_BAD_REQUEST) is returned.
        """
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetriveUpdateDeleteView(APIView):
    serializer_class = PostSerializer
    permission_classes = [AuthorOrReadOnly]

    def get(self, request:Request, post_id):
        """
        This function handles GET requests to retrieve a single post by its ID.

        Parameters:
        request (Request): The incoming request object containing information about the request.
        post_id (int): The ID of the post to retrieve.

        Returns:
        Response: A response object containing the serialized post data and a status code of 200 (HTTP_200_OK) if the post is found.
        If the post is not found, a response object containing a message and a status code of 404 (HTTP_404_NOT_FOUND) is returned.
        """
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostSerializer(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, post_id):
        """
    This function handles PUT requests to update an existing post by its ID.

    Parameters:
    request (Request): The incoming request object containing information about the request.
    post_id (int): The ID of the post to update.

    Returns:
    Response: A response object containing the updated serialized post data and a status code of 200 (HTTP_200_OK) if the post is found and updated successfully.
    If the post is not found, a response object containing a message and a status code of 404 (HTTP_404_NOT_FOUND) is returned.
    If the post data is not valid, a response object containing the validation errors and a status code of 400 (HTTP_400_BAD_REQUEST) is returned.
    """
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        """
        This function handles DELETE requests to delete an existing post by its ID.

        Parameters:
        request (Request): The incoming request object containing information about the request.
        post_id (int): The ID of the post to delete.

        Returns:
        Response: A response object containing a message and a status code of 204 (HTTP_204_NO_CONTENT) if the post is found and deleted successfully.
        If the post is not found, a response object containing a message and a status code of 404 (HTTP_404_NOT_FOUND) is returned.
        """
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        return Response(data={"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request: Request) -> Response:
    """
    This function retrieves a list of posts created by the currently authenticated user.

    Parameters:
    request (Request): The incoming request object containing information about the request.
        It is assumed that the request has been authenticated and the user is authorized to access this endpoint.

    Returns:
    Response: A response object containing the serialized data of the posts created by the current user.
        The response has a status code of 200 (HTTP_200_OK) if the operation is successful.
        The serialized data includes information about each post, such as its ID, title, content, and creation date.
    """
    user = request.user

    serializer = CurrentUserPostsSerializer(instance=user, context={"request": request})

    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_posts_for_author(request):
    """
    Handles GET requests to retrieve a list of posts by a specific author.

    Parameters:
    request (Request): The incoming request object containing information about the request.

    Returns:
    Response: A response object containing a list of serialized post data and a status code of 200 (HTTP_200_OK).
    """
    username = request.query_params.get("username", None)

    if username:
        # Filter posts by author username
        posts = Post.objects.filter(author__username=username)
    else:
        # Retrieve all posts if no username is provided
        posts = Post.objects.all()

    # Serialize the queryset
    serializer = PostSerializer(posts, many=True)

    # Return the serialized data in the response
    return Response(data=serializer.data, status=status.HTTP_200_OK)