from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.utils.html import escape
from django.urls import reverse

from notes import data


# Create your views here.

def _html_shell(title: str, body: str) -> str:
    safe_title = escape(title)
    return f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

    <style>
        body {{background: linear-gradient(135deg, #f8f9fa, #e9f2ff);      min-height: 100vh;}}

        .main-card {{
            border: none;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        }}

        .navbar-brand {{
            font-weight: 700;
            letter-spacing: 0.5px;
        }}

        code {{
            background: #f1f3f5;
            padding: 0.15rem 0.4rem;
            border-radius: 6px;
            color: #d63384;
        }}

        .notes li {{
            margin-bottom: 0.5rem;
        }}

        textarea {{
            min-height: 140px;
            resize: vertical;
        }}

        footer {{
            color: #6c757d;
            font-size: 0.95rem;
        }}
    </style>
</head>
<body>

    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="{escape(reverse('home'))}">MySite</a>

            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#mainNavbar"
                aria-controls="mainNavbar"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="mainNavbar">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('home'))}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('about'))}">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('notes_list'))}">Notes</a>
                    </li>
                     <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('note_create'))}">Create new note</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main class="container py-5">
        <div class="card main-card">
            <div class="card-body p-4 p-md-5">
                {body}
            </div>
        </div>
    </main>

    <footer class="text-center py-4">
        <div class="container">
            <span>Powered by Nadir Zamanov</span>
        </div>
    </footer>

    <script
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js">
    </script>
</body>
</html>
"""


def _csrf_field(request: HttpRequest) -> str:
    token = get_token(request)
    return f'<input type="hidden" name="csrfmiddlewaretoken" value="{escape(token)}">'


def home(request: HttpRequest) -> HttpResponse:
    body = f"""
        <div class="card shadow-lg border-0 rounded-4 p-4 text-center" style="max-width: 500px;">

        <h1 class="fw-bold mb-3">📘 Knowledge Hub</h1>

        <p class="text-muted">
            Welcome! This is home page
        </p>

        <a href="{escape(reverse('notes_list'))}" 
           class="btn btn-primary mt-3">
            📂 Go to Notes
        </a>

    </div>
</div>"""
    return HttpResponse(_html_shell("Knowledge Hub - home page", body))


def about(request: HttpRequest) -> HttpResponse:
    body = f"""
            <div class="d-flex justify-content-center">
    <div class="card shadow-lg border-0 rounded-4 p-4 text-center" style="max-width: 500px;">

        <h1 class="fw-bold mb-3">ℹ️ About this Project</h1>

        <p class="text-muted mb-2">
            Knowledge Hub — project for Django course
        </p>

        <p class="badge bg-primary-subtle text-primary px-3 py-2">
            Lesson 7 — Views & Routes
        </p>

    </div>
</div>
        """
    return HttpResponse(_html_shell("Knowledge Hub - about page", body))


def notes_list(request: HttpRequest) -> HttpResponse:
    raw_tag = request.GET.get('tag')
    raw_category = request.GET.get('category')

    notes = data.list_notes()

    if raw_tag:
        tag_filter = raw_tag.strip().lower()
        notes = [n for n in notes if n['tag'.lower()] == tag_filter]

    if raw_tag:
        category_filter = raw_category.strip().lower()
        notes = [n for n in notes if n['category'.lower()] == category_filter]

    items: list[str] = []
    for note in notes:
        url = reverse('note_detail', kwargs={'note_id': note['id']})
        items.append(f"""
        <li class="list-group-item d-flex justify-content-between align-items-start">

    <div>
        <a href="{escape(url)}" class="fw-semibold text-decoration-none">
            {escape(note['title'])}
        </a>

        <div class="small text-muted mt-1">
            Tag: <span class="badge bg-info text-dark">{escape(note["tag"])}</span>
            Category: <span class="badge bg-secondary">{escape(note["category"])}</span>
        </div>
    </div>

</li>
""")

    items_html = "\n    ".join(items) if items else "<li class=muted>Notes not found</li>"

    filter_hint = f"""
        <p class="muted"> Filter example from query string:
        <a href="?tag=python><code>?tag=python</code></a>
        <a href="?category=django><code>?category=django</code></a>
        <a href="{escape(reverse("notes_list"))}>Reset filters</a?
        </p>
    """
    body = f"""
   <div class="container d-flex justify-content-center">

    <div class="card shadow-lg border-0 rounded-4 w-100" style="max-width: 700px;">

        <div class="card-body p-4">

            <div class="text-center mb-4">
                <h1 class="fw-bold">📒 Notes</h1>
                <p class="text-muted">Browse your saved notes</p>
            </div>

            <ul class="list-group list-group-flush">
                {items_html}
            </ul>

        </div>

    </div>

