import qrcode
from datetime import datetime
import uuid
firma = 'SISTEMA DE INTEGRACION CURRICULAR \n'
firma += 'Cédula: 0401642221.\n'
firma += 'Nombes: Erick Patricio.\n'
firma += 'Apellidos: Josa Narváez.\n'
firma += f'Fecha Generación: {datetime.now()}\n'
firma += 'Universidad Politécnica Estatal del Carchi'
firma += f'http://127.0.0.1:8000/validarFirmaUIAP/{str(uuid.uuid4())}'
img = qrcode.make(firma)
f = open("output.png", "wb")
img.save(f)
f.close()