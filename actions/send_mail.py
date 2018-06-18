#! /usr/bin/python

import smtplib

from optparse import OptionParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

parser = OptionParser()
parser.add_option("-f", "--from", dest="sender", help="sender email address", default="no-reply@doma.in")
parser.add_option("-t", "--to", dest="recipient", help="recipient email address")
parser.add_option("-s", "--subject", dest="subject", help="email subject", default="Default Subject")
parser.add_option("-i", "--imageheader", dest="imageheader", help="image attachment", default=False)
parser.add_option("-b", "--imagefooter", dest="imagefooter", help="image attachment", default=False)
parser.add_option("-c", "--content", dest="content", help="mail content", default=False)

(options, args) = parser.parse_args()

# Create message container.
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = options.subject
msgRoot['From'] = options.sender
msgRoot['To'] = options.recipient
msgRoot['Content'] = options.content
# Create the body of the message.
html = """\
 <html>
  <body>
     <table align="center" border=1>
       <tr><td style="width:150px"><img style="display:block;" src="cid:image1"></img></td> </tr>
       <tr><td style="width:150px"><div style="color:blue;max-width:990px;word-wrap: break-word;">""" + options.content + """</div></td></tr>
       <tr><td style="width:150px"><img style="display:block;" src="cid:image2" ></img></td></tr>
    </table>
  </body>
 </html>
"""

# Record the MIME types.
msgHtml = MIMEText(html, 'html')

if options.imageheader is not False:
    img = open(options.imageheader, 'rb').read()
    msgImg = MIMEImage(img, 'jpg')
    msgImg.add_header('Content-ID', '<image1>')
    msgImg.add_header('Content-Disposition', 'inline', filename=options.imageheader)

if options.imagefooter is not False:
    img = open(options.imagefooter, 'rb').read()
    msgfooter = MIMEImage(img, 'jpg')
    msgfooter.add_header('Content-ID', '<image2>')
    msgfooter.add_header('Content-Disposition', 'inline', filename=options.imagefooter)

msgRoot.attach(msgHtml)
msgRoot.attach(msgImg)
msgRoot.attach(msgfooter)

# Send the message via local SMTP server.
s = smtplib.SMTP('smtp-out.us.dell.com:25')
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
#s.sendmail(options.sender, options.recipient, msgRoot.as_string())
s.sendmail(options.sender, options.recipient, msgRoot.as_string())
s.quit()
