import pandas as pd
import matplotlib.pyplot as plt


# Funciones de validación
def ingresarEntero(etiqueta):
    numero = 0
    while (True):
        try:
            print(etiqueta)
            numero = int(input())
        except:
            print("Sucedio un error en el ingreso de datos, reintente nuevamente")
        else:
            break
    return numero


def ingresarFloatPositivo(etiqueta):
    numero = 0.0
    while (True):
        try:
            print(etiqueta)
            numero = float(input())
        except:
            print("Sucedio un error en el ingreso de datos, reintente nuevamente")
        else:
            if (numero >= 0):
                break
    return numero


def ingresarEnteroEntreRangos(etiqueta, inferior, superior):
    numero = 0
    while (True):
        numero = ingresarEntero(etiqueta)
        if (numero >= inferior and numero <= superior):
            break
    return numero


def ingresarCadenaNoVacia(etiqueta):
    cadena = ""
    while (True):
        try:
            print(etiqueta)
            cadena = input()
        except:
            print("Sucedio un error en el ingreso de datos, reintente nuevamente")
        else:
            if (cadena != ""):
                break
    return cadena


def ingresarCaracterValidado(etiqueta, valores):
    caracter = ""
    while (True):
        try:
            print(etiqueta)
            caracter = input()
        except:
            print("Sucedio un error en el ingreso de datos, reintente nuevamente")
        else:
            if (valores.find(caracter) != -1):
                break
    return caracter


# Entidad Calificacion
class Calificacion:
    codigo = ""
    nombre = ""
    parcial = 0.0
    final = 0.0

    def __init__(self, codigo, nombre, parcial, final):
        self.codigo = codigo
        self.nombre = nombre
        self.parcial = parcial
        self.final = final

    def notaFinal(self):
        return (self.parcial + self.final) / 2

    def condicion(self):
        return "Aprobado" if (self.notaFinal() >= 13) else "Desaprobado"

    def asDataRow(self):
        return [self.codigo, self.nombre, self.parcial, self.final, self.notaFinal(), self.condicion()]


class AdmCalificaciones:
    dfCalificaciones = None
    nombreArchivoExcel = ""

    def __init__(self, nombreArchivoExcel):
        self.dfCalificaciones = pd.read_excel(nombreArchivoExcel, sheet_name="Notas")
        self.nombreArchivoExcel = nombreArchivoExcel

    def listarCalificaciones(self):
        print(self.dfCalificaciones)

    def existeCalificacion(self, codigo):
        subDataFrame = self.dfCalificaciones.loc[self.dfCalificaciones["Codigo"] == codigo]
        return subDataFrame.empty == False

    def registrarCalificacion(self, calificacion):
        # Usar loc para añadir elementos al final del DataFrame
        self.dfCalificaciones.loc[self.dfCalificaciones.shape[0]] = calificacion.asDataRow()
        self.dfCalificaciones.to_excel(self.nombreArchivoExcel, sheet_name='Notas', index=False)

    def mostrarEstadisticas(self):
        print("Estadisticas del Examen Parcial")
        # print("Nota Mayor: ", self.dfCalificaciones["Parcial"].max())
        # print("Nota Menor: ", self.dfCalificaciones["Parcial"].min())
        print(self.dfCalificaciones["Parcial"].describe())
        print("Estadisticas del Examen Final")
        # print("Nota Mayor: ", self.dfCalificaciones["Final"].max())
        # print("Nota Menor: ", self.dfCalificaciones["Final"].min())
        print(self.dfCalificaciones["Final"].describe())
        print("Estadisticas de la Nota Final")
        # print("Nota Mayor: ", self.dfCalificaciones["NotaFinal"].max())
        # print("Nota Menor: ", self.dfCalificaciones["NotaFinal"].min())
        print(self.dfCalificaciones["NotaFinal"].describe())
        print("Estadisticas Condicion")
        dfCondicion = self.dfCalificaciones.groupby(["Condicion"])
        print(dfCondicion["Condicion"].count())
        # Pie
        y = dfCondicion["Condicion"].count().tolist()
        etiquetas = dfCondicion["Condicion"].count().keys().tolist()
        plt.pie(y, labels=etiquetas)
        plt.legend(title="Nota Final")
        plt.show()
        # Histograma
        notasFinales = self.dfCalificaciones["NotaFinal"].tolist()
        plt.hist(notasFinales)
        plt.show()


class Sistema:
    admCalificaciones = None

    def __init__(self):
        self.admCalificaciones = AdmCalificaciones("NotasAlumnos.xlsx")

    def menu(self):
        print("Sistema de Calificaciones")
        print("[1] Registrar Calificación")
        print("[2] Listar Calificaciones")
        print("[3] Mostrar Estadísticas")
        print("[4] Salir")
        opcion = ingresarEnteroEntreRangos("Ingrese su opción: ", 1, 4)
        return opcion

    def ingresarCalificacion(self):
        print("Ingreso de Calificación")
        print("----------------------\n")
        codigo = ingresarCadenaNoVacia("Codigo Alumno: ")
        if (self.admCalificaciones.existeCalificacion(codigo) == False):
            nombre = ingresarCadenaNoVacia("Nombre Alumno: ")
            parcial = ingresarFloatPositivo("Examen Parcial: ")
            final = ingresarFloatPositivo("Examen Final: ")
            calificacion = Calificacion(codigo, nombre, parcial, final)
            self.admCalificaciones.registrarCalificacion(calificacion)
        else:
            print("Codigo duplicado!")

    def listarCalificaciones(self):
        self.admCalificaciones.listarCalificaciones()

    def mostrarEstadisticas(self):
        self.admCalificaciones.mostrarEstadisticas()


# Programa Principal
sistema = Sistema()
while (True):
    opcion = sistema.menu();
    if (opcion == 1):
        sistema.ingresarCalificacion()
    elif (opcion == 2):
        sistema.listarCalificaciones()
    elif (opcion == 3):
        sistema.mostrarEstadisticas()
    else:
        break
