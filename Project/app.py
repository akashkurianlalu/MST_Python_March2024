from flask import Flask,render_template,request
import mysql.connector

connection=mysql.connector.connect(
    host='localhost',
    user='root',
    password='Akas#795',
    database='project')

mycursor=connection.cursor()
#craete flask application
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pancake_details')
def pancake():
    return render_template('pancake_details.html')

@app.route('/chicken_salad_details')
def chickensalad():
    return render_template('chicken_salad_details.html')

@app.route('/Spaghetti_Bolognese_details')
def SpaghettiBolognese():
    return render_template('Spaghetti_Bolognese_details.html')

@app.route('/chocolate_cake_details')
def chocolatecake():
    return render_template('chocolate_cake_details.html')

@app.route('/submit_details',methods=['GET','POST'])
def submit_details():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        query="insert into users (username,email,password) values (%s,%s,%s)"
        data=(username,email,password)
        mycursor.execute(query,data)
        connection.commit()
        return render_template('submit_details.html')
    return render_template('user_registration.html')

@app.route('/register')
def register():
    return render_template('user_registration.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_home',methods=['GET','POST'])
def login_home():
    if request.method=='POST':
        username = request.form["username"]
        password = request.form["password"]
        query="select * from users where username=%s"
        data=(username,)
        mycursor.execute(query,data)
        user=mycursor.fetchone()
        if user:
            if user[3] == password:
                return render_template('submit_details.html')
            else:
                return render_template('login.html', msg="Incorrect password")
        else:
            return render_template('login.html', msg="Incorrect username")
    return render_template('login.html',msg="Please enter details!!!")

@app.route('/submit_recipe',methods=['GET','POST'])
def submit_recipe():
    if request.method=='POST':
        recipe_name=request.form['recipeName']
        ingredients=request.form['ingredients']
        instructions=request.form['instructions']
        cooking_type=request.form['cookingType']
        serving_size=request.form['servingSize']
        username = request.form['username']
        query = "SELECT user_id FROM users WHERE username=%s"
        data = (username,)
        mycursor.execute(query, data)
        user = mycursor.fetchone()

        if user:
            user_id = user[0]
            query="insert into recipes (recipe_name,ingredients,instructions,cooking_type,serving_size,user_id) values (%s,%s,%s,%s,%s,%s)"
            data=(recipe_name,ingredients,instructions,cooking_type,serving_size,user_id)
            mycursor.execute(query,data)
            connection.commit()
            return render_template('submit.html')
        else:
            return "User not found", 404
    return render_template('submit_details.html')  

@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/goodbye')
def goodbye():
    return render_template('goodbye.html')

@app.route('/view_comment')
def view_comment():
    query="select comment,date_posted from comments"
    mycursor.execute(query)
    data=mycursor.fetchall()
    return render_template('view_comment_page.html',sqldata=data)

@app.route('/search',methods=['GET'])
def search():
    item = request.args.get('itemSearch')
    if item == 'pancake':
        return render_template('pancake_details.html')
    elif item == 'chickensalad':
        return render_template('chicken_salad_details.html')
    elif item == 'chocolatecake':
        return render_template('chocolate_cake_details.html')
    elif item == 'spaghettibolognese':
        return render_template('Spaghetti_Bolognese_details.html')
    else:
        return "Item not found", 404

@app.route('/comm')
def comm():
    return render_template('comment_page.html')

@app.route('/comment_submit',methods=['GET','POST'])
def comment_submit():
    if request.method=='POST':
        comment=request.form['comment']
        date_posted=request.form['date_posted']
        query="insert into comments (comment,date_posted) values(%s,%s)"
        data=(comment,date_posted)
        mycursor.execute(query,data)
        connection.commit()
        return render_template('goodbye.html')
    return render_template('comment_page.html')
    
#run flask application
if __name__ == '__main__':
    app.run(debug=True)