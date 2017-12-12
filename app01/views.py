from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from app01 import models
import datetime

def index(request):


    time_choice = models.Booking.time_choices

    return render(request,"index.html",{"time_choice":time_choice})

def booking(request):

    # current_data=datetime.datetime.now().date()
    # models.Booking.objects.create(user_id=1,room_id=1,booking_date=current_data,booking_time=13)
    # models.Booking.objects.create(user_id=1, room_id=2, booking_date=current_data, booking_time=13)
    # models.Booking.objects.create(user_id=1, room_id=3, booking_date=current_data, booking_time=13)

    choice_date = request.GET.get("choice_date")
    print(choice_date,'-------------------')
    data = datetime.datetime.strptime(choice_date,"%Y-%m-%d").date()
    print("data",type(data))

    res = {"status":True,"msg":None,"error":None}
    try:

        #获取指定日期的预定信息
        booking_list = models.Booking.objects.filter(booking_date=data)
        print(booking_list)
        booking_dict = {}
        for item in booking_list:

            if item.room_id not in booking_dict:
                booking_dict[item.room_id] = {item.booking_time: {'name': item.user.name, 'id': item.user.id}}
            else:
                if item.booking_time not in booking_dict[item.room_id]:
                    booking_dict[item.room_id][item.booking_time] = {'name': item.user.name, 'id': item.user.id}
        print(booking_dict)




        room_list = models.MeetingRoom.objects.all()
        data = []
        for room in room_list:
            tr = []
            tr.append({"text":room.title,"attrs":''})

            for tm in models.Booking.time_choices:

                if room.id in booking_dict and tm[0] in booking_dict[room.id]:
                    print(room.id, tm[0])
                    td = {"text": booking_dict[room.id][tm[0]]["name"], "attrs": {"room_id": room.id, "time_id": tm[0], "class": "aaa"}}
                else:
                    td = {"text": '', "attrs": {"room_id": room.id, "time_id": tm[0]}}

                tr.append(td)
                #print(td)
            data.append(tr)



        res["msg"] = data
        return JsonResponse(res)
    except Exception as e:
        res["status"] = False
        res["error"] = str(e)
    print(res)
    return JsonResponse(res)
