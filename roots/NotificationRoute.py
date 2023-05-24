from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from Controllers import NotificationController as notification_controller


notificationRouter = APIRouter()


@notificationRouter.get("/notification/{user_id}")
def get_notifications_by_user_id(user_id: int, db: Session = Depends(get_db)):
    notifications = notification_controller.get_notifications_by_user_id(db, user_id)
    return notifications


@notificationRouter.delete("/notification/{notification_id}")
def delete_notification_by_id(notification_id: int, db: Session = Depends(get_db)):
    deleted_notification = notification_controller.delete_notification_by_id(db, notification_id)
    return deleted_notification


@notificationRouter.put("/read_notification/{notification_id}")
def mark_notif_readed(notification_id: int, db: Session = Depends(get_db)):
    return notification_controller.markAsRead(notification_id, db)
    

@notificationRouter.get("/read_notifications/")
def mark_all_notif_readed(db: Session = Depends(get_db)):
    return notification_controller.markAllAsRead (db)
    