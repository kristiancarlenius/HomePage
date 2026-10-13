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


class MeetingTimeFormatTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pw12345!')
        self.client.login(username='alice', password='pw12345!')

    def test_create_meeting_with_24h_time(self):
        response = self.client.post(reverse('meeting_create'), {
            'title': 'Late sync',
            'start_0': '2026-10-13', 'start_1': '21:30',
            'end_0': '2026-10-13', 'end_1': '23:59',
        })
        self.assertRedirects(response, reverse('calendar'))
        meeting = Meeting.objects.get(title='Late sync')
        self.assertEqual(timezone.localtime(meeting.start).strftime('%H:%M'), '21:30')

    def test_edit_form_shows_24h_time(self):
        start = timezone.make_aware(timezone.datetime(2026, 10, 13, 15, 0))
        meeting = Meeting.objects.create(
            title='Afternoon', start=start, end=start + timezone.timedelta(hours=1), created_by=self.alice
        )
        response = self.client.get(reverse('meeting_edit', args=[meeting.pk]))
        self.assertContains(response, 'value="15:00"')
        self.assertNotContains(response, 'p.m.')

    def test_datetime_filter_renders_24h(self):
        from django.template import Context, Template
        dt = timezone.make_aware(timezone.datetime(2026, 10, 13, 18, 5))
        out = Template('{{ dt }}|{{ dt|time }}').render(Context({'dt': dt}))
        self.assertEqual(out, '2026-10-13 18:05|18:05')
