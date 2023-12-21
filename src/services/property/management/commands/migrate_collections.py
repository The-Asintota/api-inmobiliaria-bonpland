from typing import List
from django.core.management.base import BaseCommand
from services.property.models.mongo_db import MongoModel
import services.property.models as models
import inspect


class Command(BaseCommand):
    """
    A Django management command that `migrates collections`.
    
    This command finds all subclasses of `MongoModel` in the `models` module, creates a collection for each one, and prints a success message.
    """
    
    help = 'Migrate collections.'
    
    def find_subclasses(self) -> List:
        """
        Find all subclasses of MongoModel in the models module.
        """
        
        subclasses = []
        for _, obj in inspect.getmembers(models):
            if inspect.isclass(obj) and issubclass(obj, MongoModel):
                subclasses.append(obj)
        return subclasses
    
    def handle(self, *args, **options) -> None:
        """
        Manage the command.

        This method finds all subclasses of MongoModel and performs the `migrations` to a `MongoDB database`.
        """
        
        subclasses = self.find_subclasses()
        subclasses_list = '\n   - '.join(
            [subclass.__name__ for subclass in subclasses]
        )
        self.stdout.write(
            self.style.WARNING(
                f'Collections found:\n  - {subclasses_list}'
            )
        )
        for subclass in subclasses:
            if issubclass(subclass, MongoModel) and subclass != MongoModel:
                subclass.create_collection()

        self.stdout.write(
            self.style.SUCCESS(
                'Collections successfully migrated.'
            )
        )