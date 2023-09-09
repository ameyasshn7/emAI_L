#importing required libraries
from flask import Flask,render_template, request,redirect,url_for,jsonify
import google.generativeai as palm
import json

#setting up global variables
app = Flask(__name__)
API_KEY = 'YOUR_API_KEY'
palm.configure(api_key = API_KEY)
text = ""
user_responses = {}

questions = [
    {
        'question': 'What is your Campaign Goal?',
        'choices': 
            
        ['Convince Users to buy your Product',           
        'Recover Churned Customers', 
        ' Onboard and Welcome New Users',
        'Share Product Updates'],
        
    },
    
    {
        'question' : 'What kind of Brand Tone would you like for your message?',
        'choices' : ['Formal','Informal']
    }     
]

#defining routes and functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_id = len(user_responses) + 1
    business_model = request.form['business_model']  # Get the selected business model
    user_response = {
        'business_model' : business_model,
    }
    for idx, question in enumerate(questions):
        selected_choice = int(request.form['q{}'.format(idx + 1)])
        user_response[question['question']] = question['choices'][selected_choice]
        
    # user_responses.append(user_response)
    text_input_key = "addText"
    user_response[text_input_key] = request.form.get(text_input_key, '')
    user_responses['user_id'] = user_response
    
    
    
    
    return redirect(url_for('display_responses'))


@app.route('/responses')
def display_responses():
    BUSINESSMODEL = request.form.get('business_model','') # Get the selected business model
    PURPOSE = request.form.get('q1', '') #get purpose
    TONE = request.form.get('q2', '') #get tone of the required prompt
    ADDTEXT = request.form.get('addText', '') #get additional text added by user
    
    
    output = []
    
    prompt  = f'''
    Generate emails tailored to my clients. 
    I am the owner of a {BUSINESSMODEL} agency. 
    I want the tone of the emails to be "{TONE}" to effectively communicate with my audience. 
    The main purpose of these emails is to {PURPOSE}. 
    Additionally, include the following information about my business: {ADDTEXT}. 
    Please ensure that my email is distinct and resonates well with the target audience. 
    The content must be authentic and relevant.
    '''

    
    for i in range(5):
        response = palm.generate_text(prompt=prompt)
        output.append(response.result)
    
    
    
    return render_template('responses.html', generated_text  = output)
    

    
    
if __name__ == '__main__':
    app.run(debug=True)
