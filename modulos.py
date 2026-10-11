# modulos.py - Funciones del sistema de mesa de partes digital (version 2)
ARCHIVO = "expedientes.txt"


def LimpiarTexto(texto):
    """Quita espacios sobrantes y reemplaza el separador '|' para no romper el archivo."""
    return texto.strip().replace("|", "/")


def ValidarCodigo(codigo):
    """Formato EXP-NNNN (ejemplo: EXP-0001)."""
    return len(codigo) == 8 and codigo.startswith("EXP-") and codigo[4:].isdigit()


def ValidarDocumento(documento):
    """DNI (8 digitos) o RUC (11 digitos)."""
    return documento.isdigit() and len(documento) in (8, 11)


def ValidarFecha(fecha):
    """Formato DD/MM/AAAA con rangos validos."""
    partes = fecha.split("/")
    if len(partes) != 3:
        return False
    dia, mes, anio = partes
    if not (dia.isdigit() and mes.isdigit() and anio.isdigit()):
        return False
    if len(dia) != 2 or len(mes) != 2 or len(anio) != 4:
        return False
    dia, mes, anio = int(dia), int(mes), int(anio)
    dias_mes = [31, 29 if (anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)) else 28,
                31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return 1 <= mes <= 12 and 1 <= dia <= dias_mes[mes - 1]


def PedirTextoObligatorio(mensaje):
    texto = LimpiarTexto(input(mensaje))
    while texto == "":
        print("Este dato no puede estar vacio.")
        texto = LimpiarTexto(input(mensaje))
    return texto


def SeleccionarTramite():
    print("\n===== TIPO DE TRAMITE =====")
    print("1. Solicitud administrativa")
    print("2. Licencia o autorizacion")
    print("3. Certificado o constancia")
    print("4. Reclamo o queja")
    print("5. Recurso administrativo")
    print("6. Acceso a la informacion publica")
    print("7. Otros")

    opcion = input("Seleccione el tipo de tramite: ").strip()

    if opcion == "1":
        return "Solicitud administrativa"
    elif opcion == "2":
        return "Licencia o autorizacion"
    elif opcion == "3":
        return "Certificado o constancia"
    elif opcion == "4":
        return "Reclamo o queja"
    elif opcion == "5":
        return "Recurso administrativo"
    elif opcion == "6":
        return "Acceso a la informacion publica"
    elif opcion == "7":
        return "Otros"
    else:
        print("Opcion no valida. Se registrara como Otros.")
        return "Otros"


def RegistrarExpediente(codigos, nombres, documentos, tramites, descripciones, fechas, areas):
    codigo = input("Codigo del expediente (formato EXP-0001): ").strip().upper()
    while not ValidarCodigo(codigo) or codigo in codigos:
        if not ValidarCodigo(codigo):
            print("Codigo invalido. Use el formato EXP-0001.")
        else:
            print("Ese codigo ya esta registrado.")
        codigo = input("Codigo del expediente (formato EXP-0001): ").strip().upper()

    nombre = PedirTextoObligatorio("Nombre del ciudadano: ")

    documento = input("Documento de identidad (DNI 8 digitos o RUC 11): ").strip()
    while not ValidarDocumento(documento):
        print("Documento invalido. Debe tener 8 digitos (DNI) o 11 digitos (RUC).")
        documento = input("Documento de identidad (DNI 8 digitos o RUC 11): ").strip()

    tramite = SeleccionarTramite()
    descripcion = PedirTextoObligatorio("Descripcion: ")

    fecha = input("Fecha de recepcion (DD/MM/AAAA): ").strip()
    while not ValidarFecha(fecha):
        print("Fecha invalida. Use el formato DD/MM/AAAA con una fecha real.")
        fecha = input("Fecha de recepcion (DD/MM/AAAA): ").strip()

    area = PedirTextoObligatorio("Area responsable: ")

    codigos.append(codigo)
    nombres.append(nombre)
    documentos.append(documento)
    tramites.append(tramite)
    descripciones.append(descripcion)
    fechas.append(fecha)
    areas.append(area)

    print("Expediente registrado correctamente.")


def ConsultarExpediente(codigos, nombres, documentos, tramites, descripciones, fechas, areas):
    codigo_buscar = input("Ingrese el codigo del expediente: ").strip().upper()
    encontrado = False

    for i in range(len(codigos)):
        if codigos[i] == codigo_buscar:
            print("\n===== EXPEDIENTE ENCONTRADO =====")
            print(f"Codigo: {codigos[i]}")
            print(f"Ciudadano: {nombres[i]}")
            print(f"Documento: {documentos[i]}")
            print(f"Tipo de tramite: {tramites[i]}")
            print(f"Descripcion: {descripciones[i]}")
            print(f"Fecha: {fechas[i]}")
            print(f"Area responsable: {areas[i]}")
            encontrado = True
            break

    if not encontrado:
        print("No se encontro el expediente.")


def MostrarListado(codigos, nombres, tramites, fechas):
    print("\nCODIGO     CIUDADANO                 TRAMITE                          FECHA")
    for i in range(len(codigos)):
        print(f"{codigos[i]:<10} {nombres[i]:<25} {tramites[i]:<32} {fechas[i]}")


def OrdenarExpediente(codigos, nombres, documentos, tramites, descripciones, fechas, areas):
    if len(codigos) < 2:
        print("No hay suficientes expedientes para ordenar.")
        return
    print("Ordenando los expedientes por codigo...")
    n = len(codigos)
    # Ordenamiento burbuja sobre arreglos paralelos
    for i in range(n):
        for j in range(0, n - i - 1):
            if codigos[j] > codigos[j + 1]:
                codigos[j], codigos[j + 1] = codigos[j + 1], codigos[j]
                nombres[j], nombres[j + 1] = nombres[j + 1], nombres[j]
                documentos[j], documentos[j + 1] = documentos[j + 1], documentos[j]
                tramites[j], tramites[j + 1] = tramites[j + 1], tramites[j]
                descripciones[j], descripciones[j + 1] = descripciones[j + 1], descripciones[j]
                fechas[j], fechas[j + 1] = fechas[j + 1], fechas[j]
                areas[j], areas[j + 1] = areas[j + 1], areas[j]
    print("Expedientes ordenados correctamente.")
    MostrarListado(codigos, nombres, tramites, fechas)


def GuardarInformacion(codigos, nombres, documentos, tramites, descripciones, fechas, areas):
    print("Guardando informacion...")
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        for i in range(len(codigos)):
            linea = (f"{codigos[i]}|{nombres[i]}|{documentos[i]}|{tramites[i]}|"
                     f"{descripciones[i]}|{fechas[i]}|{areas[i]}\n")
            archivo.write(linea)
    print(f"Datos guardados en el archivo '{ARCHIVO}'. Total: {len(codigos)} expediente(s).")


def CargarInformacion(codigos, nombres, documentos, tramites, descripciones, fechas, areas):
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                campos = linea.strip().split("|")
                if len(campos) == 7:
                    codigos.append(campos[0])
                    nombres.append(campos[1])
                    documentos.append(campos[2])
                    tramites.append(campos[3])
                    descripciones.append(campos[4])
                    fechas.append(campos[5])
                    areas.append(campos[6])
        print(f"Se cargaron {len(codigos)} expediente(s) desde '{ARCHIVO}'.")
    except FileNotFoundError:
        print("No existe un archivo previo. Se inicia con el registro vacio.")
