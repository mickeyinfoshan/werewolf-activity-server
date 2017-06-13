from django.shortcuts import render
from django.http import JsonResponse
from .models import Activity, Participation

class PageRequest:
    page = 0
    page_size = 20

    def __init__(self, page, page_size):
        try:
            self.page = int(page)
        except ValueError:
            self.page = 0
        try:
            self.page_size = int(page_size)
        except ValueError:
            self.page_size = 20

def get_page_req(request):
    return PageRequest(request.GET.get("page", 0), request.GET.get("pageSize", 20))

def plain_model(model):
    plain = model.__dict__.copy()
    datetime_fields = model.get_datetime_fields()
    # print(datetime_fields)
    common_except_prefix = ["_"]
    try:
        datetime_fields = model.get_datetime_fields()
        print(datetime_fields)
        for datetime_field in datetime_fields:
            plain[datetime_field] = datetime_to_unix(getattr(model, datetime_field))
    except:
        pass

    fields_to_del = []
    for prefix in common_except_prefix:
        for field in plain:
            if field.startswith(prefix):
                fields_to_del.append(field)
    for field in fields_to_del:
        del plain[field]
    return plain


def datetime_to_unix(dt):
    if dt.year < 1900:
        return 0
    return int(dt.strftime("%s"))

# Create your views here.
def activity_list(request):
    page_req = get_page_req(request)
    start = page_req.page * page_req.page_size
    end = start + page_req.page_size
    except_query = ["page", "pageSize"]
    selector = {}
    for q in request.GET:
        if q not in except_query:
            selector[q] = request.GET[q]
    activities = Activity.objects.filter(**selector).order_by("-created_at")[start:end]
    res = []
    for activity in activities:
        participations = activity.participation_set.order_by("-created_at").all()
        activity_res = plain_model(activity)
        activity_res["members"] = [plain_model(p) for p in participations]
        res.append(activity_res)
            
    return JsonResponse(res, safe=False)