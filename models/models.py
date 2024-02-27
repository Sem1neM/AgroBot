from peewee import *

from config import DB_PASSWORD, DB_NAME, DB_USER, DB_HOST

conn = MySQLDatabase(
    database=DB_NAME, user=DB_USER,
    password=DB_PASSWORD, host=DB_HOST
)


class BaseModel(Model):
    class Meta:
        database = conn


class Feedback(BaseModel):
    user_id = CharField(column_name="user_id")
    message = CharField(column_name="message")
    message_time = DateTimeField(column_name="message_time")

    class Meta:
        table_name = "feedback"

# TODO: Здесь должны быть классы хранящие в себя данные финансирования (гранты, субсидии). Придумать их грамотное
#  отображение
