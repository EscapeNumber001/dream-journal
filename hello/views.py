import json
import django.utils.timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, models
from django.core.paginator import Paginator
from django.core.files import File

from .forms import AddOrEditEntryForm, EntrySearchForm, SORTING_METHODS
from .models import Entry
from mysite import settings

from markdownify import markdownify as mdf
import markdown
import bleach

# Helper functions
def _verify_entry_user(request, e):
    return e.owner == request.user


def _perform_entry_addoredit(request, form, entry_pk=-1):
    if entry_pk != -1:
        e = get_object_or_404(Entry, pk=entry_pk)
    else:
        e = Entry()
    is_new_entry = entry_pk == -1

    e.entry_title = form.cleaned_data["entry_title"]
    e.is_secret = form.cleaned_data["is_secret"]
    e.entry_text = markdown.markdown(
        bleach.clean(
            form.cleaned_data["entry_text"]
        )
    )
    e.entry_text_wordcount = _count_words(e.entry_text)
    e.creation_datetime = form.cleaned_data["creation_datetime"]
    if not is_new_entry:
        e.last_edit_datetime = django.utils.timezone.now()
    e.owner = request.user
    e.save()
    return e.pk


# BUG: This function doesn't count words immediately after a newline.
# Not a very important issue right now since this only causes a loss of
# one word per newline.
def _count_words(text: str) -> int:
    return len(text.split(" "))


# Views
def home(request):
    return render(request, "index.html")


@login_required
def entry_list(request):
    sort_by = "creation_datetime"
    page_num = 1
    search_query = ""

    if "page_num" in request.GET and request.GET["page_num"] != "":
        page_num = request.GET["page_num"]

    search_form = EntrySearchForm(request.GET)

    if search_form.is_valid():
        search_query = search_form.cleaned_data["query_text"]
        sort_dir = "" if search_form.cleaned_data["sort_dir"] == "asc" else "-"

        # Although we're accessing the field names directly, this should be safe because
        # it is restricted to only the fields in the SORTING_METHODS dict in forms.py.
        if search_form.cleaned_data["sort_by"] != "":
            sort_by = sort_dir + search_form.cleaned_data["sort_by"]
        else:
            sort_by = sort_dir + "creation_datetime"

    all_entries = Entry.objects.filter(owner__exact=request.user)\
        .filter(entry_text__icontains=search_query)\
        .order_by(sort_by)
    secret_entries_enabled = request.session.get('secretentries', False)
    if not secret_entries_enabled:
        all_entries = all_entries.filter(is_secret__exact=False)
    p = Paginator(all_entries, 10)
    page_obj = p.get_page(page_num)

    return render(request, "entry_list.html", {'all_entries': p.page(page_num), 'page_obj': page_obj, 'search_form': search_form} )


@login_required
def detail(request, req_pk):
    entry = get_object_or_404(klass=Entry, pk=req_pk)
    if not _verify_entry_user(request, entry):
        return HttpResponse("You are forbidden from viewing this page.", status=403)

    return render(
        request=request, 
        template_name="entry_detail.html", 
        context={
            'entry': entry,
            'timezone': settings.TIME_ZONE
        }
    )


@login_required
def entry_add(request):
    if request.method == "POST":
        form = AddOrEditEntryForm(request.POST)
        if form.is_valid():
            pk = _perform_entry_addoredit(request, form)
            return HttpResponseRedirect(f"/entry/{pk}")
    else:
        form = AddOrEditEntryForm(initial={"creation_datetime": django.utils.timezone.now()})
            
    return render(request=request, template_name="entry_add.html", context={"form": form})


@login_required
@require_POST
def entry_delete(request, req_pk):
    entry = get_object_or_404(klass=Entry, pk=req_pk)
    if not _verify_entry_user(request, entry):
        return HttpResponse("You are forbidden from deleting this post.", status=403)
    
    entry.delete()
    return HttpResponseRedirect("/")


