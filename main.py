
import tkinter as tk
from tkinter import messagebox, simpledialog
import psycopg2

class Estudiante:
    def __init__(self, estudiante_id, nombre, fecha_nacimiento, carrera):
        self.estudiante_id = estudiante_id
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.carrera = carrera

class Materia:
    def __init__(self, codigo_materia, nombre, creditos):
        self.codigo_materia = codigo_materia
        self.nombre = nombre
        self.creditos = creditos

class Nota:
    def __init__(self, estudiante, materia, nota):
        self.estudiante = estudiante
        self.materia = materia
        self.nota = nota

class VistaBaseDatos:
    def __init__(self, host, port, database, user, password):
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()

    def insert_estudiante(self, estudiante_id, nombre, fecha_nacimiento, carrera):
        try:
            # Verificar si el ID del estudiante ya existe
            self.cursor.execute("SELECT COUNT(*) FROM estudiantes WHERE id_estudiante = %s;", (estudiante_id,))
            count = self.cursor.fetchone()[0]

            if count > 0:
                messagebox.showerror("Error", "El ID del estudiante ya existe.")
                return

            # Insertar el nuevo estudiante perrito
            self.cursor.execute(
                "INSERT INTO estudiantes (id_estudiante, nombre_completo, fecha_nacimiento, carrera) VALUES (%s, %s, %s, %s);",
                (estudiante_id, nombre, fecha_nacimiento, carrera))
            self.connection.commit()
            messagebox.showinfo("Éxito", "Estudiante insertado correctamente.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error al insertar estudiante: {e}")

    def ver_notas_estudiante(self, estudiante_id):
        try:
            self.cursor.execute("SELECT nombre_materia, nota FROM notas INNER JOIN materias ON notas.codigo_materia = materias.codigo_materia WHERE id_estudiante = %s;", (estudiante_id,))
            notas = self.cursor.fetchall()
            if notas:
                nota_str = "\n".join([f"Materia: {materia}, Nota: {nota}" for materia, nota in notas])
                messagebox.showinfo("Notas del estudiante", nota_str)
            else:
                messagebox.showinfo("Notas del estudiante", "El estudiante no tiene notas registradas.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error al obtener notas del estudiante: {e}")

    def promedioNotas(self, estudiante_id):
        try:
            self.cursor.execute("SELECT AVG(nota) FROM notas WHERE id_estudiante = %s GROUP BY id_estudiante;", (estudiante_id,))
            promedio = self.cursor.fetchone()[0]
            if promedio:
                messagebox.showinfo("Promedio de notas", f"Promedio de notas del estudiante: {promedio}")
            else:
                messagebox.showinfo("Promedio de notas", "El estudiante no tiene notas registradas.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error al calcular promedio de notas del estudiante: {e}")

    def eliminar_estudiante(self, estudiante_id):
        try:
            self.cursor.execute("DELETE FROM estudiantes WHERE id_estudiante = %s;", (estudiante_id,))
            self.connection.commit()
            messagebox.showinfo("Éxito", "Estudiante eliminado correctamente.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error al eliminar estudiante: {e}")

    def eliminar_materia(self, codigo_materia):
        try:
            self.cursor.execute("DELETE FROM materias WHERE codigo_materia = %s;", (codigo_materia,))
            self.connection.commit()
            messagebox.showinfo("Éxito", "Materia eliminada correctamente.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error al eliminar materia: {e}")

    def ver_todos_estudiantes(self):
        try:
            self.cursor.execute("SELECT * FROM estudiantes;")
            estudiantes = self.cursor.fetchall()
            if estudiantes:
                estudiantes_str = "\n".join([f"ID: {estudiante[0]}, Nombre: {estudiante[1]}, Fecha de Nacimiento: {estudiante[2]}, Carrera: {estudiante[3]}" for estudiante in estudiantes])
                messagebox.showinfo("Lista de Estudiantes", estudiantes_str)
            else:
                messagebox.showinfo("Lista de Estudiantes", "No hay estudiantes registrados.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error al obtener la lista de estudiantes: {e}")

    def ver_notas_materia(self, codigo_materia):
        try:
            # Obtener el nombre de la materia
            self.cursor.execute("SELECT nombre_materia FROM materias WHERE codigo_materia = %s;", (codigo_materia,))
            nombre_materia = self.cursor.fetchone()

            if nombre_materia:
                nombre_materia = nombre_materia[0]  # El nombre de la materia es el primer elemento de la tupla
                self.cursor.execute(
                    "SELECT nombre_completo, nota FROM notas INNER JOIN estudiantes ON notas.id_estudiante = estudiantes.id_estudiante WHERE codigo_materia = %s;",
                    (codigo_materia,))
                notas = self.cursor.fetchall()
                if notas:
                    notas_str = "\n".join([f"Estudiante: {nota[0]}, Nota: {nota[1]}" for nota in notas])
                    messagebox.showinfo(nombre_materia, notas_str)
                else:
                    messagebox.showinfo(nombre_materia, "No hay notas registradas para esta materia.")
            else:
                messagebox.showinfo("Error", "No se encontró la materia con el código especificado.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error al obtener las notas de la materia: {e}")

    def ver_todas_materias(self):
        try:
            self.cursor.execute("SELECT * FROM materias;")
            materias = self.cursor.fetchall()
            if materias:
                materias_str = "\n".join([f"Código: {materia[0]}, Nombre: {materia[1]}, Créditos: {materia[2]}" for materia in materias])
                messagebox.showinfo("Lista de Materias", materias_str)
            else:
                messagebox.showinfo("Lista de Materias", "No hay materias registradas.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error al obtener la lista de materias: {e}")

    def actualizar(self):
        try:
            self.cursor.execute("SELECT * FROM estudiantes;")
            estudiantes = self.cursor.fetchall()
            if estudiantes:
                estudiantes_str = "\n".join([f"ID: {estudiante[0]}, Nombre: {estudiante[1]}, Fecha de Nacimiento: {estudiante[2]}, Carrera: {estudiante[3]}" for estudiante in estudiantes])
                messagebox.showinfo("Lista de Estudiantes Actualizada", estudiantes_str)
            else:
                messagebox.showinfo("Lista de Estudiantes Actualizada", "No hay estudiantes registrados.")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error al actualizar la lista de estudiantes: {e}")

