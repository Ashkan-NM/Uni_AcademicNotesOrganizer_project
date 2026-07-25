from django.test import TestCase
from django.contrib.auth.models import User
from .models import Course, Note

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='123')
        self.course = Course.objects.create(user=self.user, title='ریاضی', description='درس ریاضی')
        self.note = Note.objects.create(course=self.course, title='جزوه 1', content='محتوا...')

    def test_course_creation(self):
        self.assertEqual(self.course.title, 'ریاضی')
        self.assertEqual(str(self.course), 'ریاضی')

    def test_note_creation(self):
        self.assertEqual(self.note.title, 'جزوه 1')
        self.assertEqual(str(self.note), 'جزوه 1')