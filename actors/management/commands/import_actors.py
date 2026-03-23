import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from actors.models import Actor


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--filename',
            type=str,
            help='The name of the file to import actors from'
        )

    def handle(self, *args, **options):
        filename = options['filename']
        self.stdout.write(f'Importing actors from {filename}')

        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                birthday = datetime.strptime(row['birthday'], '%Y-%m-%d').date()
                nationality = row['nationality']

                try:
                    self.stdout.write(self.style.NOTICE(f'Importing actor: {name}'))
                    Actor.objects.create(
                        name=name,
                        birthday=birthday,
                        nationality=nationality
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to import actor {name}: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully imported actors'))
