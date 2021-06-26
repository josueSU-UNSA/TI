"""Archivo que arrancara la aplicacion"""
from flask import Flask,render_template,request,redirect,url_for,flash#el render template es para que pueda renderizar una plantilla

#el url_for nos sirve para poder dar una url y poder redireccionar
#el redirect nos sirve para hacer en si la redireccion
#flash nos permite poder mandar mensajes entre vistas

from flask_mysqldb import MySQL#importaremos el modulo para conectar a mysql


app=Flask(__name__)#necesitaremos para poder ejecutar el servidor

#MYSQL connection
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='flaskcontacts'

mysql=MySQL(app)#ejecutamos el modulo ,creando un objeto para guardarla en una variable mysql
#poniendo el app estamos enviando la configuracion del mysql

#Inicilizaremos una sesion
#una sesion son datos que guarda nuestra aplicacion de servidor para luego reutilizarlos
#lo guardaremos en la memoria de la aplicacion
#configuraciones
app.secret_key='mysecretkey'


@app.route('/')#nos enviara algo cada vez que entremos a nuestra pagina principal para evitar el not Found
def Index():
    #haremos esta consulta para enviar los datos en el tbody del html ya que esta funcion es la que redirecciona al index
    cur=mysql.connection.cursor()
    cur.execute('SELECT *FROM horarios')#hacemos la consutla sql para traer todos los datos
    data=cur.fetchall()#con esto se ejecuta la consulta almacenado en una variable data
    
    #recordar que esto se ejecuta cada vez que aparece la parte incial

    return render_template('index.html',horarios=data)#enviara esta imagen, renderizara el formulario
    #el horarios=data es para poder mandar al html las tuplas creadas
@app.route('/add_contact',methods=['POST'])
def add_contact():# empezaremos a guardar datos
    if request.method=='POST':
        curso=request.form['curso']#guardamos en una variable lo recibido desde el form
        dia=request.form['dia']#recibimos cada dato guardandolos en una variable
        hora_inicio=request.form['hora_inicio']
        hora_final=request.form['hora_final']
        profesor=request.form['profesor']
        grupo=request.form['grupo']
        cur=mysql.connection.cursor()#esta parte para saber donde esta el cursor de la conexion mysql almacenado en una variable
        #el cur nos permitira hacer ejecutar las consultas de mysql
        cur.execute('INSERT INTO horarios(curso,dia,hora_inicio,hora_final,profesor,grupo) VALUES(%s,%s,%s,%s,%s,%s)',(curso,dia,hora_inicio,hora_final,profesor,grupo))
        mysql.connection.commit()#aqui ejecutamos la consulta
        flash("Curso Agregado")
        return redirect(url_for('Index'))#nos redirecciona otra vez al html incial esto despues de hacer la consulta
        
@app.route('/edit/<id>')
def get_contact(id):#solo obtendremos un contacto para poder modificarlo
    cur= mysql.connection.cursor()
    cur.execute('SELECT *FROM horarios WHERE id= %s',(id))#mediante el id haremos la ejecucion de sql para traer esa fila 
    data=cur.fetchall()#me traera el arreglo de la fila del id respectivo
    return render_template('edit_curso.html',horario=data[0])
    """print(data[0])#esto para que me entregue una dupla pura y no una dentro de otra
    return 'recibido'"""
@app.route('/update/<id>',methods=['POST'])
def update_horario(id):
    if request.method=='POST':

        curso=request.form['curso']#guardamos en una variable lo recibido desde el form
        dia=request.form['dia']#recibimos cada dato guardandolos en una variable
        hora_inicio=request.form['hora_inicio']
        hora_final=request.form['hora_final']
        profesor=request.form['profesor']
        grupo=request.form['grupo']

        cur=mysql.connection.cursor()
        cur.execute("""
        UPDATE horarios 
        SET curso=%s,
            dia=%s,
            hora_inicio=%s,
            hora_final=%s,
            profesor=%s,
            grupo=%s
        WHERE id=%s
        """,(curso,dia,hora_inicio,hora_final,profesor,grupo,id))        
        mysql.connection.commit()
        flash('Curso modificado ')
        return redirect(url_for('Index'))
@app.route('/delete/<string:id>')#el string id porque esa es la condicion que pusimos para poder hacer el delete en una fila
def delete_contact(id):
    #pasaremos el id por una consulta sql para eliminar este id
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM horarios WHERE id={}'.format(id))#el format nos sirve para poder remplazar en la instruccion sql el id
    mysql.connection.commit()#se ejecuto la consulta
    flash('Curso eliminado del horario')  
    return redirect(url_for('Index'))

if __name__=='__main__':#si el archivo que se esta ejecutando es el main es decir el app.py entonces arranca el servidor
    app.run(port=3000,debug=True)#corre el servidor