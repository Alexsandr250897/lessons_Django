from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpRequest
from django.core.handlers.wsgi import WSGIRequest

from .models import Note, User
from .servis import create_note, filter_notes, queryset_optimization


def home_page_views(request: HttpRequest):
    """
    Обязательно! Каждая функция view должна принимать первым параметром request.
    """

    queryset = queryset_optimization(Note.objects.all())

    print(queryset.query)

    return render(request, "home.html", {"notes": queryset[:100]})


def filter_notes_views(request: WSGIRequest):
    """
    Фильтруем записи по запросу пользователя.
    HTTP метод - GET.
    Обрабатывает URL вида: /filter/?search=<text>
    """

    search: str = request.GET.get("search", "")  # `get` - получение по ключу. Если такого нет, то - "",
    queryset = queryset_optimization(
        filter_notes(search)
    )

    context: dict = {
        "notes": queryset[:100],
        "search_value_form": search,
    }
    return render(request, "home.html", context)


@login_required
def create_note_views(request: WSGIRequest):
    if request.method == "POST":
        note = create_note(request)
        return HttpResponseRedirect(reverse('show-note', args=[note.uuid]))

    # Вернется только, если метод не POST.
    return render(request, "create_form.html")


def show_note_views(request: WSGIRequest, note_uuid):
    try:
        note = Note.objects.get(uuid=note_uuid)  # Получение сразу только ОДНОЙ записи.

    except Note.DoesNotExist:
        # Если не найдено такой записи.
        raise Http404

    return render(request, "note.html", {"note": note})


def delete_note_views(request: WSGIRequest, note_uuid: str):
    if request.method == "POST":
        Note.objects.filter(uuid=note_uuid).delete()
    return HttpResponseRedirect(reverse("home"))


def register(request: WSGIRequest):
    if request.method != "POST":
        return render(request, "registration/register.html")
    print(request.POST)
    if not request.POST.get("username") or not request.POST.get("email") or not request.POST.get("password1"):
        return render(
            request,
            "registration/register.html",
            {"errors": "Укажите все поля!"}
        )
    print(User.objects.filter(
            Q(username=request.POST["username"]) | Q(email=request.POST["email"])
    ))
    # Если уже есть такой пользователь с username или email.
    if User.objects.filter(
            Q(username=request.POST["username"]) | Q(email=request.POST["email"])
    ).count() > 0:
        return render(
            request,
            "registration/register.html",
            {"errors": "Если уже есть такой пользователь с username или email"}
        )

    # Сравниваем два пароля!
    if request.POST.get("password1") != request.POST.get("password2"):
        return render(
            request,
            "registration/register.html",
            {"errors": "Пароли не совпадают"}
        )

    # Создадим учетную запись пользователя.
    # Пароль надо хранить в БД в шифрованном виде.
    User.objects.create_user(
        username=request.POST["username"],
        email=request.POST["email"],
        password=request.POST["password1"]
    )
    return HttpResponseRedirect(reverse('home'))


def user_notes(request: WSGIRequest, username: str):
    queryset = queryset_optimization(
        Note.objects.filter(user__username=username)
    )
    # SELECT * FROM "posts_note"
    # INNER JOIN "users" ON ("posts_note"."user_id" = "users"."id")
    # WHERE "users"."username" = boris1992
    # ORDER BY "posts_note"."created_at" DESC

    print(Note.objects.filter(user__username=username).query)

    return render(request, "posts-list.html", {"notes": queryset})