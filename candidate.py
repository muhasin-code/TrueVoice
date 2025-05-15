from flask import *
from database import *
# from flask_mail import Mail, Message
import random
import string
import smtplib
from email.mime.text import MIMEText


import datetime


import json
from web3 import Web3, HTTPProvider


# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:7545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]
compiled_contract_path = 'C:/Users/rajes/Desktop/final/final/Blockchainvoting/voting/node_modules/.bin/build/contracts/votin.json'
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0xE04D34D9F2d50b982D5AB1Da64fa4E2A5eF397A8'




candidate=Blueprint(__name__,'candidate')




def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


#view all cadidate
@candidate.route('/view_all_candidates',methods=['get','post'])

def view_all_candidates():
    p_id= request.args.get('id')
    student_id=session['std_id']

    data={}
    q0="""select candidate.*,election.election_name ,post.*,student.*,course.* from candidate inner join election on candidate.election_id=election.election_id
     inner join post on candidate.post_id=post.post_id 
     inner join student on candidate.student_id=student.student_id 
     inner join course on student.course_id=course.course_id where candidate.status='approved'and candidate.post_id='%s' """%(p_id)
    data['view']=select(q0)
    print("++++++++++",q0)
    

    q1="select * from vote where student_id='%s' and post_id='%s' "%(student_id,p_id)
    data['views']=select(q1)
    




    if 'action' in request.args:
        action=request.args['action']

        candidate_id = request.args["candidate_id"]  
        # email = request.args["email"]

        election_id=request.args['election_id']
        post_id=request.args['post_id']




    else:
        action=None
    if action=='cotp':


        q3="select * from student inner join candidate using (student_id) where login_id='%s'"%(session['login_id'])
        res3=select(q3)
        if res3:
            session['email']=res3[0]['email']
            print("00000000000000000000000000000000000000000000000",session['email'])



# Generate OTP
        otp = generate_otp()
        print("--------------",otp)

# Send OTP to the user's email
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('projectblockchain2025@gmail.com', 'icrv cqay bqsb clsl')

            msg = MIMEText(f'Your OTP for voting is {otp}')
            msg['Subject'] = 'Your OTP for Voting'
            msg['To'] =session['email']
            msg['From'] = 'projectblockchain2025@gmail.com'

            gmail.send_message(msg)
            gmail.quit()

            flash('An OTP has been sent to your email. Please enter it to complete your registration.')
        except smtplib.SMTPException as e:
            print("Couldn't send email: " + str(e))
            flash("Failed to send OTP. Please try again.")
            return redirect(url_for('candidate.candidate_home'))
         

        # # Temporarily store user details and OTP in session
        session['user_details'] = {
            'candidate_id': candidate_id,
        
            'email': session['email'],
            # 'student_id': student_id,
            'election_id': election_id,
            'post_id': post_id,

        }
        session['otp'] = otp

        return redirect(url_for('candidate.verify_otp',))
    
    return render_template('candidate/view_all_candidates.html',data=data)


@candidate.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():

    student_id=session['std_id']
    if 'verify' in request.form:
        entered_otp = request.form['otp']
        if entered_otp == session.get('otp'):
            shop_details = session.get('user_details')
            if shop_details:
                candidate_id=shop_details['candidate_id'] 
                election_id=shop_details['election_id'] 
                post_id=shop_details['post_id'] 
                print("-------------",post_id)
                d=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(compiled_contract_path) as file:
                    contract_json = json.load(file)  # load contract info as JSON
                    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
                contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
                id=web3.eth.get_block_number()
                message = contract.functions.add_vote(int(id),int(election_id),int(post_id),int(student_id),int(candidate_id),d,'voted').transact()
               
                q2 = "insert into vote values(null, '%s', '%s', '%s', 'completed')" % (student_id, election_id, post_id)
                insert(q2)


        
                flash("verified successfully")

                
            return "<script>alert(' THANK YOU FOR YOUR VOTING .');window.location='candidate_home'</script>"
        else:
            flash('Invalid OTP. Please try again.')

    return render_template('candidate/cotp.html')