class Menu(tk.Tk):
    def __init__(self, baseVista):
        super().__init__()
        self.baseVista = baseVista
        self.title("Database Viewer")
        self.crearCositas()

    def crearCositas(self):


        #Vainas para el estudiante si señor
        ver_todos_estudiantes_button = tk.Button(self, text="Lista Estudiantes", command=self.ver_todos_estudiantes)
        ver_todos_estudiantes_button.pack(pady=10)

        insert_button = tk.Button(self, text="Insertar Estudiante", command=self.insert_estudiante)
        insert_button.pack(pady=10)

        eliminar_estudiante_button = tk.Button(self, text="Eliminar Estudiante", command=self.eliminar_estudiante)
        eliminar_estudiante_button.pack(pady=10)

        ver_notas_button = tk.Button(self, text="Notas del Estudiante", command=self.ver_notas)
        ver_notas_button.pack(pady=10)

        promedio_button = tk.Button(self, text="Calcular Promedio", command=self.calcular_promedio)
        promedio_button.pack(pady=10)


        #Vainas de las materias
        ver_todas_materias_button = tk.Button(self, text="Todas las Materias", command=self.ver_todas_materias)
        ver_todas_materias_button.pack(pady=10)

        eliminar_materia_button = tk.Button(self, text="Eliminar Materia", command=self.eliminar_materia)
        eliminar_materia_button.pack(pady=10)

        ver_notas_materia_button = tk.Button(self, text="Notas de una Materia", command=self.ver_notas_materia)
        ver_notas_materia_button.pack(pady=10)


        #Vainas del menú
        update_button = tk.Button(self, text="Actualizar Base de Datos", command=self.actualizarBase)
        update_button.pack(pady=10)

    def actualizarBase(self):
        self.baseVista.actualizar()

    def insert_estudiante(self):
        estudiante_id = simpledialog.askinteger("Insertar Estudiante", "Ingrese el ID del estudiante:")
        if estudiante_id is None:
            return  # Salir si el usuario cancela
        nombre = simpledialog.askstring("Insertar Estudiante", "Ingrese el nombre completo del estudiante:")
        fecha_nacimiento = simpledialog.askstring("Insertar Estudiante",
                                                  "Ingrese la fecha de nacimiento del estudiante (año-mes-dia):")
        carrera = simpledialog.askstring("Insertar Estudiante", "Ingrese la carrera del estudiante:")
        if nombre and fecha_nacimiento and carrera:
            self.baseVista.insert_estudiante(estudiante_id, nombre, fecha_nacimiento, carrera)

    def eliminar_estudiante(self):
        estudiante_id = simpledialog.askinteger("Eliminar Estudiante", "Ingrese el ID del estudiante a eliminar:")
        if estudiante_id:
            self.baseVista.eliminar_estudiante(estudiante_id)

    def eliminar_materia(self):
        codigo_materia = simpledialog.askinteger("Eliminar Materia", "Ingrese el código de la materia a eliminar:")
        if codigo_materia:
            self.baseVista.eliminar_materia(codigo_materia)

    def ver_todos_estudiantes(self):
        self.baseVista.ver_todos_estudiantes()

    def ver_notas_materia(self):
        codigo_materia = simpledialog.askinteger("Notas de una Materia", "Ingrese el código de la materia:")
        if codigo_materia:
            self.baseVista.ver_notas_materia(codigo_materia)

    def ver_todas_materias(self):
        self.baseVista.ver_todas_materias()

    def calcular_promedio(self):
        estudiante_id = simpledialog.askinteger("Calcular Promedio", "Ingrese el ID del estudiante:")
        if estudiante_id:
            self.baseVista.promedioNotas(estudiante_id)

    def ver_notas(self):
        estudiante_id = simpledialog.askinteger("Notas del Estudiante", "Ingrese el ID del estudiante:")
        if estudiante_id:
            self.baseVista.ver_notas_estudiante(estudiante_id)

if __name__ == "__main__":
    # Configuración de la conexión a la base de datos
    host = "localhost"
    port = "5432"
    database = "escuela"
    user = "postgres"
    password = "root"

    # Crear el DatabaseViewer con los datos
    baseVista = VistaBaseDatos(host, port, database, user, password)

    # Crear la aplicación Tkinter
    menu = Menu(baseVista)
    menu.mainloop()
