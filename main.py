from flask import *
from public import public
from admin import admin
from candidate import candidate
from student import student
import smtplib
from email.mime.text import MIMEText
# from flask_mail import Mail
app=Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'projectblockchain2025@gmail.com'
app.config['MAIL_PASSWORD'] = 'icrv cqay bqsb clsl'

app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
# mail=Mail(app)


app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(candidate)
app.register_blueprint(student)










app.secret_key="qweert"
app.run(debug=True,port=5679)