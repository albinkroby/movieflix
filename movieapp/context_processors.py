from .models import MovieCategory

def categories(request):
    categories = MovieCategory.objects.all()
    return {'categories': categories}
