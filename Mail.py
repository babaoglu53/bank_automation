from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys
from HtmlContent import HtmlContent

class Mail:
    def sendMailForMoneyTransactions(self, subject, transaction_name, transaction_name_2, account_no, amount, mail, mail_pass, to_mail):
        message = MIMEMultipart()
        message["From"] = mail
        message["To"] = to_mail
        message["Subject"] = subject
        
        html_content = HtmlContent().getHtmlContentForMoneyTransactions(transaction_name, transaction_name_2, account_no, amount)
        message_body =  MIMEText(html_content,"html")
        message.attach(message_body)

        try:
            mail = smtplib.SMTP("smtp.yandex.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login(message["From"], mail_pass)
            mail.sendmail(message["From"], message["To"], message.as_string())
            print("Mail başarıyla gönderildi...")
            mail.close()
        except Exception as e:
            print(e)
            sys.stderr.write("Mail göndermesi başarısız oldu...")
            sys.stderr.flush()

    def sendMailForVerification(self, subject, message_text, verification_code, mail, mail_pass, to_mail):
        message = MIMEMultipart()
        message["From"] = mail
        message["To"] = to_mail
        message["Subject"] = subject
        
        html_content = HtmlContent().getHtmlContentForVerification(message_text, verification_code)
        message_body =  MIMEText(html_content,"html")
        message.attach(message_body)

        try:
            mail = smtplib.SMTP("smtp.yandex.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login(message["From"], mail_pass)
            mail.sendmail(message["From"], message["To"], message.as_string())
            print("Mail başarıyla gönderildi...")
            mail.close()
        except Exception as e:
            print(e)
            sys.stderr.write("Mail göndermesi başarısız oldu...")
            sys.stderr.flush()