from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from .models import Course, Note
from .forms import CourseForm, NoteForm

# ----- ثبت نام -----
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notes:course_list')
    else:
        form = UserCreationForm()
    return render(request, 'notes/register.html', {'form': form})

# ----- مدیریت درس‌ها (Course) -----
@login_required
def course_list(request):
    courses = Course.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notes/course_list.html', {'courses': courses})

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return redirect('notes:course_list')
    else:
        form = CourseForm()
    return render(request, 'notes/course_form.html', {'form': form, 'title': 'ایجاد درس جدید'})

@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('notes:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'notes/course_form.html', {'form': form, 'title': 'ویرایش درس'})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('notes:course_list')
    return render(request, 'notes/confirm_delete.html', {'object': course, 'type': 'درس'})

# ----- مدیریت جزوه‌ها (Note) -----
@login_required
def note_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id, user=request.user)
    notes = course.notes.all().order_by('-created_at')
    return render(request, 'notes/note_list.html', {'course': course, 'notes': notes})

@login_required
def note_create(request, course_id):
    course = get_object_or_404(Course, pk=course_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.course = course
            note.save()
            return redirect('notes:note_list', course_id=course.id)
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'ایجاد جزوه جدید', 'course': course})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, course__user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:note_list', course_id=note.course.id)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form, 'title': 'ویرایش جزوه', 'course': note.course})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, course__user=request.user)
    course_id = note.course.id
    if request.method == 'POST':
        note.delete()
        return redirect('notes:note_list', course_id=course_id)
    return render(request, 'notes/confirm_delete.html', {'object': note, 'type': 'جزوه'})

# ----- جستجو -----
@login_required
def search_notes(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Note.objects.filter(
            Q(course__user=request.user) & (Q(title__icontains=query) | Q(content__icontains=query))
        ).select_related('course')
    return render(request, 'notes/search_results.html', {'query': query, 'results': results})