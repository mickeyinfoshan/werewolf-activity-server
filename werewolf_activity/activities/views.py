from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Activity, Participation
import json
from datetime import datetime


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
            plain[datetime_field] = datetime_to_unix(
                getattr(model, datetime_field))
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
    activities = Activity.objects.filter(
        **selector).order_by("-created_at")[start:end]
    res = [make_activity_response(activity) for activity in activities]
    return JsonResponse(res, safe=False)


def activity_item(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    return JsonResponse(make_activity_response(activity))


def make_activity_response(activity):
    participations = activity.participation_set.order_by(
        "-created_at").all()
    activity_res = plain_model(activity)
    activity_res["members"] = [plain_model(p) for p in participations]
    return activity_res


def join_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    participant_count = activity.participation_set.count()
    if participant_count >= activity:
        return JsonResponse({"msg": "人数已达上限"}, status=400)
    params = {"openID": "", "avatar": "",
                       "nickname": "", "comment": ""}
    json_body = {}
    try:
        json_body = json.loads(request.body)
    except:
        pass
    param_sources = [request.GET, request.POST, json_body]
    for key in params:
        for source in param_sources:
            if key in source:
                params[key] = source[key]
    
    params_can_blank = ["comment"]
    for key in params:
        if key not in params_can_blank and params[key] == "":
            return JsonResponse({"msg": "%s不能为空" % key}, status=400)
    
    has_participated = activity.participation_set.filter(user_open_id=params["openID"]).count() > 0
    if has_participated:
        return JsonResponse({"msg": "已参加"}, status=400)
    activity.participation_set.create(user_open_id=params["openID"], user_avatar=params["avatar"], user_nickname=params["nickname"], comment=params["comment"])
    return JsonResponse({"msg": "成功参加"})

def quit_activity(request, activity_id):
    params = {"openID": ""}
    json_body = {}
    try:
        json_body = json.loads(request.body)
    except:
        pass
    
    param_sources = [request.GET, request.POST, json_body]
    for key in params:
        for source in param_sources:
            if key in source:
                params[key] = source[key]

    params_can_blank = []
    for key in params:
        if key not in params_can_blank and params[key] == "":
            return JsonResponse({"msg": "%s不能为空" % key}, status=400)
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.participation_set.filter(user_open_id=params["openID"]).delete()
    return JsonResponse({"msg":"成功鸽子"})

def del_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.delete()
    return JsonResponse({"msg":"删局成功"})

def save_activity(request, activity):
    str_params = {
        "openID": "", 
        "avatar": "",
        "nickname": "", 
        "name": "", 
        "address": "", 
        "description":"",
    }
    number_params = {
        "start": 0,
        "end": 0,
        "price": 0,
        "max": 15, 
    }
    json_body = {}
    try:
        json_body = json.loads(request.body)
    except:
        pass
    param_sources = [request.GET, request.POST, json_body]
    for key in str_params:
        for source in param_sources:
            if key in source:
                str_params[key] = source[key]

    for key in number_params:
        for source in param_sources:
            if key in source:
                try:
                    number_params[key] = int(source[key])
                except:
                    pass
    
    params_can_blank = ["description"]
    for key in str_params:
        if key not in params_can_blank and str_params[key] == "":
            return JsonResponse({"msg": "%s不能为空" % key}, status=400)
    
    activity.name = str_params["name"]
    activity.start = datetime.fromtimestamp(number_params["start"])
    activity.end = datetime.fromtimestamp(number_params["end"])
    activity.address = str_params["address"]
    activity.creator_avatar = str_params["avatar"]
    activity.creator_nickname = str_params["nickname"]
    activity.creator_open_id = str_params["openID"]
    activity.price = number_params["price"]
    activity.max_participants = number_params["max"]
    activity.description = str_params["description"]
    try:
        activity.save()
        return JsonResponse({"msg": "保存成功"})
    except:
        return JsonResponse({"msg": "保存失败"}, status=500)

def create_activity(request):
    activity = Activity()
    return save_activity(request, activity)

def update_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    return save_activity(request, activity)