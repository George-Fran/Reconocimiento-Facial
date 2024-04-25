#Primero que nada importamos las librerias necesarios en este caso opencv os para leer archivos face y tkinter para la interfaz grafica claro tambien podria ser por la consola pero se mira mejor
import cv2
import os
import face_recognition
from tkinter import Tk, Button, filedialog, Label, simpledialog, messagebox


# Primer paso agregamos una función para cargar una imagen desde un archivo

def cargar_imagen():
    ruta_imagen = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
    if ruta_imagen:
        analizar_imagen(ruta_imagen)

# Segundo paso agregamos una función para analizar la imagen seleccionada
def analizar_imagen(ruta_imagen):
    imagen = cv2.imread(ruta_imagen)
    
    # Aseguramos que la imagen se este leyendo correctamente
    if imagen is None:
        #Retorna una ventana si no lee bien
        messagebox.showerror("Error al leer la imagen.")
        return
    
    # Convertir la imagen a RGB si fuera necesario hacerlo
    if len(imagen.shape) == 3 and imagen.shape[2] == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    # Segun la imagen detectamos si exite uno o mas rostros
    faces = face_recognition.face_locations(imagen)
    
    # Aseguramos que se haya detectado al menos un rostro en la imagen seleccionada revisando la longitud de la lista faces
    for (top, right, bottom, left) in faces:
        face = imagen[top:bottom, left:right]
        # Codificamos el rostro
        rostroCodigoImagen = face_recognition.face_encodings(face, known_face_locations=[(0, right - left, bottom - top, 0)])[0]
        # Comparamos los rostros con los que tenemos en nuestra lista de rostros guardado en este caso en la carpeta faces
        result = face_recognition.compare_faces(rostrosCodigos, rostroCodigoImagen)
        
        # Si el resultado es true nos mandara el nombre de la persona encontrada en la imagen y un color positivo

        if True in result:
            index = result.index(True)
            name = rostrosNombres[index]
            color = (88, 180, 217)
        # En todo caso retorne false retornamos el nombre como "Desconocido" y un color rojo
        else:
            name = "Desconocido"
            color = (255, 0, 0)
            
        # Dibujamos el rectangulo que se visualizar en el rostro de la imagen

        cv2.rectangle(imagen, (left, top), (right, bottom), color, 2)
        # Creamos un cuadro de texto para mostrar el nombre de la persona encontrada dentro de la imagen
        cv2.putText(imagen, name, (left, bottom + 25), 2, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Convertir de nuevo a BGR antes de mostrar(Este paso es importante ya que si lo quitamos el rostro de la persona tomara un tono de piel color pitufo)
    imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)

    # Mostramos la imagen dentro de una ventana con una funcion de la biblioteca de cv2
    cv2.imshow("Imagen Analizada", imagen)
    # Si el usuario oprime cualqier tecla se cierra la ventana
    cv2.waitKey(0)
    # Cerramos la ventana
    cv2.destroyAllWindows()

