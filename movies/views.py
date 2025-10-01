from django.shortcuts import render,get_object_or_404, redirect
from .models import Movie, Genre
from .models import Movie, Review
from django.db.models import Avg
from .forms import MovieForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'movies/home.html')
@login_required
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie)
    
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    review_star_ratings = [
        {"review": review, "stars": "★" * review.rating + "☆" * (5 - review.rating)}
        for review in reviews
    ]
    
    if request.method == 'POST':
        reviewer_name = request.POST['reviewer_name']
        rating = int(request.POST['rating'])
        comment = request.POST['comment']
        
        Review.objects.create(
            movie=movie,
            reviewer_name=reviewer_name,
            rating=rating,
            comment=comment
        )
        
        return redirect('movie_detail', movie_id=movie.id)
    
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'review_star_ratings': review_star_ratings,
    })



def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)

        if form.is_valid():
            movie = form.save(commit=False)

            new_genre_name = request.POST.get('new_genre')
            if new_genre_name:
                genre, created = Genre.objects.get_or_create(name=new_genre_name)
                movie.genre = genre

            movie.save()
            return redirect('movie_list')
    else:
        form = MovieForm()

    return render(request, 'movies/add_movie.html', {'form': form})



def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save(commit=False)

            new_genre_name = request.POST.get('new_genre')
            if new_genre_name:
                genre, created = Genre.objects.get_or_create(name=new_genre_name)
                movie.genre = genre

            movie.save()
            return redirect('movie_list')  
    else:
        form = MovieForm(instance=movie)
        
    return render(request, 'movies/edit_movie.html', {'form': form, 'movie': movie})

from django.shortcuts import get_object_or_404

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list') 
    return render(request, 'movies/delete_movie.html', {'movie': movie})

from .forms import ReviewForm


def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', movie_id=review.movie.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'movies/edit_review.html', {'form': form, 'review': review})
from django.http import JsonResponse

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        review.delete()
        return redirect('movie_detail', movie_id=review.movie.id)

    return render(request, 'movies/delete_review.html', {'review': review})




from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm


def register(request):
    if request.user.is_authenticated:
        return render(request, "movies/register.html", {"message": "You are already logged in. Please log out to register a new account."})
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)

            login(request, user)

            return redirect("movies:home")
    else:
        form = RegistrationForm()

    return render(request, "movies/register.html", {"form": form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'movies/login.html', {"error": "Identifiant ou mot de passe invalide."})

    return render(request, 'movies/login.html')

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("movies:login") 
    else:
        return redirect("movies:login")
