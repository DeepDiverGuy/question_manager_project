from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import User, Question, FavoriteQuestion, ReadQuestion



class ApiViewsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(idname='user1', display_name='User One', email='user1@example.com', phone='1234567890')
        self.user2 = User.objects.create(idname='user2', display_name='User Two', email='user2@example.com', phone='9876543210')

        self.question1 = Question.objects.create(question='Question 1', option1='Option A', option2='Option B', option3='Option C', option4='Option D', option5='Option E', answer=1, explain='Explanation 1')
        self.question2 = Question.objects.create(question='Question 2', option1='Option A', option2='Option B', option3='Option C', option4='Option D', option5='Option E', answer=2, explain='Explanation 2')

        self.favorite1 = FavoriteQuestion.objects.create(user_id=self.user1, question_id=self.question1)
        self.favorite2 = FavoriteQuestion.objects.create(user_id=self.user1, question_id=self.question2)

        self.read1 = ReadQuestion.objects.create(user_id=self.user1, question_id=self.question1)
        self.read2 = ReadQuestion.objects.create(user_id=self.user1, question_id=self.question1)

    def test_add_favorite_question(self):
        url = reverse('add_favorite_question')
        data = {'user_id': self.user2.id, 'question_id': self.question2.id}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FavoriteQuestion.objects.filter(user_id=self.user2.id).count(), 1)

    def test_add_read_question(self):
        url = reverse('add_read_question')
        data = {'user_id': self.user2.id, 'question_id': self.question2.id}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReadQuestion.objects.filter(user_id=self.user2.id).count(), 1)

    def test_count_favorite_questions_per_user(self):
        url = reverse('count_favorite_questions_per_user')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_count_read_questions_per_user(self):
        url = reverse('count_read_questions_per_user')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_favorite_questions(self):
        url = reverse('get_favorite_questions')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_read_questions(self):
        url = reverse('get_read_questions')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_questions_by_read_status(self):
        url = reverse('filter_questions') + "?status=read"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_questions_by_unread_status(self):
        url = reverse('filter_questions') + "?status=unread"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_questions_by_favorite_status(self):
        url = reverse('filter_questions') + "?status=favorite"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_questions_by_unfavorite_status(self):
        url = reverse('filter_questions') + "?status=unfavorite"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