# Tercer Paso agregamos la funcion para detectar rostro por la camara
def usar_camara():
    # Establecemos el indice de la camara que usaremos en este caso la 0 la cual vendria a ser la principal en todo caso no funcione cambia el 0 por 1 2 3 cualquiera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # Establecemos el clasificador de rostros que usaremos en este caso usaremos el que da por defecto opencv
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    # Creamos un bucle infinito para que la camara se mantenga hasta que el usuario la cierre con esc
    while True:
        # Leemos la camara
        ret, frame = cap.read()
        # Si no se logra leer bien se cerrara
        if ret == False:
            break
        # Volteamos la imagen sino se mirara al revez
        frame = cv2.flip(frame, 1)
        orig = frame.copy()
        faces = faceClassif.detectMultiScale(frame, 1.1, 5)
        
        # Aseguramos que se haya detectado al menos un rostro en la imagen seleccionada revisando la longitud de nuestra lista faces
        for (x, y, w, h) in faces:
            face = orig[y:y + h, x:x + w]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            # Codificamos el rostro que nos dara la camara pueden ver varios no hay problema solo es un poco lento
            rostroCodigoCamara = face_recognition.face_encodings(face, known_face_locations=[(0, w, h, 0)])[0]
            # Comparamos los rostros que detecta la camara con los que tenemos guardados
            result = face_recognition.compare_faces(rostrosCodigos, rostroCodigoCamara)
            
            # Si el resultado es True nos mandar el nombre de el rostro encontrado y un color positivo
            if True in result:
                index = result.index(True)
                name = rostrosNombres[index]
                color = (88, 180, 217)
            # En todo caso sea False ns mandara que el rostro es "Desconocido" y un color rojo
            else:
                name = "Desconocido"
                color = (255, 0, 0)
                
            # Dibujamos un rectangulo en el rostro encontrado
            cv2.rectangle(frame, (x, y + h), (x + w, y + h + 30), color, -1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            # Creamos un cuadro de texto para mostrar el nombre de la persona encontrada dentro de la imagen
            cv2.putText(frame, name, (x, y + h + 25), 2, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
        # Mostramos la imagen dentro de una ventana con una funcion de la biblioteca de cv2 
        cv2.imshow("Camara", frame)
        # Si el usuario oprime la tecla ESC se cerrara la ventana
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    # Cerramos la ventana
    cap.release()
    cv2.destroyAllWindows()

# Cuarto paso creamos la funcion para agregar y codificar rostros
def agregar_rostro():
    # Abrir una ventana para seleccionar la imagen
    ruta_imagen = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
    if ruta_imagen:
        # Leemos la imagen y detectar el rostro
        imagen = cv2.imread(ruta_imagen)
        face_locations = face_recognition.face_locations(imagen)

        # Aseguramos si se detecto un rostro en la imagen
        if len(face_locations) == 1:
            top, right, bottom, left = face_locations[0]
            rostro = imagen[top:bottom, left:right]

            # Codificamos el rostro y guardamos en nuestra carpeta faces
            rostro_codigo = face_recognition.face_encodings(rostro, known_face_locations=[(0, right - left, bottom - top, 0)])[0]
            
            # Obteneemos el nombre del rostro abriendo una ventana de dialogo
            rostro_nombre = simpledialog.askstring("RecoFace", "Ingrese el nombre de la persona:")

            # Verificamos que el usauario haya ingresado un nombre
            if rostro_nombre:
                rostrosCodigos.append(rostro_codigo)
                rostrosNombres.append(rostro_nombre)
                cv2.imwrite(os.path.join(carpetaRostros, rostro_nombre + ".jpg"), rostro)
                messagebox.showinfo("RecoFace",f"Rostro {rostro_nombre} agregado correctamente")
            # Si el usuario cancela el proceso no se guarda nada
            else:
                messagebox.showwarning("RecoFace", "Operacion cancelada por el usuario")
        # Si no se detecta un rostro en la imagen se mostrara como error
        else:
            messagebox.showerror("Error", "No se detecto un rostro en la imagen")
        
# Codificamos los rostros y especificamos la carpeta de rostros " puedes cambiarla por la que quieras"
carpetaRostros = "D:/PROYECTOS/FaceReco/images/faces"
rostrosCodigos = []
rostrosNombres = []

# Recorrer la carpeta de rostros y codificar cada rostro

for file_name in os.listdir(carpetaRostros):
    image_path = os.path.join(carpetaRostros, file_name)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detectamos el rostro en la imagen
    face_locations = face_recognition.face_locations(image)

    # Nos aseguramos que se detecte un solo rostro en la imagen
    if len(face_locations) == 1:
        top, right, bottom, left = face_locations[0]
        face = image[top:bottom, left:right]

        # Codificamos el rostro que nos pasaron y lo agregamos a la lista
        rostro_codigo = face_recognition.face_encodings(face, known_face_locations=[(0, right - left, bottom - top, 0)])[0]
        rostrosCodigos.append(rostro_codigo)
        rostrosNombres.append(file_name.split(".")[0])
    # Si no se detecta un solo rostro en la imagen se mostrara como error
    else:
        print(f"Error: No se detectó un solo rostro en la imagen {image_path}.")


# Creamos la interfas grafica, esto no es necesario se podria hacer mediante la consola pero igual
# Creamos la ventana
ventana = Tk()
# Damos titulo a nuestra ventana
ventana.title("RecoFace")

# Configurar dimensiones y posiciones de nuestra ventana tanto ancho como alto
ancho_ventana = 400
alto_ventana = 300

# Obtenemos las dimensiones de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Calculamos la posicion para centrar las ventanas
posicion_x = (ancho_pantalla - ancho_ventana) // 2
posicion_y = (alto_pantalla - alto_ventana) // 2

# Configuramos la posicion y dimensiones de la ventana
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

# Cambiamos el color de la ventana HEXACODE
ventana.configure(bg="#e0e0e0")

# Agregamos un titulo dentro de la ventana lo otro fue el titulo de la ventana
label_titulo = Label(ventana, text="RecoFace: Tu identidad, tu llave.", font=("Helvetica", 14), bg="#e0e0e0")
# Le pasamos un padding para que no este tan cerca de los botones
label_titulo.pack(pady=10)

# Crear una caja para contener los botones y no se separen
caja = Label(ventana, bg="#e0e0e0")
caja.pack(expand=True)

# Colocamos los botones dentro de la caja

# Creamos los botones y le pasamos los funciones que al dar click se ejecute la funcion usar_Camara dentro del command
btn_camara = Button(caja, text="Usar Cámara", command=usar_camara, font=("Helvetica", 12), padx=20, pady=10, borderwidth=0)
# Le pasamos un padding para que no esten tan cerca cada boton de uno
btn_camara.grid(row=0, column=0, pady=(10, 5))

# Creamos el boton Cargar Imagen y le pasamos los funcion que al dar click se ejecute la funcion cargar_imagen dentro del command
btn_imagen = Button(caja, text="Cargar Imagen", command=cargar_imagen, font=("Helvetica", 12), padx=20, pady=10, borderwidth=0)
# Le pasamos un padding para que no esten tan cerca cada boton de uno
btn_imagen.grid(row=1, column=0, pady=5)

# Creamos el boton Agregar Rostro y le pasamos los funcion que al dar click se ejecute la funcion agregar_rostro dentro del command
btn_agregar_rostro = Button(caja, text="Agregar Rostro", command=agregar_rostro, font=("Helvetica", 12), padx=20, pady=10, borderwidth=0)
# Le pasamos un padding para que no esten tan cerca cada boton de uno
btn_agregar_rostro.grid(row=2, column=0, pady=5)

# Iniciamos el bucle principal y eso seria todo
ventana.mainloop()
