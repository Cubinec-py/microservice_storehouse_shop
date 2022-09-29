from django.db import models
from django.shortcuts import reverse
from django.utils import timezone


class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s %s' % (self.first_name, self.last_name)


class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    description = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined, so we can specify the object above.
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(blank=True, default=False, null=True)
    pages = models.IntegerField()
    created = models.DateField(default=timezone.now, null=True, blank=True)
    count = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    storehouse_book_id = models.CharField(max_length=50, null=True, help_text='Book id from storehouse')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def status_book(self):
        if self.count < 1:
            return self.available is False
        else:
            return self.available is True

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.id)])