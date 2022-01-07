from flask import Flask, render_template,url_for,request,redirect,session
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.secret_key = "NGUIMBIY//%&$/="

bcrypt = Bcrypt(app)


pw_hash = bcrypt.generate_password_hash('nguimbi',10).decode('utf-8')



@app.route('/')


def index():


   return render_template('index.html')


@app.route('/upload/',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.form['arquivo'] 
        f.save('./upload')

    return render_template('upload.html',file=f)

    




@app.route('/login/',methods=['GET','POST'])
def login():


   if request.method == 'POST':


      user_name = request.form['user'] 

      user_pass = request.form['password'] 


      if user_name == "Pedro" and bcrypt.check_password_hash(pw_hash, user_pass):
         session['id_user'] = 1
         return redirect(url_for('home'))

      return "!!"




@app.route('/home/')
def home():
    """
    try:
        if session['id_user']:

            return "Bem vindo"

    except KeyError:
        return redirect(url_for('index'))
    """ 
    if session:
        return f" Bem vindo id_user: {session['id_user']}"
    return redirect(url_for('index'))

    

    


@app.route('/sair/')
def sair():
    session.pop('id_user',None)
    return redirect(url_for('index'))
                



if __name__ == "__main__":


    app.run(debug=True)


