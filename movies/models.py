from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='movies/', null=True, blank=True)  # Le champ ImageField
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f'Review for {self.movie.title} by {self.reviewer_name}'
