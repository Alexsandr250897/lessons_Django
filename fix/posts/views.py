from django.shortcuts import render
from django.http import HttpRequest


def home_page_view(request: HttpRequest):
    return render(request, "home.html")



def create_note_view(request:HttpRequest):
    return render(request, "create_form.html")


def show_note_view(request:HttpRequest, not_id :int):
    return render(request, "note.html")