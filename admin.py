from flask import *
from database import *
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

admin=Blueprint(__name__,'admin')



@admin.route('/admin_home')
def index():
    return render_template('admin/admin_home.html')


#change password
@admin.route("/ad_change_password",methods=['get','post'])
def ad_change_password():
    login_id=session['admin_id']
    if "submit" in request.form:
        password=request.form['password']
        q1="UPDATE login SET password='%s' WHERE login_id='%s'"%(password,login_id)
        update(q1)
        return "<script>alert('password changed');window.location='/ad_change_password';</script>"
    return render_template("admin/ad_change_password.html")



#manage course
@admin.route('/manage_course', methods=['GET', 'POST'])
def manage_course():
    # Display data
    data = {}
    q0 = "SELECT * FROM course"
    data['view'] = select(q0)

    # Insert data
    if 'submit' in request.form:
        course_name = request.form['course_name']
        
        # Check for duplicate course name
        q_check = "SELECT * FROM course WHERE course_name='%s'" % (course_name)
        existing_course = select(q_check)
        
        if existing_course:
            return "<script>alert('Course  already added!');window.location='/manage_course'</script>"
        else:
            q2 = "INSERT INTO course VALUES (NULL, '%s')" % (course_name)
            insert(q2)
            return "<script>alert('Course added successfully');window.location='/manage_course'</script>"

    # Update data
    if 'action' in request.args:
        action = request.args['action']
        course_id = request.args['course_id']
    else:
        action = None

    if action == 'update':
        q1 = "SELECT * FROM course WHERE course_id='%s'" % (course_id)
        res = select(q1)
        data['up'] = res
        
    if 'updates' in request.form:
        course_name = request.form['course_name']
        q3 = "UPDATE course SET course_name='%s' WHERE course_id='%s'" % (course_name, course_id)
        update(q3)
        return "<script>alert('Course updated successfully');window.location='/manage_course'</script>"
    #delete data
    if action=='delete':
        q4="delete from course where course_id='%s'"%(course_id)
        delete(q4)
        return"<script>alert('delete sucessfully');window.location='manage_course'</script>"

    return render_template('admin/manage_course.html',data=data)
   
#delete data
    # if action=='delete':
    #     q4="delete from course where course_id='%s'"%(course_id)
    #     delete(q4)
    #     return"<script>alert('delete sucessfully');window.location='manage_course'</script>"

    # return render_template('admin/manage_course.html',data=data)
    
#manage student
    
@admin.route('/manage_student',methods=['get','post'])
def manage_student():
    data={}
    q="""select *  from student inner  join course on student.course_id=course.course_id 
      inner join login on student.login_id=login.login_id"""
    q1="select *  from course "
    data ['stud']=select(q)
    data ['cour']=select(q1)
#insert into database
    if 'submit' in request.form:
        username=request.form['username']
        password=request.form['dob']
        course_id=request.form['course_id']
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        email=request.form['email']
        phone=request.form['phone']
        gender=request.form['gender']
        dob=request.form['dob']
        house_name=request.form['house_name']
        place=request.form['place']
        pincode=request.form['pincode']
        

        q2="insert into login values(null,'%s','%s','student')"%(username,password)
        log_details=insert(q2)


        q3="insert into student values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(log_details,course_id,first_name,last_name,email,phone,gender,dob,house_name,place,pincode)
        insert(q3)
        return"<script>alert('student added  sucessfully');window.location='manage_student'</script>"
    
    if 'action' in request.args:
        action=request.args['action']
        student_id=request.args['student_id']
    else:
        action=None


    if action=="update":
        q2="select * from student inner join course on student.course_id = course.course_id where  student_id='%s'"%(student_id)
        data['up']=select(q2)

    #update data
    if 'updates' in request.form:
        course_id=request.form['course_id']
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        email=request.form['email']
        phone=request.form['phone']
        gender=request.form['gender']
        dob=request.form['dob']
        house_name=request.form['house_name']
        place=request.form['place']
        pincode=request.form['pincode']

        q3="update student set course_id='%s',first_name='%s',last_name='%s',email='%s',phone='%s',gender='%s',dob='%s',house_name='%s',place='%s',pincode='%s' where student_id='%s'"%(course_id,first_name,last_name,email,phone,gender,dob,house_name,place,pincode,student_id)
        update(q3)
        return "<script>alert('student update sucessfully');window.location='manage_student'</script>"
   
    
   # delete data
    if action=='delete':
        q4="delete from student where student_id='%s'"%(student_id)
        delete(q4)
        return"<script>alert('delete sucessfully');window.location='manage_student'</script>"

    return render_template('admin/manage_student.html',data=data)

