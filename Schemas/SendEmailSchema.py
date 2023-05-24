from pydantic import BaseModel

class SendEmails(BaseModel):
    emails: list
    subject: str
    body: str
