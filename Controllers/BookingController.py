import random
from fastapi import HTTPException
from models.Desk import Desk
from models.Door import Door
from models.Material import Material
from models.Object import Object
from models.Reservation import Reservation
from datetime import datetime,timedelta
from models.User import User

from models.Workspace import Workspace

def get_available_time_slots(desk_id,date,db):

        # Generate list of all time slots from 06:00 to 22:00
        start_time = datetime.strptime('06:00', '%H:%M')
        end_time = datetime.strptime('22:00', '%H:%M')
        time_slots = []
        while start_time <= end_time:
            time_slots.append(start_time.strftime('%H:%M'))
            start_time += timedelta(minutes=30)
        # Remove time slots that are already reserved
        reservations = db.query(Reservation).filter_by(desk_id=desk_id, date=date).all()
        for r in reservations:
            start_time = datetime.strptime(r.start_time, '%H:%M')
            end_time = datetime.strptime(r.end_time, '%H:%M')
            if(r.status != "Canceled"):
                if "06:00" in time_slots:
                    time_slots = time_slots[time_slots.index("06:00")+1:]
                start_time += timedelta(minutes=30)
                while start_time <= end_time:
                    time_slot = start_time.strftime('%H:%M')
                    if time_slot in time_slots:
                        if (time_slot != end_time.strftime('%H:%M')):
                            time_slots.remove(time_slot)
                    start_time += timedelta(minutes=30)
        print(time_slots)
        return time_slots

def makeReservation(request, db):
    existing_reservation = db.query(Reservation).filter(
        Reservation.desk_id == request.deskId,
        Reservation.date == request.date,
        Reservation.start_time < request.endTime,
        Reservation.end_time > request.startTime
    ).first()

    if existing_reservation and existing_reservation.status != "Canceled":
        # Desk is already reserved for the specified time period
        raise HTTPException(status_code=401, detail="Desk already reserved")

    user_reservations = db.query(Reservation).filter_by(user_id=request.userId, date=request.date).all()

    for reservation in user_reservations:
        if reservation.status != "Canceled":
            raise HTTPException(status_code=401, detail="You have already reserved on this day")

    reservation = Reservation(
        user_id=request.userId,
        desk_id=request.deskId,
        start_time=request.startTime,
        end_time=request.endTime,
        date=request.date,
        anonymous=request.anonymousBooking,
        status='Active'
    )

    db.add(reservation)
    db.commit()
    return "Reservation added successfully."

def getWorkspacesForBooking(date,userId,db):
    workspaces = db.query(Workspace).all()
    listWorkspaces = []
    for w in workspaces:
        if(userHaveWorkspaceRights(w,userId,db)):
            print(w.name)   
            listUserId=[]
            nbAvailable = 1
            nbBooked =0
            s=0
            print(len(w.objects))
            for o in w.objects:
                if (isinstance(o,Desk)):
                    s=s+1
                    reservation = db.query(Reservation).filter(Reservation.desk_id == o.id ,Reservation.date == date ).first()
                    if(reservation):
                        obj ={
                            "id":reservation.user_id,
                            "showImage":reservation.anonymous
                        }
                        listUserId.append(obj)
                        nbBooked = nbBooked+1
                nbAvailable = s
            if (s !=0):
                nbAvailable = 100 - (nbBooked*100)/s
            userProfileImages =[]
            for obj in listUserId:
                l ={
                    "anonymous" : obj['showImage'],
                    "img":""
                }
                if(not l["anonymous"]):
                    user = db.query(User).filter(User.id == obj['id']).first()
                    if(user.avatar):
                        l['img'] = user.avatar
                        userProfileImages.append(l)
                else:
                    userProfileImages.append(l)
            random_selection = random.sample(userProfileImages, len(listUserId))
            listWorkspaces.append({
                "name" : w.name,
                "totalPlaces" : s,
                "nbBooked" : nbBooked,
                "nbAvailable" : nbAvailable,
                "userProfileImages":random_selection,
                "tags":w.tags
                })
    return listWorkspaces

def userHaveWorkspaceRights(w,u,db):
    s=0
    u = db.query(User).filter(User.id == u).first()
    if(w.tags):
        for t1 in u.role.tags:
            for t2 in w.tags:
                if(t2['key'] == t1['key'] and t2['value'] == t1['value']):
                    s = s+1
        if s>0:
            return True
        else:
            return False
    else:
        return True
def userHaveDeskRights(d,u,db):
    s=0
    u = db.query(User).filter(User.id == u).first()
    if(d.tags):
        print(d.tags)
        print('i am here')
        for t1 in u.role.tags:
            for t2 in d.tags:
                if(t2['key'] == t1['key'] and t2['value'] == t1['value']):
                    s = s+1
        if s > 0:
            return True
        else:
            return False
    else:
        return True