@candidate.route('/candidate_home')
def candidate_home():
    return render_template('candidate/candidate_home.html')




#change password
@candidate.route("/cd_change_password",methods=['get','post'])
def cd_change_password():
    login_id=session['login_id']
    if "submit" in request.form:
        password=request.form['password']
        q1="UPDATE login SET password='%s' WHERE login_id='%s'"%(password,login_id)
        update(q1)
        return "<script>alert('password changed');window.location='/cd_change_password';</script>"
    return render_template("candidate/cd_change_password.html")

#view profile 
@candidate.route('/view_profile',methods=['GET','POST'])
def view_profile():
    data={}
    q="select * from candidate inner join student on candidate.student_id=student.student_id  inner join course on student.course_id=course.course_id  where candidate_id='%s'"%(session['candidate_id'])
    data['stud']=select(q)
    return render_template('candidate/view_profile.html',data=data)

#view students
@candidate.route('/view_students',methods=['get','post'])
def manage_student():
    data={}
    q="select *  from student inner  join course on student.course_id=course.course_id "
    q1="select *  from course "
    data ['stud']=select(q)
    data ['cour']=select(q1)

    return render_template('candidate/view_students.html',data=data)

#manage campaigns
@candidate.route('/manage_campaigns',methods=['get','post'])
def manage_campaigns():
     #view data
    data={}
    q="select *  from campaigns "
    data ['view']=select(q)


    #insert  data
    if 'submit' in request.form:
        campaign_name=request.form['campaign_name']
        venue=request.form['venue']
        campaign_date=request.form['campaign_date']


        q2="insert into campaigns values(null,'%s',curdate(),'%s','%s')"%(campaign_name,venue,campaign_date)
        insert(q2)
        return "<script>alert('campaigns added sucessfully');window.location='/manage_campaigns'</script>"
    

#update data
    if 'action' in request.args:
        action=request.args['action']
        campaign_id=request.args['campaign_id']
    else:
        action=None

    if action=='update':
        q1="select * from campaigns where campaign_id='%s'"%(campaign_id)
        res=select(q1)
        data['up']=res
    if 'updates' in request.form:
        campaign_name=request.form['campaign_name']
        venue=request.form['venue']
        campaign_date=request.form['campaign_date']
        q3="update campaigns set campaign_name='%s',venue='%s',campaign_date='%s' where campaign_id='%s'"%(campaign_name,venue,campaign_date,campaign_id)
        update(q3)
        return "<script>alert('campaigns update sucessfully');window.location='manage_campaigns'</script>"  


#delete data
    if action=='delete':
        q4="delete from campaigns where campaign_id='%s'"%(campaign_id)
        delete(q4)
        return"<script>alert('delete sucessfully');window.location='manage_campaigns'</script>"

    return render_template('candidate/manage_campaigns.html',data=data)


#view election
@candidate.route('/cd_view_election',methods=['GET','POST'])
def cd_view_election():
    data={}
    q="select * from election"
    data['view']=select(q)
    return render_template('candidate/cd_view_election.html',data=data)


#view post
@candidate.route('/cd_view_post',methods=['GET','POST'])
def cd_view_post():
    p_id= request.args.get('id')

    data={}
    q="select * from post inner join election on post.election_id=election.election_id where  election.election_id='%s' """%(p_id) 
    data['view']=select(q)
    return render_template('candidate/cd_view_post.html',data=data)



#feedback
@candidate.route('/cd_feedback',methods=['GET','POST'])
def cd_feedback():
       
   
    candidate_id= session['candidate_id']
    data={}

    q1="select * from feedback where id='%s'"%(candidate_id)
    data['view']=select(q1)
    print(data)

    
    if 'submit' in request.form:
        feedback=request.form['feedback']
        q1="insert into feedback values(NULL,'%s',curdate(),'%s','candidate')"%(candidate_id,feedback)
        insert(q1)
        return "<script>alert(' Feedback Send Successfully  ');window.location='cd_feedback'</script>"


    return render_template('candidate/cd_feedback.html',data=data)




