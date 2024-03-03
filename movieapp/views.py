from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages,auth
from .forms import RegistrationForm,UserProfileForm,MovieForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import MovieCategory, Movie, Review
from django.db.models import Avg


# Create your views here.


def index(request):
    movies = Movie.objects.all()
    latest_movies = Movie.objects.order_by('-release_date')[:3]
    return render(request, 'index.html', {'movies': movies, 'latest_movies': latest_movies})

def products_by_category(request, category_slug):
    category = get_object_or_404(MovieCategory, slug=category_slug)
    movies = Movie.objects.filter(category=category)
    return render(request, 'products_by_category.html', {'category': category, 'movies': movies})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                new_user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )

                messages.success(request, f'Account created for {new_user.username}!')
                return redirect('login')
            else:
                messages.error(request, 'Password and Confirm Password do not match.')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
        else:
            messages.error(
                request, 'Invalid login credentials. Please try again.')
        storage = messages.get_messages(request)
        storage.used = True

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('index')



def profile(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
            else:
                messages.error(request, 'There was an error updating your profile.')
        else:
            form = UserProfileForm(instance=user)

        return render(request, 'profile.html', {'user': user, 'form': form})
    else:
        return redirect('login')
    
def profile_edit(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('view_profile')
            else:
                form = UserProfileForm(instance=user)

        return render(request, 'Edit.html', {'user': user , 'form': form})
    else:
        return redirect('login')


def add_movie(request):
    user = request.user

    if user.is_authenticated:
        if request.method == 'POST':
            form = MovieForm(request.POST, request.FILES)
            if form.is_valid():
                movie = form.save(commit=False)

                category_id = form.cleaned_data['category'].id
                try:
                    movie.category = MovieCategory.objects.get(pk=category_id)
                except MovieCategory.DoesNotExist:
                    return render(request, 'add_movie.html', {'form': form, 'error_message': 'Invalid category'})

                movie.added_by = user
                movie.save()
                return redirect('index')
        else:
            form = MovieForm()

        return render(request, 'add_movie.html', {'form': form})

    else:
        return redirect('login')
    
def my_movies(request):
    if request.user.is_authenticated:
        movies = Movie.objects.filter(added_by=request.user)
        return render(request, 'mymovies.html', {'movies': movies})
    else:
        return redirect('login')

def edit_my_movie(request, slug):
    user = request.user
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, slug=slug, added_by=request.user)

        if request.method == 'POST':
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('mymovies')
        else:
            form = MovieForm(instance=movie)

        return render(request, 'updatemovie.html', {'form': form, 'movie': movie})
    else:
        return redirect('login')

def delete_my_movie(request, slug):
    user = request.user
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, slug=slug, added_by=request.user)
        movie.delete()
        return redirect('mymovies')
    else:
        return redirect('login')

def movie_detail(request, slug):
    if request.user.is_authenticated:
        user = request.user  
    else:
        user = None
    movie = get_object_or_404(Movie, slug=slug)
    reviews = Review.objects.filter(movie=movie)
    total_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if user:
        reviews = reviews.exclude(user=user)
    userreviews = Review.objects.filter(movie=movie, user=user).select_related('user')
    
      
    return render(request, 'moviedetails.html', {
    'movie': movie,
    'reviews': reviews,
    'userreviews': userreviews if userreviews else None,
    'total_rating': total_rating,
    'user': user
    })

def add_review(request, slug):
    if request.method == 'POST' and request.user.is_authenticated:
        movie = get_object_or_404(Movie, slug=slug)
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')

        if review_text and rating:
            Review.objects.create(user=request.user, movie=movie, text=review_text, rating=rating)
            # messages.success(request, 'Review added successfully.')
        else:
            # messages.error(request, 'Please provide both review text and rating.')
            pass

    return redirect('movie_detail', slug=slug)

def edit_review(request, slug):
    if request.method == 'POST' and request.user.is_authenticated:
        movie = get_object_or_404(Movie, slug=slug)
        review_text = request.POST.get('updatereview_text')
        rating = request.POST.get('updaterating')

        # Check if the user has already reviewed the movie
        existing_review = Review.objects.filter(user=request.user, movie=movie).first()

        if existing_review:
            existing_review.text = review_text
            existing_review.rating = rating
            existing_review.save()

    return redirect('movie_detail', slug=slug)



def delete_review(request, slug, review_id):
    movie = get_object_or_404(Movie, slug=slug)
    review = get_object_or_404(Review, id=review_id, user=request.user)

    review.delete()
    return redirect('movie_detail', slug=slug)


def search_movies(request):
    query=None
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    if query:
        category = MovieCategory.objects.filter(name=query).first()
        if category:
            movies = movies.filter(category=category)
    else:
        movies = Movie.objects.all()

    return render(request, 'search_results.html', {'movies': movies,'query':query})