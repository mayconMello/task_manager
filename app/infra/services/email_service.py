import smtplib
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader

from app.core.configs import settings


class EmailService:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('app/templates'))

    async def send_task_notification(self, to_email, tasks):
        template = self.env.get_template('email_template.html')
        html_content = template.render(tasks=tasks)

        msg = MIMEText(html_content, 'html')
        msg['Subject'] = "Upcoming Task Deadlines"
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = to_email

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, to_email, msg.as_string())
