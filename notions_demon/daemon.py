from template import Daemon
from time import sleep
from datetime import datetime
import sys
from sqlite3 import connect
class NotionDaemon(Daemon):
    def create_cursor(self):
        c = connect("db.sqlite3")
        return c
    def fetch_users(self, cur, working_for):
        res = cur.execute(
        f"""
        SELECT id FROM users_customuser
        WHERE is_HR=false AND 
            is_started=true AND
            start_date=adddate(now(), -7 * {working_for})
        """
        ).fetchall()

        return res

    def crecte_notion(self, cur, working_for, id):
        description = ""
        if working_for in (1, 2):
            description = f"""
                Вы уже {"неделю" if working_for == 1 else '2 недели'}
                являетесь членом нашей команды,
                заполните пожалуйста форму обратной связи: 
                __URL__
                """
        else:
            description = f""" 
                Конец вашего онбординга близок, в скором времени с вами свяжется ваш HR для интервью
                            """
        cur.execute(
            f"""
            INSERT INTO notifications_notification
                VALUES(
                    title="Обратная связь",
                    description={description},
                    date=GETDATE(),
                    is_readed=false,
                    sender=(SELECT HR_link FROM users_customuser WHERE id={id}),
                    to_id={id}
                    )
            """
        )

    def create_notions(self):
        cursor = self.create_cursor()
        for week_count in (1, 2, 4):
            users = self.fetch_users(cursor, week_count)
            for user_id in users:
                self.crecte_notion(cursor, week_count, user_id)

        cursor.commit()
        cursor.close()

    def test_insert(self):
        cursor = self.create_cursor()
        users = cursor.execute("""SELECT id FROM users_customuser WHERE is_HR=false""").fetchmany(3)
        self.crecte_notion(cursor, 1, users[0])
        self.crecte_notion(cursor, 2, users[1])
        self.crecte_notion(cursor, 4, users[2])

        cursor.commit()
        cursor.close()

    def run(self):
        while True:
            sleep(10)
            now = datetime.now()
            if now.hour == 0 and now.minute == 0:
                self.create_notions()
                sleep(60)


if __name__ == "__main__":
    d = NotionDaemon("notions_demon/pidfile.pid")
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            d.start()
        elif 'stop' == sys.argv[1]:
            d.stop()
        elif 'restart' == sys.argv[1]:
            d.restart()
        elif 'check' == sys.argv[1]:
            d.is_running()
        elif 'test_insert' == sys.argv[1]:
            d.test_insert()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print(f"usage: {sys.argv[0]} start|stop|restart|check|test_insert")
        sys.exit(2)