@login_required
def entry_edit(request, req_pk):
    entry = get_object_or_404(Entry, pk=req_pk)
    if not _verify_entry_user(request, entry):
        return HttpResponse("You are forbidden from viewing this page.", status=403)

    if request.method == "POST":
        form = AddOrEditEntryForm(request.POST)
        if form.is_valid():
            pk = _perform_entry_addoredit(request, form, req_pk)
            return HttpResponseRedirect(f"/entry/{pk}")
    else:
        form = AddOrEditEntryForm(
            instance=entry, 
            initial={
                "entry_text": mdf(entry.entry_text)
                }
            )
    return render(request=request, template_name="entry_edit.html", context={'pk': req_pk, 'form': form})


def login_page(request):
    return render(request, "login.html")


def handle_login(request):
    username = request.POST["username_input"]
    password = request.POST["password_input"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")


@login_required
def logout_page(request):
    logout(request)
    return render(request, "logout.html")


@login_required
def settings_page(request):
    return render(request, "settings.html")


@login_required
def applysettings(request):
    secret_sessionvar = None

    enablesecretspassword=request.POST["enablesecretspassword"]
    if ("secretentries" in request.POST):
        test = authenticate(request, username=request.user.username, password=enablesecretspassword)
        if test is not None:
            secret_sessionvar = request.POST["secretentries"]

    request.session["secretentries"] = "true" if secret_sessionvar else None

    if len(request.FILES) > 0:
        data = ""
        for filename in request.FILES:
            f = request.FILES[filename]
            print("Received file " + f.name)
            data = f.read()

        try:
            myjs = json.loads(data)
            for key in myjs:
                e = Entry()
                entrydata = myjs[key]

                e.creation_datetime = entrydata["creation_datetime"]
                e.last_edit_datetime = entrydata["last_edit_datetime"] if entrydata["last_edit_datetime"] != "None" else None
                e.entry_title = entrydata["entry_title"]
                e.entry_text = entrydata["entry_text"]
                e.is_secret = entrydata["is_secret"]
                e.owner = request.user
                e.save()
        except json.JSONDecodeError as e:
            return render(request, "error.html", {'errortext': f"Import failed due to invalid JSON file: {str(e)}", 'nextpage': "/settings"}, status=400)
        except (TypeError, KeyError) as e:
            return render(request, "error.html", {'errortext': "JSON file does not appear to be a journal export.", 'nextpage': '/settings'}, status=400)

    return HttpResponseRedirect("/")


def signup_page(request):
    return render(request, "signup_page.html")


def finishsignup(request):
    username = request.POST["username"]
    password = request.POST["password"]
    if len(models.User.objects.filter(username__exact=username)) > 0:
        return HttpResponse("That username is already taken.")

    models.User.objects.create_user(username=username, email=None, password=password)
    new_user = authenticate(request, username=username, password=password)
    if not new_user:
        return render(request, "error.html", {'errortext': '500 Internal Server Error: Something went wrong when creating the account.', 'nextpage': '/login'}, status=500)
    login(request, new_user)
    return HttpResponseRedirect("/")


def dataexport(request):
    all_entries = Entry.objects.all().filter(owner__exact=request.user).order_by("creation_datetime")

    response = HttpResponse(content_type='text/json')
    response['Content-Disposition'] = 'attachment; filename="entries.json"'

    root = {}
    outstr = ""

    for entry in all_entries:
        root[entry.pk] = dict()
        entry_js = root[entry.pk]
        entry_js["creation_datetime"] = str(entry.creation_datetime)
        entry_js["last_edit_datetime"] = str(entry.last_edit_datetime)
        entry_js["entry_title"] = entry.entry_title
        entry_js["entry_text"] = entry.entry_text
        entry_js["is_secret"] = entry.is_secret
    
    outstr = json.dumps(root)
    response.content = outstr
    
    return response