</div>
    """

    return HttpResponse(_html_shell("Notes list", body))


def note_detail(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return HttpResponse(f"""
        <div class="d-flex justify-content-center align-items-center" style="min-height: 60vh;">

    <div class="card shadow-lg border-0 rounded-4 p-4 text-center" style="max-width: 500px;">

        <h1 class="fw-bold text-danger mb-3">⚠️ Note not found</h1>

        <p class="text-muted mb-2">
            ID: <code>{escape(str(note_id))}</code>
        </p>

        <p class="text-secondary">
            The requested note does not exist or was removed.
        </p>

        <a href="{escape(reverse('notes_list'))}" 
           class="btn btn-primary mt-3">
            ⬅ Return to Notes
        </a>

    </div>

</div>
""", status=404)
    edit_url = reverse('note_edit', kwargs={'note_id': note["id"]})
    delete_url = reverse('note_delete', kwargs={'note_id': note["id"]})
    list_url = escape(reverse("notes_list"))

    body = f"""
    <div class="container d-flex justify-content-center">

    <div class="card shadow-lg border-0 rounded-4 w-100" style="max-width: 700px;">

        <div class="card-body p-4">

            <h1 class="fw-bold mb-3">
                {escape(note["title"])}
            </h1>

            <div class="mb-3 text-muted small">
                ID: <code>{note["id"]}</code>

                <span class="ms-2 badge bg-info text-dark">
                    {escape(note["tag"])}
                </span>

                <span class="ms-1 badge bg-secondary">
                    {escape(note["category"])}
                </span>
            </div>

            <div class="mb-4">
                <p class="fs-5">
                    {escape(note["body"]).replace(chr(10), "<br />")}
                </p>
            </div>

            <div class="d-flex gap-2 flex-wrap">

                <a href="{edit_url}" class="btn btn-warning">
                    ✏️ Edit
                </a>

                <a href="{delete_url}" class="btn btn-danger">
                    🗑 Delete
                </a>

                <a href="{list_url}" class="btn btn-outline-primary ms-auto">
                    ⬅ Back to Notes
                </a>

            </div>

        </div>

    </div>

</div>
"""
    return HttpResponse(_html_shell(note["body"], body))


def note_create(request: HttpRequest) -> HttpResponse:
    title_val = ""
    body_val = ""
    tag_val = ""
    category_val = ""

    if request.method == "POST":
        title = request.POST.get("title", "")
        note_body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        title_val, body_val, tag_val, category_val = title, note_body, tag, category

        if not title.strip():
            err = "<p class='muted' style = 'color: #b00020;'>Title cannot be empty</p>"
        else:
            data.create_note(title=title, body=note_body, tag=tag or "misc", category=category or "general")
            return redirect("notes_list")
    else:
        err = ""

    form = f"""
    <div class="container d-flex justify-content-center">

    <div class="card shadow-lg border-0 rounded-4 w-100" style="max-width: 600px;">

        <div class="card-body p-4">

            <h1 class="fw-bold mb-4 text-center">➕ New Note</h1>

            {err}

            <form method="post" action="{escape(reverse('note_create'))}">
                {_csrf_field(request)}

                <div class="mb-3">
                    <label class="form-label">Title</label>
                    <input 
                        type="text" 
                        name="title" 
                        class="form-control"
                        value="{escape(title_val)}" 
                        required
                    >
                </div>

                <div class="mb-3">
                    <label class="form-label">Text</label>
                    <textarea 
                        name="body" 
                        class="form-control" 
                        rows="6"
                        value="{escape(body_val)}" 
                    ></textarea>
                </div>

                <div class="mb-3">
                    <label class="form-label">Tag</label>
                    <input 
                        type="text" 
                        name="tag" 
                        class="form-control"
                        value="{escape(tag_val)}" 
                        placeholder="Python"
                    >
                </div>

                <div class="mb-3">
                    <label class="form-label">Category</label>
                    <input 
                        type="text" 
                        name="category" 
                        class="form-control"
                        value="{escape(category_val)}" 
                        placeholder="Django"
                    >
                </div>

                <div class="d-flex justify-content-between align-items-center mt-4">

                    <a href="{escape(reverse('notes_list'))}" 
                       class="text-muted text-decoration-none">
                        Cancel
                    </a>

                    <button type="submit" class="btn btn-success px-4">
                        💾 Save
                    </button>

                </div>

            </form>

        </div>

    </div>

