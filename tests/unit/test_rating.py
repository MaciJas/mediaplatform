from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from myapp.models import Channel, Content


class CommandTestCase(TestCase):
    def setUp(self):
        self.channel1 = Channel.objects.create(title='Channel 1')
        self.channel2 = Channel.objects.create(title='Channel 2')
        self.subchannel1 = Channel.objects.create(title='Subchannel 1', parent=self.channel1)
        self.subchannel2 = Channel.objects.create(title='Subchannel 2', parent=self.channel1)
        self.content1 = Content.objects.create(title='Content 1', channel=self.channel1, rating=3.0)
        self.content2 = Content.objects.create(title='Content 2', channel=self.channel1, rating=4.5)

    def test_compute_ratings(self):
        out = StringIO()
        call_command('compute_ratings', stdout=out)

        # Check that ratings were computed correctly
        self.channel1.refresh_from_db()
        self.channel2.refresh_from_db()
        self.subchannel1.refresh_from_db()
        self.subchannel2.refresh_from_db()

        self.assertEqual(self.channel1.rating, 3.75)
        self.assertEqual(self.channel2.rating, None)
        self.assertEqual(self.subchannel1.rating, None)
        self.assertEqual(self.subchannel2.rating, None)

        expected_output = 'Channel Title,Average Rating\n' \
                          'Channel 1,3.75\n' \
                          'Channel 2,None\n' \
                          'Subchannel 1,None\n' \
                          'Subchannel 2,None\n'
        self.assertEqual(out.getvalue(), expected_output)
