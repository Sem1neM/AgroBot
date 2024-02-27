from peewee import DateTimeField
from playhouse.migrate import MySQLMigrator, migrate

import models


def main():
    models.conn.create_tables([models.Feedback])
    migrator = MySQLMigrator(models.conn)

    message_time = DateTimeField(column_name='message_time', default="")
    migrate(migrator.add_column('feedback', 'message_time', message_time))


if __name__ == '__main__':
    main()