#complaints
@candidate.route('/cd_send_complaint',methods=['GET','POST'])
def cd_sent_complaint():
    candidate_id= session['candidate_id']
    data={}
    q1="select * from complaints inner join candidate on candidate.candidate_id=complaints.id  where id='%s'"%(candidate_id)
    
    data['view']=select(q1)
    if 'submit' in request.form:
        complaint=request.form['complaint']
        q="insert into complaints values(NULL,'%s','%s',curdate(),'pending','candidate')"%(candidate_id,complaint)
        insert(q)
        return "<script>alert(' Complaints Send Successfully  ');window.location='cd_send_complaint'</script>"

    return render_template('candidate/cd_send_complaint.html',data=data)






#RESULT
  

@candidate.route('/r_view_election',methods=['GET','POST'])
def r_view_election():
    data={}
    q="select * from election"
    data['view']=select(q)
    return render_template('candidate/r_view_election.html',data=data)


@candidate.route('/r_view_post',methods=['GET','POST'])
def r_view_post():
    p_id= request.args.get('id')

    data={}
    q="select * from post inner join election on post.election_id=election.election_id where  election.election_id='%s' """%(p_id) 
    data['view']=select(q)
    return render_template('candidate/r_view_post.html',data=data)




@candidate.route('/cd_view_result', methods=['GET', 'POST'])
def cd_view_result():
    election_id = request.args.get('election_id')
    post_id = request.args.get('post_id')
    data = {}

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    candidate_votes = {}

    # Initialize variables to prevent UnboundLocalError
    max_candidate = None
    max_votes = 0

    try:
        # Loop through all blocks to collect votes for each candidate
        for i in range(blocknumber, 0, -1):
            a = web3.eth.get_transaction_by_block(i, 0)
            decoded_input = contract.decode_function_input(a['input'])

            # Debug: print decoded input
            print("Decoded input:", decoded_input)

            # Check if the transaction matches the voting function
            if str(decoded_input[0]) == "<Function add_vote(uint256,uint256,uint256,uint256,uint256,string,string)>":
                print("Found matching function call in transaction.")

                # Check if it matches the specified post and election
                if int(decoded_input[1]['post_id']) == int(post_id) and int(decoded_input[1]['election_id']) == int(election_id):
                    candidate_id = decoded_input[1].get('candidate_id')
                    print("candidate_id:", candidate_id)

                    # Count votes for each candidate_id
                    if candidate_id:
                        candidate_votes[candidate_id] = candidate_votes.get(candidate_id, 0) + 1
                        print("Updated candidate_votes:", candidate_votes)

    except Exception as e:
        print("Error:", e)

    # Determine the candidate with the maximum votes after populating candidate_votes
    if candidate_votes:
        print("++++++++++++++++++++++++")
        max_candidate = max(candidate_votes, key=candidate_votes.get)
        max_votes = candidate_votes[max_candidate]
        print("Winner candidate_id:", max_candidate, "with votes:", max_votes)
    else:
        print("No votes found for the specified election and post.")

    # Debug: print the final candidate_votes dictionary
    print("Final candidate_votes dictionary:", candidate_votes)

    # Secure insert using parameterized query
    q = "SELECT * FROM result WHERE result.post_id='%s' AND result.election_id='%s'" % (post_id, election_id)
    res = select(q)
    
    if res:
        result_id = res[0]['result_id']
        qq = "SELECT * FROM `student` INNER JOIN candidate USING (student_id) INNER JOIN `result` USING(candidate_id) INNER JOIN course USING(course_id) WHERE result_id='%s'" % (result_id)
        data['viewsss'] = select(qq)
    else:
        query = "INSERT INTO result (candidate_id, election_id, post_id, result) VALUES (%s, %s, %s, %s)" % (max_candidate, election_id, post_id, max_votes)
        insert(query)
        print("Inserted result into database:", query)

    # Store the winner and all vote counts in the data dictionary
    data['winner'] = max_candidate
    data['max_votes'] = max_votes
    data['candidate_votes'] = candidate_votes
    print("Final winner:", max_candidate)
    print("Vote counts:", candidate_votes)


    return render_template('candidate/cd_view_result.html', data=data)



