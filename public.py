from flask import *
from database import *
public=Blueprint(__name__,'public')


@public.route('/')
def index():
    return render_template('public/index.html')

@public.route('/login',methods=['get','post'])
def login():
    if 'submit' in request.form:
        username=request.form['username']
        password=request.form['password']
        q="select * from login where username='%s' and password='%s'"%(username,password)
        res=select(q)
        if res:
            session['login_id']=res[0]['login_id']
            if res[0]['usertype']=='admin':
                q1="select * from login where login_id='%s'"%(session['login_id'])
                res1=select(q1)
                if res1:
                    session['admin_id']=res1[0]['login_id']
                    return "<script>alert('Admin login success');window.location='/admin_home'</script>"
            elif res[0]['usertype']=='student':
                q2="select * from student where login_id='%s'"%(session['login_id'])
                res2=select(q2)
                if res2:
                    session['student_id']=res2[0]['student_id']
                    session['email']=res2[0]['email']
                    return "<script>alert('Student login success');window.location='/student_home'</script>"
                else:
                    return "<script>alert('invalid student login');window.location='/login'</script>"
            elif res[0]['usertype']=='candidate':

                q3="select * from student where login_id='%s'"%(session['login_id'])
                res3=select(q3)
                student_id=res3[0]['student_id']
                q4="select * from candidate where status='approved' and student_id='%s'"%(student_id)
                res4=select(q4)
                # session['email']=res4[0]['email']

                 

                if res4[0]['status'] != 'pending':
                    session['candidate_id']=res4[0]['candidate_id']

                    t=session['std_id']=res4[0]['student_id']
                    # print("-----------------------",session['email'])

                    return "<script>alert('Candidate login success');window.location='/candidate_home'</script>"
                
                else :
                    return "<script>alert('Candidate login invalid...you are student');window.location='/student_home'</script>"
            
            elif res[0]['usertype']=='pending':
                q5="select * from student where login_id='%s'"%(session['login_id'])
                res3=select(q5)
                if res3:
                    session['student_id']=res3[0]['student_id']
                    return "<script>alert('u are in wait list for election ... so u are still student');window.location='/student_home'</script>"
                else:
                    return "<script>alert(' student login invalid');window.location='/login'</script>"
                

        else:
            return "<script>alert('Invalid username and password');window.location='/login'</script>"  
    return render_template('public/login.html') 