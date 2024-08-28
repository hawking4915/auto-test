
from method.out_log import logger
from config.ProjectInfo import sendmail,receivemail,PassKey,project_name
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from time import strftime,localtime,time
from smtplib import SMTP_SSL

# -----------------------------------------------------------
#     author：wangshinan
#     description：发送测试报告邮件
#     param：1、attachment  测试报告全路径
#            2、content邮件内容
#     remarks：需邮箱开启POP3/SMTP服务，并获取授权码（QQ邮箱-设置-帐户）
# -----------------------------------------------------------

def send_mail(attachment, content):
    logger.info("开始发送测试报告......")
    subject = "[" + strftime('%Y%m%d_%H%M%S',localtime(time())) + "] " + project_name + "自动化测试报告"
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'html', 'utf-8'))
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sendmail
    msg['To'] = ','.join(receivemail)
    with open(attachment, 'rb') as f:
        mime = MIMEBase('application', 'octet-stream')
        attachment_name = attachment.split("\\")[-1]
        mime.add_header('Content-Disposition', 'attachment', filename=attachment_name)
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)
    try:
        stmp = SMTP_SSL(host="smtp.qq.com", port=465)
        stmp.connect(host="smtp.qq.com")
        stmp.login(sendmail, PassKey)
        stmp.sendmail(sendmail, receivemail, msg.as_string())
        stmp.quit()
        logger.info("Test report sent successfully.")
    except Exception as e:
        logger.error("\033[1;35mFailed to send test report : %s.\033[0m" % (str(e)))
