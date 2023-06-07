from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.Notification import Notification


from sqlalchemy import desc

def get_notifications_by_user_id(db: Session, user_id: int):
    notifications = db.query(Notification).filter(Notification.user_id == user_id and Notification.deleted==False).order_by(
        desc(Notification.time)
    ).all()
    
    if not notifications:
        return []
    
    return notifications




def delete_notification_by_id(db: Session, notification_id: int):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(notification)
    db.commit()
    return notification
def markAsRead(notification_id: int,db:Session):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.read=True
    db.commit()
    return notification


def markAllAsRead(db:Session):
    notifications = db.query(Notification).all()
    for notification in notifications:
     
        notification.read=True
    db.commit()
    return "succedded"
