from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Paper, Subject, Category
from django.views.decorators.csrf import csrf_exempt

def main(request):
    most_voted_papers = Paper.objects.order_by('-score')[:10]
    return render(request, 'main.html', {'papers': most_voted_papers})

def fresh(request):
    fresh_papers = Paper.objects.order_by('-submitted')  # Order by most recent papers
    return render(request, 'fresh.html', {'papers': fresh_papers})

def paper(request):
    return render(request, 'paper.html')

def paper_detail(request, paper_id):
    paper = get_object_or_404(Paper, id=paper_id)
    return render(request, 'paper.html', {'paper': paper})

def search(request):
    return render(request, 'search.html')

def subject(request):
    subjects = Subject.objects.all()

    initial_subject = subjects.first() if subjects.exists() else None
    categories = Category.objects.filter(subject=initial_subject) if initial_subject else []

    return render(request, 'subject.html', {
        'subjects': subjects,
        'categories': categories
    })

@csrf_exempt
def increase_score(request, paper_id):
    if request.method == "POST":
        try:
            paper = Paper.objects.get(id=paper_id)
            paper.score += 1
            paper.save()
            return JsonResponse({'success': True, 'new_score': paper.score})
        except Paper.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Paper not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})

def fetch_papers(request):
    subject_name = request.GET.get('subject_name')
    category_name = request.GET.get('category_name')
    sort_by_votes = request.GET.get('sort_by_votes') == 'true'

    subject = Subject.objects.get(name=subject_name)
    papers = Paper.objects.filter(subject__subject=subject)

    if category_name != 'all':
        category = Category.objects.get(name=category_name)
        papers = papers.filter(subject=category)

    if sort_by_votes:
        papers = papers.order_by('-score')
    else:
        papers = papers.order_by('-submitted')

    papers_data = [{
        'id': paper.id,
        'title': paper.title,
        'abstract': paper.abstract,
        'score': paper.score,
        'url': paper.url
    } for paper in papers]

    print("PAPERS", len(papers_data))
    return JsonResponse({'papers': papers_data})

def fetch_categories(request):
    subject_name = request.GET.get('subject_name')

    subject = Subject.objects.get(name=subject_name)
    categories = Category.objects.filter(subject=subject)

    categories_data = [{'name': category.name} for category in categories]
    return JsonResponse({'categories': categories_data})

def search_papers(request):
    query = request.GET.get('query', '')
    if query:
        papers = Paper.objects.filter(title__icontains=query) | Paper.objects.filter(abstract__icontains=query)
    else:
        papers = Paper.objects.none()

    papers_data = [{
        'id': paper.id,
        'title': paper.title,
        'abstract': paper.abstract,
        'score': paper.score
    } for paper in papers]

    return JsonResponse({'papers': papers_data})