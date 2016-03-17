from django.shortcuts import render
from django.http import HttpResponse
from Rango.models import Category, Page
from Rango.forms import CategoryForm, PageForm

# Create your views here.


#def index(request):
# Construct a dictionary to pass the template engine as its context.
#	context_dict = {'boldmessage': "I am the bold font that knocks..."}
#	return render(request, 'Rango/index.html', context_dict)

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    most_viewed_pages = Page.objects.order_by('-view')[:5]
    context_dict = {'categories': category_list, 'pages': most_viewed_pages}

    # Render the response and send it back!
    return render(request, 'Rango/index.html', context_dict)
	
def secret(request):
	return HttpResponse("<h3>Borko says \"Down with Django!\"</h3>" + "<br>" + "<h1>PHP for life!!!</h1>")

	
def about(request):
	return HttpResponse("If you want to know more about why we are studying Django, ask <a href='mailto:Leif.Azzopardi@glasgow.ac.uk?Subject=WAD2%20question&cc=2140786g@student.gla.ac.uk'>Leifos</a> please." + "<br>" + "Or you could look for some hidden pages..." + "<br>" + "<img src='/static/images/beMine.jpg' height=60% width=60%>")

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'Rango/add_page.html', context_dict)
	
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'Rango/add_category.html', {'form': form})	

def static(request):
	return HttpResponse("<img src=\"/static/images/beMine.jpg\">")
	
def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)
