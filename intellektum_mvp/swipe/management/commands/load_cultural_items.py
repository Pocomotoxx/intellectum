from django.core.management.base import BaseCommand
from swipe.models import CulturalItem

class Command(BaseCommand):
    help = 'Loads initial cultural items into the database'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing cultural items...')
        CulturalItem.objects.all().delete()

        items_data = [
            {'title': 'The Great Gatsby', 'item_type': 'BOOK', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/The_Great_Gatsby_Cover_1925_Retouched.jpg/330px-The_Great_Gatsby_Cover_1925_Retouched.jpg', 'tags': 'classic,novel,american literature'},
            {'title': 'To Kill a Mockingbird', 'item_type': 'BOOK', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg/330px-To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg', 'tags': 'classic,novel,southern gothic'},
            {'title': 'Inception', 'item_type': 'MOVIE', 'image_url': 'https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg', 'tags': 'sci-fi,thriller,action'},
            {'title': 'The Shawshank Redemption', 'item_type': 'MOVIE', 'image_url': 'https://upload.wikimedia.org/wikipedia/en/8/81/ShawshankRedemptionMoviePoster.jpg', 'tags': 'drama,crime'},
            {'title': 'Starry Night', 'item_type': 'PAINTING', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/600px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg', 'tags': 'post-impressionism,van gogh,art'},
            {'title': 'Mona Lisa', 'item_type': 'PAINTING', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg/402px-Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg', 'tags': 'renaissance,da vinci,portrait'},
            {'title': 'Queen (band)', 'item_type': 'MUSICIAN', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/QueenPerforming1977.jpg/330px-QueenPerforming1977.jpg', 'tags': 'rock,band,british'},
            {'title': 'Miles Davis', 'item_type': 'MUSICIAN', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Miles_Davis_by_Palumbo.jpg/330px-Miles_Davis_by_Palumbo.jpg', 'tags': 'jazz,trumpet,composer'},
            {'title': 'The Matrix', 'item_type': 'MOVIE', 'image_url': 'https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg', 'tags': 'sci-fi,action,cyberpunk'},
            {'title': 'Pride and Prejudice', 'item_type': 'BOOK', 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/PrideAndPrejudiceTitlePage.jpg/330px-PrideAndPrejudiceTitlePage.jpg', 'tags': 'classic,romance,novel'},
        ]

        self.stdout.write(f'Loading {len(items_data)} cultural items...')
        for item_data in items_data:
            CulturalItem.objects.create(**item_data)

        self.stdout.write(self.style.SUCCESS('Successfully loaded cultural items.'))
