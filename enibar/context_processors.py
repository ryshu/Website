from .models import Note

def check_note(request):
    notes = None
    if request.method in ["POST", "GET"] and request.user.is_active:
        notes = Note.get_note(request.user)
    return {'user_notes': notes}
