import openpyxl
from datetime import datetime
from hic.main.models import Paciente
from hic.paciente.models import HistoriaClinica


def process_file(file, sheet):
    work_box = openpyxl.load_workbook(file)
    excel_data = list()
    work_sheet = work_box[sheet]
    max_col = 13
    if sheet == "LISTADO":
        max_col = 13
    for row in work_sheet.iter_rows(max_col=max_col):
        row_data = list()
        for cell in row:
            if cell:
                row_data.append(str(cell.value).strip())
            else:
                row_data.append(None)
        excel_data.append(row_data)
    return excel_data


def validate_file_extension(filename):
    return filename.endswith('.xlsx')


def process_data(data):
    for row in data:
        process_row(row=row)
    return True


def process_row(row):
    # print(row)
    try:
        row_folio = row[0]
        row_nombre = row[1]
        row_fecha_ingresp =  "1960-01-01 12:00:00" if row[2] is None else row[2]
        try:
            new_date = datetime.strptime(row_fecha_ingresp, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            new_date =  "1960-01-01"

        row_nombre_mama = row[3]
        row_telefono_mama = row[4]
        row_nombre_papa = row[5]
        row_telefono_papa = row[6]

        fecha_array = row[7].split(" ")
        fecha_str = "{}-{}-{}".format(fecha_array[3],get_month(fecha_array[0]), fecha_array[1])
        print(fecha_str)
        # fecha = "1960-01-01 12:00:00" if row[7] is None else row[7]
        try:
            nac = datetime.strptime(fecha_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except Exception as e:
            print(e)
            nac = "1960-01-01"
        print(nac)

        row_fecha_nac = nac
        row_diagnostico = row[8]
        row_medico_tratante = row[9]
        row_servicio_solicitado = row[10]
        row_observaciones_final = row[11]
        row_estado = row[12]

        """Create paciente"""
        paciente = Paciente()
        split_nombre = row_nombre.split(" ")
        paciente.nombre = split_nombre[0]
        paciente.primer_apellido = split_nombre[1]
        paciente.segundo_apellido = split_nombre[2]
        paciente.fecha_nacimiento = row_fecha_nac
        paciente.estado = row_estado
        paciente.save()

        """Create historic"""
        hic = HistoriaClinica()
        hic.folio = row_folio
        hic.paciente = paciente
        hic.fecha = new_date
        hic.nombre_madre = row_nombre_mama
        hic.ocupacion_madre = ""
        hic.telefono_madre = row_telefono_mama
        hic.nombre_padre = row_nombre_papa
        hic.ocupacion_padre = ""
        hic.telefono_padre = row_telefono_papa
        hic.estado_civil = ""
        hic.escolaridad_menor = ""
        hic.nombre_colegio = ""
        hic.grado_cursa = ""
        hic.diagnostico_medico = row_diagnostico
        hic.observaciones_generales = row_observaciones_final
        hic.remitido_por = row_medico_tratante
        hic.servicio_solicitado = row_servicio_solicitado
        hic.profesional_cargo = row_medico_tratante

        hic.save()
    except Exception as e:
        print(e)
        return  False

    return True

def get_month(month):
    if month == "ENERO": return "01"
    if month == "FEBRERO": return "02"
    if month == "MARZO": return "03"
    if month == "ABRIL": return "04"
    if month == "MAYO": return "05"
    if month == "JUNIO": return "06"
    if month == "JULIO": return "07"
    if month == "AGOSTO": return "08"
    if month == "SEPTIEMBRE": return "09"
    if month == "OCTUBRE": return "10"
    if month == "NOVIEMBRE": return "11"
    if month == "DICIEMBRE": return "12"