def getWorkspaceForBook(date:str,userId,name : str,db):
    workspace = db.query(Workspace).filter(Workspace.name == name).first()
    bookedDesks = []
    availableBookedDesks =[]
    deskWithoutPermission = []
    if(workspace):
        for o in workspace.objects:
            if (isinstance(o,Desk)):
                if(not userHaveDeskRights(o,userId,db)):
                    deskWithoutPermission.append(o.id)
                reservations = db.query(Reservation).filter(Reservation.desk_id == o.id ,Reservation.date == date ).all()
                if(reservations):
                    startTime = "22:00"
                    endTime = "06:00"
                    for r in reservations:
                        if(startTime > r.start_time):
                            startTime = r.start_time
                        if(endTime < r.end_time):
                            endTime = r.end_time
                    print(startTime)
                    print(endTime)
                    if(r.status != "Canceled"):
                        if ((startTime == "06:00") and (endTime == "22:00")):
                            bookedDesks.append(o.id)
                        else:
                            availableBookedDesks.append(o.id)

        print(bookedDesks)
        print(availableBookedDesks)
        print(deskWithoutPermission)
        return {
        "id":workspace.id,
        "mapUrl":workspace.mapUrl,
        "name" : workspace.name,
        "objects":workspace.objects,
        "bookedDesks":bookedDesks,
        "availableBookedDesks":availableBookedDesks,
        "deskWithoutPermission":deskWithoutPermission
    }
    else:
        return {}
def getReservationsPerDeskPerDay(desk_id,date,db):
    reservations = db.query(Reservation).filter(Reservation.desk_id == desk_id , Reservation.date == date)
    materials=db.query(Material).filter(Material.desk_id==desk_id).all()
    stringMaterials=""
    if materials:
     for index, item in enumerate(materials):
        stringMaterials += item.matname
        if index < len(materials) - 1:
            stringMaterials += "-"
    if(reservations):
        l=[]
        for r in reservations:
            user = db.query(User).filter(User.id == r.user_id).first()
            if(r.status != "Canceled"):
                print(r.status)

                l.append({
                "name":user.name,
                "start_time":r.start_time,
                "end_time":r.end_time,
                "anonymous":r.anonymous
                })
        return {"reservations":l,"materials":stringMaterials}
    else:
        return{}

from sqlalchemy import desc
from datetime import datetime
from sqlalchemy import func

from sqlalchemy import desc, func
from sqlalchemy import desc

from datetime import datetime

def get_user_reservations(user_id, db):
    try:
        current_datetime = datetime.now()
        reservations = db.query(Reservation).filter(Reservation.user_id == user_id).order_by(
            desc(Reservation.date),
            desc(Reservation.start_time)
        ).all()

        l = []
        for i in reservations:
            start_datetime = datetime.strptime(f"{i.date} {i.start_time}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(f"{i.date} {i.end_time}", "%Y-%m-%d %H:%M")

            status = "Active"
            if i.status == 'Canceled' :
              status ='Canceled'
            elif current_datetime > end_datetime:
                status = "Passed"
            elif start_datetime <= current_datetime <= end_datetime:
                status = "Occurring"
            i.status=status
            db.commit()
            type=""
            if i.anonymous:
              type='anonymously'
            else:
              type='publicly'
            d = {
                "start_time": i.start_time,
                "desk_id": i.desk_id,
                "date": i.date,
                "status": status,
                "workspace": get_workspace_name(db, i.desk_id),
                "end_time": i.end_time,
                "anonymous": type
            }
            l.append(d)

        db.commit()  # Commit the changes to the database
        
        return l

    except Exception as e:
        # Handle the exception here or log the error
        print(f"Error retrieving user reservations: {str(e)}")
        return None



def get_workspace_name(db, desk_id: int):
    obj = db.query(Object).filter(Object.id == desk_id).first()
    workspace_name = db.query(Workspace).filter(Workspace.id == obj.workspace_id).first().name
    return workspace_name


def get_all_reservations(db):
    try:
        current_datetime = datetime.now()

        reservations = db.query(Reservation).order_by(
            desc(Reservation.date),
            desc(Reservation.start_time)
        ).all()
        l = []
        for i in reservations:
            start_datetime = datetime.strptime(f"{i.date} {i.start_time}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(f"{i.date} {i.end_time}", "%Y-%m-%d %H:%M")

            status = "Active"
            if i.status == 'Canceled' :
              status ='Canceled'
            elif current_datetime > end_datetime:
                status = "Passed"
            elif start_datetime <= current_datetime <= end_datetime:
                status = "Occurring"
            i.status=status
            db.commit()
            type=""
            if i.anonymous:
              type='anonymously'
            else:
              type='publicly'
            username=db.query(User).filter(User.id==i.user_id).first().name  
            d = {
                "user_id":i.user_id,
                "name":username,
                "start_time": i.start_time,
                "desk_id": i.desk_id,
                "date": i.date,
                "status": status,
                "workspace": get_workspace_name(db, i.desk_id),
                "end_time": i.end_time,
                "anonymous": type
            }
            l.append(d)

        db.commit()  # Commit the changes to the database
        
        return l
    except Exception as e:
        # Handle the exception here or log the error
        print(f"Error retrieving user reservations: {str(e)}")
        return None


def cancelReservation(request,db):
        existing_reservation = db.query(Reservation).filter(
        Reservation.desk_id == request.deskId,
        Reservation.date == request.date,
        Reservation.start_time == request.startTime,
        Reservation.end_time == request.endTime
    ).first()
        print('aaa',existing_reservation,request)
        if existing_reservation:
          existing_reservation.status='Canceled'
          db.commit()
          return existing_reservation