from django.db.models import F
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from .models import Question, Answer, Poll, Voter


def question(request, pid):
    if not request.user.is_authenticated():
        raise Http404
    p = get_object_or_404(Poll, id=pid)
    try:
        already_voted = Voter.objects.get(user=request.user, poll=p)
    except Voter.DoesNotExist:
        pass
    else:
        return redirect(reverse('poll:already'))

    context = {'poll': p, 'pid': pid, "errors": []}
    answers = {q.id: request.POST.get("question{}".format(q.id), None) for q in p.questions.all()}

    if all(answers.values()):
        if any(int(Answer.objects.get(id=aid).question.id) != int(qid) for qid, aid in answers.items()):
            context["errors"].append("Nope")  # This should NEVER happen
            return render(request, 'poll/question.html', context)
        for aid in answers.values():
            Answer.objects.filter(id=aid).update(votes=F("votes") + 1)
        v = Voter(user=request.user, poll=p)
        v.save()
        return redirect(reverse('poll:thanks'))
    else:
        context["errors"].append("Veuillez répondre à toutes les questions")
    return render(request, 'poll/question.html', context)


def thanks(request):
    return render(request, 'poll/thanks.html', {})


def already(request):
    return render(request, 'poll/already.html', {})

def admin_index(request):
    context = {'polls': Poll.objects.all()}
    return render(request, 'poll/admin/index.html', context)
