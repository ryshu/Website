from ..models import Event, Inscription, ExternInscription, Invitation
from bde.shortcuts import bde_member, is_contributor
from shop.models import BuyingHistory
from django.db.models import Count

from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.templatetags.static import static

import json


@bde_member
def admin_management(request, eid):
    event = get_object_or_404(Event, id=eid)
    if event.gestion is None:
        raise Http404

    context = {'event': event}

    return render(request, 'events/admin/management_index.html', context)

@bde_member
def management_list_users(request, eid):
    e = get_object_or_404(Event, id=eid)
    ret = {}
    if request.method == "OPTIONS":
        # Reg
        ret['reg'] = [{
                "display_name": str(ins.user.profile),
                "picture": ins.user.profile.get_picture_url(),
                "color": "bg-blue" if ins.in_date is not None else "bg-green" if is_contributor(ins.user) else "bg-red",
                "type": "reg",
                "id": ins.id,
            } for ins in Inscription.objects.filter(event=e).select_related("user__profile").select_related('event').select_related("user__contribution").annotate(null_nick=Count('user__profile__nickname')).order_by('null_nick', '-user__profile__nickname', '-user__last_name', '-user__first_name', '-user__username').reverse()
        ]
        ret['ext_reg'] = [{
                "display_name": "{} {} ({})".format(ins.last_name, ins.first_name, ins.via.name),
                "picture": static('images/default_user_icon.png'),
                "color": "bg-blue" if ins.in_date is not None else "",
                "type": "ext_reg",
                "id": ins.id,
            } for ins in ExternInscription.objects.filter(event=e).select_related('event').select_related('via').order_by('last_name', 'first_name')
        ]
        ret['invits'] = [{
                "display_name": "{} {} (invité par {})".format(ins.first_name, ins.last_name, str(ins.user.profile)),
                "picture": static('images/default_user_icon.png'),
                "color": "bg-blue" if ins.in_date is not None else "",
                "type": "invit",
                "id": ins.id,
            } for ins in Invitation.objects.filter(event=e).select_related('event').select_related('user__profile').order_by('last_name', 'first_name')
        ]
        return JsonResponse(ret)


@bde_member
def management_info_user(request, eid, type, iid):
    e = get_object_or_404(Event, id=eid)
    context = {'type': type, 'iid': iid, 'event': e}
    if type == "reg":
        ins = Inscription.objects.select_related('user__profile').get(event=e, id=iid)
        context['ins'] = ins
        context['display_name'] = str(ins.user.profile)
        context['products'] = [prod for prod in BuyingHistory.get_all_bought_products(ins.user) if prod.event == e]
    elif type == "ext_reg":
        pass
    else:
        pass
    return render(request, "events/admin/info_popup.html", context)


@bde_member
def management_ack(request, eid, type, iid):
    e = get_object_or_404(Event, id=eid)
    if type == "reg":
        ins = Inscription.objects.get(event=e, id=iid)
        ins.in_date = timezone.now()
        ins.save()
        return JsonResponse({"status": 1})
    elif type == "ext_reg":
        pass
    else:
        pass
    return render(request, "events/admin/info_popup.html")


@bde_member
def management_nl_ack(request):
    req = json.loads(request.read().decode())
    e = get_object_or_404(Event, id=req['eid'])

    if req['type'] == "reg":
        ins = Inscription.objects.get(event=e, id=req['iid'])
    elif req['type'] == "ext_reg":
        ins = ExternInscription.objects.get(event=e, id=req['iid'])
    else:
        ins = Invitation.objects.get(event=e, id=req['iid'])

    ins.payment_mean = req.get("payment_mean")
    ins.in_date = timezone.now()
    ins.save()
    return JsonResponse({"status": 1})


@bde_member
def management_nl_del(request, eid, type, iid):
    e = get_object_or_404(Event, id=eid)
    klass = ""
    if type == "reg":
        ins = Inscription.objects.get(event=e, id=iid)
        if(is_contributor(ins.user)):
            klass = "bg-green"
        else:
            klass = "bg-red"
    elif type == "ext_reg":
        ins = ExternInscription.objects.get(event=e, id=iid)
    else:
        ins = Invitation.objects.get(event=e, id=iid)

    ins.payment_mean = None
    ins.in_date = None
    ins.save()
    return JsonResponse({"status": 1, "klass": klass})


@bde_member
def management_nl_info_user(request, eid, type, iid):
    e = get_object_or_404(Event, id=eid)
    context = {'type': type, 'iid': iid, 'eid': eid, 'event': e}
    if type == "reg":
        ins = Inscription.objects.select_related('user__profile').get(event=e, id=iid)
        context['display_name'] = str(ins.user.profile)
    elif type == "ext_reg":
        ins = ExternInscription.objects.get(event=e, id=iid)
        context['display_name'] = "{} {}".format(ins.first_name, ins.last_name)
    else:
        ins = Invitation.objects.get(event=e, id=iid)
        context['display_name'] = "{} {}".format(ins.first_name, ins.last_name)
    context['ins'] = ins
    return render(request, "events/admin/info_nl_popup.html", context)


@bde_member
def management_nl_ack_popup(request, iid, eid):
    context = {"eid": eid, "iid": iid}
    return render(request, "events/admin/nl_ack_popup.html", context)