# manage post

@admin.route('/manage_post',methods=['get','post'])
def manage_post():
#display data
    data={}
    q0="select * from post inner join election where post.election_id=election.election_id"
    q1="select *  from election "

    data['view']=select(q0)
    data ['election']=select(q1)


    #insert  data
    if 'submit' in request.form:
        election_id=request.form['election']     
        post_name=request.form['post_name']

        print(election_id)
        print(post_name)

        q2="insert into post values(null,'%s',curdate(),'%s')"%(post_name,election_id)
        insert(q2)
        return "<script>alert('post added sucessfully');window.location='/manage_post'</script>"
#update data
    if 'action' in request.args:
        action=request.args['action']
        post_id=request.args['post_id']
    else:
        action=None

    if action=='update':
        q1="select * from post inner join election on post.election_id=election.election_id where post_id='%s'"%(post_id)
        res=select(q1)
        data['up']=res

    if 'updates' in request.form:
        election_id=request.form['election_id']
        post_name=request.form['post_name']

        q3="update post set election_id='%s', post_name='%s' where post_id='%s'"%(election_id,post_name,post_id)
        update(q3)
        return "<script>alert('post update sucessfully');window.location='manage_post'</script>"  

   # delete data
    if action=='delete':
        q4="delete from post where post_id='%s'"%(post_id)
        delete(q4)
        return"<script>alert('delete sucessfully');window.location='manage_post'</script>"
  
        
    return render_template('admin/manage_post.html',data=data)


# manage election

@admin.route('/manage_election',methods=['get','post'])
def manage_election():
#display data
    data={}
    q0="select * from election"
    data['view']=select(q0)

    #insert  data
    if 'submit' in request.form:
        election_name=request.form['election_name']
        date=request.form['date']
        enddate=request.form['enddate']

        venue=request.form['venue']

        q2="insert into election values(null,'%s','%s','%s','%s','pending')"%(election_name,date,enddate,venue)
        insert(q2)
        return "<script>alert('election added sucessfully');window.location='/manage_election'</script>"
#update data
    if 'action' in request.args:
        action=request.args['action']
        election_id=request.args['election_id']
    else:
        action=None

    if action=='update':
        q1="select * from election where election_id='%s'"%(election_id)
        res=select(q1)
        data['up']=res
    if 'updates' in request.form:
        election_name=request.form['election_name']
        date=request.form['date']
        venue=request.form['venue']


        q3="update election set election_name='%s',date='%s',venue='%s' where election_id='%s'"%(election_name,date,venue,election_id)
        update(q3)
        return "<script>alert('election update sucessfully');window.location='manage_election'</script>"  
    
    if 'action' in request.args:
        action=request.args['action']
        election_id=request.args['election_id']
    else:
        action=None  
    if action=="start":
        q7="update election set status='start' where election_id='%s'"%(election_id)
        update(q7)
        return "<script>alert('Election Start Successfully');window.location='/manage_election'</script>"
    
    if action=="completed":
        q7="update election set status='completed' where election_id='%s'"%(election_id)
        update(q7)
        return "<script>alert('Election Stop Successfully');window.location='/manage_election'</script>"
  
  

    # delete data
    if action=='delete':
        q4="delete from election where election_id='%s'"%(election_id)
        delete(q4)
        return"<script>alert('delete sucessfully');window.location='manage_election'</script>"
  
        
    return render_template('admin/manage_election.html',data=data)


@admin.route('/view_candidates',methods=['get','post'])
def view_candidates():
    # student_id=session['student_id']

