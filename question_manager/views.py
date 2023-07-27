from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from .models import User, Question, FavoriteQuestion, ReadQuestion
from .serializers import UserSerializer, QuestionSerializer, FavoriteQuestionSerializer, ReadQuestionSerializer
from django.views.decorators.cache import cache_page



# View to insert data for FavoriteQuestion
@api_view(['POST'])
def add_favorite_question(request):
    user_id = request.data.get('user_id')
    question_id = request.data.get('question_id')

    try:
        user = User.objects.get(id=user_id)
        question = Question.objects.get(id=question_id)

        favorite_question = FavoriteQuestion(user_id=user, question_id=question)
        favorite_question.save()

        return Response({'message': 'Favorite question added successfully.'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User with the given ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except Question.DoesNotExist:
        return Response({'error': 'Question with the given ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to insert data for ReadQuestion
@api_view(['POST'])
def add_read_question(request):
    user_id = request.data.get('user_id')
    question_id = request.data.get('question_id')

    try:
        user = User.objects.get(id=user_id)
        question = Question.objects.get(id=question_id)

        read_question = ReadQuestion(user_id=user, question_id=question)
        read_question.save()

        return Response({'message': 'Read question added successfully.'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User with the given ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except Question.DoesNotExist:
        return Response({'error': 'Question with the given ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# View to retrieve data for FavoriteQuestion
@api_view(['GET'])
def get_favorite_questions(request):
    favorite_questions = FavoriteQuestion.objects.all().select_related('user_id', 'question_id')
    serializer = FavoriteQuestionSerializer(favorite_questions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# View to retrieve data for ReadQuestion
@api_view(['GET'])
def get_read_questions(request):
    read_questions = ReadQuestion.objects.all().select_related('user_id', 'question_id')
    serializer = ReadQuestionSerializer(read_questions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# View to count total favorite questions per user (paginated to 100 users per page)
@api_view(['GET'])
@cache_page(60 * 5)  # Cache the response for 5 minutes
def count_favorite_questions_per_user(request):
    users = User.objects.all()
    paginator = Paginator(users, 100)  # 100 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    favorite_counts = []
    for user in page_obj:
        count = FavoriteQuestion.objects.filter(user_id=user).count()
        favorite_counts.append({'user_id': user.id, 'user_count': count})

    return Response(favorite_counts, status=status.HTTP_200_OK)

# View to count total read questions per user (paginated to 100 users per page)
@api_view(['GET'])
@cache_page(60 * 5)  # Cache the response for 5 minutes
def count_read_questions_per_user(request):
    users = User.objects.all()
    paginator = Paginator(users, 100)  # 100 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    read_counts = []
    for user in page_obj:
        count = ReadQuestion.objects.filter(user_id=user).count()
        read_counts.append({'user_id': user.id, 'user_count': count})

    return Response(read_counts, status=status.HTTP_200_OK)

# View to filter questions by read, unread, favorite, and unfavorite status
@api_view(['GET'])
@cache_page(60 * 5)  # Cache the response for 5 minutes
def filter_questions(request):
    status_filter = request.GET.get('status', '').lower()

    if status_filter == 'read':
        questions = ReadQuestion.objects.all()
        serializer = ReadQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif status_filter == 'unread':
        questions = Question.objects.exclude(id__in=ReadQuestion.objects.values('question_id'))
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif status_filter == 'favorite':
        questions = FavoriteQuestion.objects.all()
        serializer = FavoriteQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif status_filter == 'unfavorite':
        questions = Question.objects.exclude(id__in=FavoriteQuestion.objects.values('question_id'))
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid status filter provided.'}, status=status.HTTP_400_BAD_REQUEST)