</div>
"""
    return HttpResponse(_html_shell("Create note", form))


def note_edit(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return HttpResponse(_html_shell("404 not found", f"""
    <h1>Can't edit</h1>
    <p class="muted">Note id: {escape(str(note_id))} nor found</p>
    <p><a href="{escape(reverse("notes_list"))}">Return to Nodes List</a></p>
"""), status=404)

    if request.method == "POST":
        title = request.POST.get("title", "")
        note_body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        if not title.strip():
            err = "<p class='muted' style = 'color: #b00020;'>Title cannot be empty</p>"

            note = {
                **note,
                "title": title,
                "body": note_body,
                "tag": tag,
                "category": category,
            }
        else:
            data.update_note(
                note_id,
                title=title,
                body=note_body,
                tag=tag or "misc",
                category=category or "general",
            )
            return redirect("note_detail", note_id=note_id)
    else:
        err = ""
        title_e = escape(note["title"])
        note_e = escape(note["body"])
        tag_e = escape(note["tag"])
        category_e = escape(note["category"])

        form = f"""
        <h1>Edit</h1>
        <form method="post" action="{escape(reverse("note_edit", kwargs={"note_id": note_id}))}" >
        {_csrf_field(request)}
        <div class="mb-3">
                    <label class="form-label">Title</label>
                    <input 
                        type="text" 
                        name="title" 
                        class="form-control"
                        value="{title_e}" 
                        required
                    >
                </div>

                <div class="mb-3">
                    <label class="form-label">Text</label>
                    <textarea 
                        name="body" 
                        class="form-control" 
                        rows="6"
                    >{note_e}</textarea>
                </div>

                <div class="mb-3">
                    <label class="form-label">Tag</label>
                    <input 
                        type="text" 
                        name="tag" 
                        class="form-control"
                        value="{tag_e}" 
                    >
                </div>

                <div class="mb-3">
                    <label class="form-label">Category</label>
                    <input 
                        type="text" 
                        name="category" 
                        class="form-control"
                        value="{category_e}" 
                        
                    >
                </div>

                <div class="d-flex justify-content-between align-items-center mt-4">

                    <a href="{escape(reverse('note_detail', kwargs={'note_id': note_id}))}" 
                       class="text-muted text-decoration-none">
                        Cancel
                    </a>

                    <button type="submit" class="btn btn-success px-4">
                        💾 Save
                    </button>

                </div>
    </form>        
"""
        return HttpResponse(_html_shell("Edit note", form))

def note_delete(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return HttpResponse(_html_shell("404", "<h1>Note not found</h1>"), status=404)
    
    if request.method == "POST":
        data.delete_note(note_id)
        return redirect("notes_list")
    
    delete_url = reverse('note_delete', kwargs={'note_id': note_id})
    cancel_url = reverse('note_detail', kwargs={'note_id': note_id})
    csrf_input = _csrf_field(request)
    safe_title = escape(note['title'])

    form = f"""
    <div id="deleteModal" style="position:fixed; z-index:9999; left:0; top:0; width:100%; height:100%; background-color: rgba(0,0,0,0.6);">
        <div class="card main-card" style="margin:15% auto; padding:30px; width:450px; text-align:center; background: white; border: none; border-radius: 15px;">
            <h2 class="fw-bold text-danger mb-3">Are you sure?</h2>
            <p class="text-muted mb-4">Do you really want to delete note:<br><strong class="text-dark">"{safe_title}"</strong>?</p>
            
            <div class="d-flex justify-content-center gap-3">
                <form action="{escape(delete_url)}" method="POST">
                    {csrf_input}
                    <button type="submit" class="btn btn-danger px-4 shadow-sm">Delete</button>
                </form>
                <a href="{escape(cancel_url)}" class="btn btn-outline-secondary px-4">
                    Cancel
                </a>
            </div>
        </div>
    </div>
    """
    return HttpResponse(_html_shell("Delete note", form))