#display data
    data={}
    q0='''select candidate.*,election.election_name ,post.*,student.*,course.* from candidate inner join election on candidate.election_id=election.election_id
     inner join post on candidate.post_id=post.post_id 
     inner join student on candidate.student_id=student.student_id 
     inner join course on student.course_id=course.course_id'''
    
    data['view']=select(q0)
#delete data
    if 'action' in request.args:
        action=request.args['action']
        student_id=request.args['student_id']
    else:
        action=None


    if action=='approve':
        qq1="select * from student where student_id='%s'"%(student_id)
        res=select(qq1)
        std_log_id=res[0]['login_id']
        q6="update login set usertype='candidate' where login_id='%s'"%(std_log_id)
        update(q6)
        q7="update candidate set status='approved' where student_id='%s'"%(student_id)
        update(q7)
        return "<script>alert('Approved Successfully');window.location='/view_candidates'</script>"
  

    if action=="reject":
        qq1="select * from student where student_id='%s'"%(student_id)
        res=select(qq1)
        stds_log_id=res[0]['login_id']
        q10="update login set usertype='student' where login_id='%s'"%(stds_log_id)
        rr=update(q10)
        print(rr)

        q9="update candidate set status='rejected' where student_id='%s'"%(student_id)
        rrr=update(q9)
        print(rrr)
        
        
        return "<script>alert('Rejected');window.location='/view_candidates'</script>"
    
    return render_template('admin/view_candidate.html',data=data)


@admin.route('/view_verified_candidate',methods=['get','post'])

def view_verified_candidate():
    data={}
    q0='''select candidate.*,election.election_name ,post.*,student.*,course.* from candidate inner join election on candidate.election_id=election.election_id
     inner join post on candidate.post_id=post.post_id 
     inner join student on candidate.student_id=student.student_id 
     inner join course on student.course_id=course.course_id where candidate.status='approved' '''
    data['view']=select(q0)
    return render_template('admin/view_verified_candidate.html',data=data)


   













#view complaints
@admin.route('/view_complaints',methods=['GET','POST'])
def view_complaints():
    data={}
    
    q = """
    SELECT complaints.*, 
           CASE 
               WHEN complaints.usertype = 'student' THEN student.first_name 
               WHEN complaints.usertype = 'candidate' THEN s2.first_name 
           END AS name,
           complaints.usertype
    FROM complaints
    LEFT JOIN student ON complaints.id = student.student_id
    LEFT JOIN candidate ON complaints.id = candidate.candidate_id
    LEFT JOIN student AS s2 ON candidate.student_id = s2.student_id
    """
    data['view']=select(q)
    return render_template('admin/view_complaints.html',data=data)

@admin.route('/send_reply',methods=['GET','POST'])
def sent_reply():
    complaint_id=request.args['id']
    if 'submit' in request.form:
        reply=request.form['reply']
        q="update complaints set reply='%s' where complaint_id='%s'"%(reply,complaint_id)
        update(q)
        return "<script>alert('Replied successfully');window.location='/view_complaints'</script>"
    return render_template('admin/send_reply.html')
#feedback
@admin.route('/view_feedback',methods=['GET','POST'])
def view_feedback():
    data={}
    
    q = """
    SELECT feedback.*, 
           CASE 
               WHEN feedback.usertype = 'student' THEN student.first_name 
               WHEN feedback.usertype = 'candidate' THEN s2.first_name 
           END AS name,
           feedback.usertype
    FROM feedback
    LEFT JOIN student ON feedback.id = student.student_id
    LEFT JOIN candidate ON feedback.id = candidate.candidate_id
    LEFT JOIN student AS s2 ON candidate.student_id = s2.student_id
    """
    data['view']=select(q)
    return render_template('admin/view_feedback.html',data=data)


 #campaigns
@admin.route('/view_campaigns',methods=['GET','POST'])
def view_campaigns():
    data={}
    q="select * from campaigns"
    data['view']=select(q)
    if 'action' in request.args:
        action=request.args['action']
        campaign_id=request.args['campaign_id']
    else:
        action=None

    if action=='delete':
        q4="delete from campaigns where campaign_id='%s'"%(campaign_id)
        delete(q4)
        return"<script>alert('delete sucessfully');window.location='view_campaigns'</script>"
  
        
    return render_template('admin/view_campaigns.html',data=data)









