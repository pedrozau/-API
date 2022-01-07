from flask import Flask,request,session,jsonify,redirect,url_for
from flask_bcrypt import Bcrypt
import mysql.connector
app = Flask(__name__)
app.secret_key = "NUDGTDJGDJK/"
bcrypt = Bcrypt(app)

@app.route('/api/v1/')
def api():
     return "Welcome Api/v1/"

# get information about users
@app.route('/api/v1/user/',methods=['GET','POST'])
def user():
    user_name = ""
    user_password = ""
    if request.method == "POST":
        if request.form['user_name'] == "" != request.form['user_password'] == "":
            user_name = request.form['user_name']
            user_password = request.form['user_password']


    elif request.method == "GET":
        if request.args.get('user_name') == "" != request.args.get('user_password') == "":
            user_name = request.args.get('user_name')
            user_password = request.args.get('user_password')


    if user_name == "" and user_password == "":
        return {"msg":"field empty"}
    else:
        new_password = bcrypt.generate_password_hash(user_password,10).decode('utf-8')
        user_insert(str(user_name), new_password)


    return redirect(url_for('notes'))




@app.route('/api/v1/login/',methods=['GET','POST'])
def login():
    if request.method == "POST":
        user_names = request.form['user_name']
        user_passwords = request.form['user_password']
    elif request.method == "GET":
        user_names = request.args.get('user_name')
        user_passwords = request.args.get('user_password')
    conexao = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='flask')
    comand_sql = "SELECT * FROM login WHERE user_name = '{}'".format(user_names);
    cursor = conexao.cursor()
    cursor.execute(comand_sql)
    for id,user_name,user_password in cursor:
        if user_name == user_names:
            if bcrypt.check_password_hash(user_password,user_passwords):

                session['id_user'] = id
                return jsonify({"notes":noteShow(),"user":[{"id":id,"user_name":user_name}]})
            else:
                return {"msg":"senha incorrect"}
        else:
            return {"msg":"usuario não existe"}

    return {"msg":"field empty"}

@app.route('/api/v1/note/',methods=['GET','POST'])
def note():
    try:
        if (session):
            if request.method == "POST":
                titulo = request.form['titulo']
                texto = request.form['texto']
            elif request.method == "GET":
                titulo = request.args.get('titulo')
                texto = request.args.get('texto')
            else:
                return {"msg":"nathing"}

            note_insert(titulo,texto)
            return jsonify({"notas":noteShow()})
    except:

        return redirect(url_for('login'))



@app.route('/api/v1/logout/')
def  logout():
    if (session):
        session.pop("id_user",None)
        redirect(url_for('login'))
    else:
        pass
    return redirect(url_for('login'))
    return {"msg":"logout"}





@app.route('/api/v1/notes/')
def notes():
    try:
        if (session):
            return  jsonify({"notas":noteShow()})
        else:

            redirect(url_for('login'))

    except:
        return redirect(url_for('login'))




def user_insert(user_name,user_password):
    conexao = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='flask')
    cursor = conexao.cursor()
    comand_sql = "INSERT INTO `login` (`id`, `user_name`, `user_password`) VALUES (NULL, %s, %s);"
    datas = []
    datas.append(user_name)
    datas.append(user_password)
    cursor.execute(comand_sql,datas)
    cursor.execute(comand_sql, datas)
    conexao.commit()
def user_show():
    conexao = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='flask')
    comand_sql = "SELECT * FROM login"
    cursor = conexao.cursor()
    cursor.execute(comand_sql)
    data = []
    for id,user_name,user_password in cursor:
        datas = {}
        datas['id'] = id
        datas['user_name'] = user_name
        datas['user_password'] = user_password
        data.append(datas)
    return data


def note_insert(titulo,texto):
    connection = mysql.connector.connect(user='root',password='',host='127.0.0.1',database="flask")
    try:
        if (session):
            data = []
            id_user = session['id_user']
            data.append(id_user)
            data.append(titulo)
            data.append(texto)
            query = "INSERT INTO `note` (`id`, `id_user`, `titulo`, `texto`) VALUES (NULL, %s, %s, %s);"
            cursor = connection.cursor()
            cursor.execute(query,data)
            connection.commit()
            cursor.close()
            connection.close()

            return {"msg":"success"}
    except:

        return redirect(url_for('login'))



def noteShow():
    try:
        if (session):
            id_user = session['id_user']
            conexao = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='flask')
            comand_sql = "SELECT * FROM note WHERE id_user = '{}' ".format(id_user)
            cursor = conexao.cursor()
            cursor.execute(comand_sql)
            data = []
            for id,id_user,titulo,texto in cursor:
                datas = {}
                datas['id'] = id
                datas['id_user'] = id_user
                datas['titulo'] = titulo
                datas['texto'] = texto
                data.append(datas)
            return data
    except:
        return redirect(url_for('login'))

def noteDelete(id):
    connection = mysql.connector.connect(user='root',password='',host='127.0.0.1',database='flask')
    cursor = connction.cursor()
    query_sql = ""
    cursor.execute(query_sql)











if __name__ == "__main__":
    app.run(debug=True)
