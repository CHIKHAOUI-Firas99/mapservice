from fastapi import HTTPException
from models.Desk import Desk
from models.Door import Door
from models.Object import Object

from models.Workspace import Workspace

def makeReservation():
    pass

def getWorkspacesForBooking(date,db):
    workspaces = db.query(Workspace).all()
    listWorkspaces = []
    for w in workspaces:
        nbAvailable = 1
        nbBooked =0
        s=0
        print(len(w.objects))
        for o in w.objects:
            if (isinstance(o,Desk)):
                s=s+1
                if (o.users):
                    for i in o.users:
                        if(i.date == date):
                            nbBooked = nbBooked+1
                            print(w.name)
                            print("he has reservation")
            nbAvailable = s
        if (s !=0):
            nbAvailable = 100 - (nbBooked*100)/s
        listWorkspaces.append({
            "name" : w.name,
            "totalPlaces" : s,
            "nbBooked" : nbBooked,
            "nbAvailable" : nbAvailable
            })
    return listWorkspaces

def getWorkspaceForBook(date:str,name : str,db):
    workspace = db.query(Workspace).filter(Workspace.name == name).first()
    bookedDesks = []

    if(workspace):
        for o in workspace.objects:
            if (isinstance(o,Desk)):
                if(o.users):
                    for i in o.users:
                        if (i.date == date):
                            bookedDesks.append(o.id)
        print(bookedDesks)
        return {
        "id":workspace.id,
        "mapUrl":workspace.mapUrl,
        "name" : workspace.name,
        "objects":workspace.objects,
        "bookedDesks":bookedDesks
    }
    else:
        return {}