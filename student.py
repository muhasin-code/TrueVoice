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

import random



student=Blueprint(__name__,'student')


def generate_otps():
    return ''.join(random.choices(string.digits, k=6))


#view all cadidate
@student.route('/a_view_all_candidates',methods=['get','post'])

def a_view_all_candidates():
    p_id= request.args.get('id')
    student_id=session['student_id']

    data={}
    q0="""select candidate.*,election.election_name ,post.*,student.*,course.* from candidate inner join election on candidate.election_id=election.election_id
     inner join post on candidate.post_id=post.post_id 
     inner join student on candidate.student_id=student.student_id 
     inner join course on student.course_id=course.course_id where candidate.status='approved'and candidate.post_id='%s' """%(p_id)
    data['view']=select(q0)
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
    if action=='sotp':
# Generate OTP
        otp = generate_otps()
        print("--------------",otp)

# Send OTP to the user's email
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('projectblockchain2025@gmail.com', 'icrv cqay bqsb clsl')

            msg = MIMEText(f'Your OTP for voting is {otp}')
            msg['Subject'] = 'Your OTP for Voting'
            msg['To'] = session['email']
            print("---------------------",session['email'])
            msg['From'] = 'projectblockchain2025@gmail.com'

            gmail.send_message(msg)
            gmail.quit()

            flash('An OTP has been sent to your email. Please enter it to complete your registration.')
        except smtplib.SMTPException as e:
            print("Couldn't send email: " + str(e))
            flash("Failed to send OTP. Please try again.")
            return redirect(url_for('student.student_home'))
         

        # # Temporarily store user details and OTP in session
        session['user_details'] = {
            'candidate_id': candidate_id,
        
            'email': session['email'],
            # 'student_id': student_id,
            'election_id': election_id,
            'post_id': post_id,

        }
        session['otp'] = otp

        return redirect(url_for('student.sotp',))
    
    return render_template('student/a_view_all_candidates.html',data=data)


@student.route('/sotp', methods=['GET', 'POST'])
def sotp():

    student_id=session['student_id']
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

                
            return "<script>alert(' THANK YOU FOR YOUR VOTING .');window.location='student_home'</script>"
        else:
            flash('Invalid OTP. Please try again.')

    return render_template('student/otps.html')



#Home page
@student.route('/student_home')
def index():
    return render_template('student/student_home.html')



#change password
@student.route("/st_change_password",methods=['get','post'])
def st_change_password():
    login_id=session['login_id']
    if "submit" in request.form:
        password=request.form['password']
        q1="UPDATE login SET password='%s' WHERE login_id='%s'"%(password,login_id)
        update(q1)
        return "<script>alert('password changed sucessfully');window.location='/st_change_password';</script>"
    return render_template("student/st_change_password.html")


#view election
@student.route('/view_election',methods=['GET','POST'])
def view_election():
    data={}
    q="select * from election"
    data['view']=select(q)
    return render_template('student/view_election.html',data=data)

#view post
@student.route('/view_post',methods=['GET','POST'])
def view_post():
    p_id= request.args.get('id')

    data={}
    q="select * from post inner join election on post.election_id=election.election_id where  election.election_id='%s' """%(p_id) 
    data['view']=select(q)
    return render_template('student/view_post.html',data=data)


#view campaigns
@student.route('/st_view_campaigns',methods=['GET','POST'])
def st_view_campaigns():
    data={}
    q="select * from campaigns"
    data['view']=select(q)

    return render_template('student/st_view_campaigns.html',data=data)

#apply as candidate
@student.route('/apply_as_candidate', methods=['GET', 'POST'])
def apply_as_candidate():
    student_id = session['student_id']
    data = {}

    # Fetch available posts and elections
    q0 = "SELECT * FROM post INNER JOIN election WHERE post.election_id = election.election_id"
    q1 = "SELECT * FROM election"

    data['post'] = select(q0)
    data['election'] = select(q1)

    # Insert into the database
    if 'submit' in request.form:
        post_id = request.form['post_id']
        election_id = request.form['election_id']

        # Check if the student has already applied for a post in the selected election
        q_check = "SELECT * FROM candidate WHERE student_id='%s' AND election_id='%s'" % (student_id, election_id)
        existing_application = select(q_check)

        if existing_application:
            # If the student has already applied for a post in this election, show an error
            return "<script>alert('You have already applied for a post in this election. You can only apply for one post per election.');window.location='apply_as_candidate'</script>"

        # Proceed with the application if no existing record is found
        q2 = "UPDATE login SET usertype='pending' WHERE login_id='%s'" % (session['login_id'])
        log_details = insert(q2)

        q3 = "INSERT INTO candidate VALUES (null, '%s', '%s', CURDATE(), 'pending', '%s')" % (student_id, election_id, post_id)
        insert(q3)

        return "<script>alert('Candidate application submitted successfully. Please wait for admin approval.');window.location='apply_as_candidate'</script>"

    if 'action' in request.args:
        action = request.args['action']
        candidate_id = request.args['candidate_id']
    else:
        action = None

    return render_template('student/apply_as_candidate.html', data=data)


#feedback


@student.route('/feedback',methods=['GET','POST'])
def feedback():
       
    student_id= session['student_id']
    data={}
    q1="select * from feedback where id='%s'"%(student_id)
    data['view']=select(q1)
    print(data)

    
    if 'submit' in request.form:
        feedback=request.form['feedback']
        q1="insert into feedback values(NULL,'%s',curdate(),'%s','student')"%(student_id,feedback)
        insert(q1)
        return "<script>alert(' Feedback Send Successfully  ');window.location='feedback'</script>"


    return render_template('student/feedback.html',data=data)
    

#complaints
@student.route('/send_complaint',methods=['GET','POST'])
def cd_sent_complaint():
    student_id= session['student_id']
    data={}
    q1="select * from complaints inner join student on student.student_id=complaints.id  where id='%s'"%(student_id)
    
    data['view']=select(q1)
    if 'submit' in request.form:
        complaint=request.form['complaint']
        q="insert into complaints values(NULL,'%s','%s',curdate(),'pending','student')"%(student_id,complaint)
        insert(q)
        return "<script>alert(' Complaints Send Successfully  ');window.location='send_complaint'</script>"

    return render_template('student/send_complaint.html',data=data)







#RESULT
  

@student.route('/s_view_election',methods=['GET','POST'])
def s_view_election():
    data={}
    q="select * from election"
    data['view']=select(q)
    return render_template('student/s_view_election.html',data=data)


@student.route('/s_view_post',methods=['GET','POST'])
def s_view_post():
    p_id= request.args.get('id')

    data={}
    q="select * from post inner join election on post.election_id=election.election_id where  election.election_id='%s' """%(p_id) 
    data['view']=select(q)
    return render_template('student/s_view_post.html',data=data)





@student.route('/st_view_result', methods=['GET', 'POST'])
def st_view_result():
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



    return render_template('student/st_view_result.html', data=data)



