from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User

from .models import Meeting


class MeetingPermissionTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pw12345!')
        self.bob = User.objects.create_user(username='bob', password='pw12345!')
        now = timezone.now()
        self.meeting = Meeting.objects.create(
            title='Sync', start=now, end=now + timezone.timedelta(hours=1), created_by=self.alice
        )

    def test_creator_can_edit(self):
        self.assertTrue(self.meeting.can_edit(self.alice))

    def test_other_user_cannot_edit(self):
        self.assertFalse(self.meeting.can_edit(self.bob))

    def test_admin_can_edit_any_meeting(self):
        self.bob.is_staff = True
        self.bob.save()
        self.assertTrue(self.meeting.can_edit(self.bob))

    def test_non_creator_gets_403_on_edit_view(self):
        self.client.login(username='bob', password='pw12345!')
        response = self.client.get(reverse('meeting_edit', args=[self.meeting.pk]))
        self.assertEqual(response.status_code, 403)
