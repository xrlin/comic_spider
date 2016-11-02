import time
import asyncio
from mailthon import email
from mailthon.postman import Postman
from mailthon.middleware import TLS, Auth

TEMPLATE = """
    <HTML>
        <BODY>
            <H1>海贼王漫画更新了</H1>
        </BODY>
    </HTML>
"""

class RemindMailer(Postman):

    @classmethod
    def config_for(cls, settings):
        return cls(host=settings.get('MAIL_HOST'),
            port=settings.get('MAIL_PORT'),
            middlewares=[
                TLS(force=True),
                Auth(username=settings.get('MAIL_USER'),
                password=settings.get('MAIL_PASS'))
            ])

    def send_mail(self, spider):
        print('*'*40)
        print('Sending mail to {}'.format(spider.settings.get("MAIL_TO")))
        return self.send(email(
        content=TEMPLATE,
        subject='漫画更新提醒',
        sender=spider.settings.get('MAIL_FROM'),
        receivers=spider.settings.get('MAIL_TO'),
        ))
        # self.send(to=spider.settings.get("MAIL_TO"), subject="漫画更新提醒", body=TEMPLATE, mimetype='text/html', charset='utf-8')
    def async_send(self, spider):
        r = self.send_mail(spider)
        print('Send mail success.') if r.ok else print('Send mail failed!')
        # # 获取EventLoop:
        # loop = asyncio.get_event_loop()
        # # 执行coroutine
        # loop.run_until_complete(self.send_mail(spider))
        # loop.close()
