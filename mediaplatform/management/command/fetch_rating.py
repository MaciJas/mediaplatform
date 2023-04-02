from django.core.management.base import BaseCommand
from myapp.models import Channel, Content


class Command(BaseCommand):
    help: str = 'Computes the ratings for all channels'

    def handle(self, *args: str, **options: str) -> None:
        channels = Channel.objects.all()

        for channel in channels:
            if channel.subchannels.exists():
                subchannel_ratings = [subchannel.rating() for subchannel in channel.subchannels.all()]
                if subchannel_ratings:
                    channel.rating = sum(subchannel_ratings) / len(subchannel_ratings)
            else:
                content_ratings = [content.rating for content in channel.contents.all()]
                if content_ratings:
                    channel.rating = sum(content_ratings) / len(content_ratings)
            channel.save()

        with open('channel_ratings.csv', 'w') as f:
            f.write('Channel Title,Average Rating\n')
            for channel in Channel.objects.order_by('-rating'):
                f.write(f'{channel.title},{channel.rating}\n')