#RESULT
  

@admin.route('/a_view_election',methods=['GET','POST'])
def a_view_election():
    data={}
    q="select * from election"
    data['view']=select(q)
    return render_template('admin/a_view_election.html',data=data)


@admin.route('/a_view_post',methods=['GET','POST'])
def a_view_post():
    p_id= request.args.get('id')

    data={}
    q="select * from post inner join election on post.election_id=election.election_id where  election.election_id='%s' """%(p_id) 
    data['view']=select(q)
    return render_template('admin/a_view_post.html',data=data)





# @admin.route('/view_result', methods=['GET', 'POST'])
# def view_result():
#     election_id = request.args.get('election_id')
#     post_id = request.args.get('post_id')
#     data = {}

#     with open(compiled_contract_path) as file:
#         contract_json = json.load(file)
#         contract_abi = contract_json['abi']
#     contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
#     blocknumber = web3.eth.get_block_number()
#     candidate_votes = {}

#     try:
#         # Loop through all blocks to collect votes for each candidate
#         for i in range(blocknumber, 0, -1):
#             a = web3.eth.get_transaction_by_block(i, 0)
#             decoded_input = contract.decode_function_input(a['input'])

#             # Debug: print decoded input
#             print("Decoded input:", decoded_input)

#             # Check if the transaction matches the voting function
#             if str(decoded_input[0]) == "<Function add_vote(uint256,uint256,uint256,uint256,uint256,string,string)>":
#                 print("Found matching function call in transaction.")

#                 # Check if it matches the specified post and election
#                 if int(decoded_input[1]['post_id']) == int(post_id) and int(decoded_input[1]['election_id']) == int(election_id):
#                     candidate_id = decoded_input[1].get('candidate_id')
#                     print("candidate_id:", candidate_id)

#                     # Count votes for each candidate_id
#                     if candidate_id:
#                         candidate_votes[candidate_id] = candidate_votes.get(candidate_id, 0) + 1
#                         print("Updated candidate_votes:", candidate_votes)


#     except Exception as e:
#         print("Error:", e)
#         max_candidate = None
#         max_votes = 0


#         print("+++ddddddddddddddddddddddddddddddddd+++++++++++++++++++++")


#         # Determine the candidate with the maximum votes after populating candidate_votes
#         if candidate_votes:
#             print("++++++++++++++++++++++++")
#             max_candidate = max(candidate_votes, key=candidate_votes.get)
#             max_votes = candidate_votes[max_candidate]
#             print("Winner candidate_id:", max_candidate, "with votes:", max_votes)
#         else:
#             max_candidate = None
#             max_votes = 0
#             print("No votes found for the specified election and post.")

#         # Debug: print the final candidate_votes dictionary
#         print("Final candidate_votes dictionary:", candidate_votes)

#         # Secure insert using parameterized query
#         q="select * from result  where result.post_id='%s' and  result.election_id='%s'"%(post_id,election_id)
#         res=select(q)
#         if res:
#             result_id=res[0]['result_id']
#             qq=" SELECT * FROM `student` INNER JOIN candidate USING (student_id) INNER JOIN `result` USING(candidate_id) inner join course using(course_id) where result_id='%s'  "%(result_id)

#             data['viewsss']=select(qq)
#         else:

#             query = "INSERT INTO result (candidate_id, election_id, post_id, result) VALUES (%s, %s, %s, %s)"%(max_candidate, election_id, post_id, max_votes)
#             insert(query)
#             print("Inserted result into database:", query)



#     # Store the winner and all vote counts in the data dictionary
#     data['winner'] = max_candidate
#     data['max_votes'] = max_votes
#     data['candidate_votes'] = candidate_votes
#     print("Final winner:", max_candidate)
#     print("Vote counts:", candidate_votes)



#     return render_template('admin/view_result.html', data=data)



@admin.route('/view_result', methods=['GET', 'POST'])
def view_result():
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

    return render_template('admin/view_result.html', data=data)
