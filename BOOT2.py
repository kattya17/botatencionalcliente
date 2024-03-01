import telebot
from telebot import types

bot = telebot.TeleBot('6026419634:AAEvcoolbAZTLACdIE7ofsHSfCx2I_YTZVQ')

@bot.message_handler(commands=["help", "start"])
def enviar(message):
    markup = generar_markup_preguntas()
    bot.reply_to(message, "Hola, ¿en qué puedo ayudarte?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    pregunta = call.data
    if pregunta in preguntas_con_subpreguntas:
        subpreguntas = preguntas_con_subpreguntas[pregunta]
        if subpreguntas:
            markup = generar_markup_subpreguntas(subpreguntas)
            bot.send_message(call.message.chat.id, "Elige una subpregunta:", reply_markup=markup)
        else:
            respuesta = obtener_respuesta(pregunta)
            bot.send_message(call.message.chat.id, respuesta)
    else:
        respuesta = obtener_respuesta(pregunta)
        bot.send_message(call.message.chat.id, respuesta)

@bot.callback_query_handler(func=lambda call: True, regexp="subpregunta_.*")
def subpregunta_callback_handler(call):
    subpregunta = call.data.replace("subpregunta_", "")
    respuesta = obtener_respuesta_subpregunta(subpregunta)
    bot.send_message(call.message.chat.id, respuesta)

def generar_markup_preguntas():
    preguntas = [
        "Requisitos",
        "¿Cuáles son las últimas promociones?",
        "¿Información sobre servicio FTTH?",
        "Cobertura",
        "Quiero dar de baja mi servicio",
        "Costos",
        "Planes",
        "Cambio de Domicilio",
        "Cambio de plan",
        "Cambio de equipo",
        "Servicio Técnico",
        "No hay señal",
        "¿Cómo restablecer la contraseña de mi cuenta?",
        "¿Cómo puedo resguardar mi red Wi-Fi?",
        "¿A qué se refiere con INTERNET SATELITAL?",
        " ¿Por qué mi servicio de televisión no tiene canales locales?"

    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    botones = [types.InlineKeyboardButton(pregunta, callback_data=pregunta) for pregunta in preguntas]
    markup.add(*botones)
    return markup

def generar_markup_subpreguntas(subpreguntas):
    markup = types.InlineKeyboardMarkup(row_width=1)
    botones = [types.InlineKeyboardButton(subpregunta["subpregunta"], callback_data="subpregunta_" + subpregunta["subpregunta"]) for subpregunta in subpreguntas]
    markup.add(*botones)
    return markup

def obtener_respuesta(pregunta):
    preguntas_frecuentes = {
        "Requisitos": "Fotocopia de tu documento de identidad, Fotocopia de factura de agua, luz, gas o teléfono Una de estas referencias financieras: + Certificado de trabajo o última papeleta de pago + Extracto bancario de tu cuenta de ahorro o cuenta corriente + Formulario de Impuestos (400IT/200IVA)",
        "¿Información sobre servicio FTTH?": "El servicio FTTH es una tecnología de conexión de fibra óptica que ofrece alta velocidad y estabilidad.",
        "Cobertura": "Por favor, ingresa la fecha y hora para verificar la cobertura.",
        "Quiero dar de baja mi servicio": "Para dar de baja tu servicio, debes llevar todos los equipos entregados el día de instalación a Multicentro, junto a su Carnet Identidad. ",
        "Costos": "Los costos varían según el plan y los servicios adicionales. Te recomendamos revisar nuestra página web para obtener información detallada.",
        "Planes": "Ofrecemos diferentes planes que se adaptan a diferentes necesidades. Puedes obtener más información en nuestra página web o contactando a nuestro equipo de ventas.",
        "Cambio de Domicilio": "Para solicitar un cambio de domicilio, comunícate con nuestro equipo de atención al cliente.800101010",
        "Cambio de plan": "Puedes cambiar tu plan contactando a nuestro equipo de atención al cliente. Ellos te proporcionarán información sobre el nuevo monto.",
        "Cambio de equipo": "Para solicitar un cambio de equipo, comunícate con nuestro equipo de atención al cliente.",
        "Servicio Técnico": "Si tienes problemas con tu servicio, por favor, comunícate con nuestro equipo de servicio técnico.",
        "No hay señal": "Si no tienes señal, te recomendamos verificar la conexión de tu equipo y reiniciarlo. Si el problema persiste, comunícate con nuestro equipo de atención al cliente.",
        "¿Cómo restablecer la contraseña de mi cuenta?": "Puedes restablecer la contraseña de tu cuenta siguiendo los siguientes pasos: ROUTER ZTE MODELO ZXHN-F660Cambiar contraseña de la red inalámbrica (WiFi) 1.    Ingresar en una página de navegador la dirección: 192.168.1.1 2.    Colocar nombre de usuario y contraseña: Username: user Password: user 3.    Seleccionar Network. 4.    Seleccionar Security. 5.    En el campo WPA Passphrase escribir la nueva contraseña. 6.    Click en el botón Submit, para guardar el cambio. ",
        "¿Cómo puedo resguardar mi red Wi-Fi?": "Para resguardar tu red Wi-Fi, te recomendamos cambiar la contraseña periódicamente y utilizar una contraseña segura. Además, puedes activar la encriptación WPA2 para mayor seguridad.",
        "¿A qué se refiere con INTERNET SATELITAL?": "Entel cuenta con internet a través de conectividad satelital, brindando la posibilidad de acceder a la red global desde cualquier zona geográfica del país.",
        " ¿Por qué mi servicio de televisión no tiene canales locales?": "Estimado usuario, respecto a su consulta de programación de canales locales, indicarle que el contenido que se emite es de proveedores de canal que decidieron entrar a la grilla de Entel, en casos que no se emita programación de la región, se debe a que el proveedor decidió no ser parte de nuestra grilla. agradecemos su comprensión"
    }

    if pregunta in preguntas_con_subpreguntas:
       # return "Elige una subpregunta:"
       return respuestas_subpreguntas[subpregunta]

    elif pregunta in preguntas_frecuentes:
        return preguntas_frecuentes[pregunta]
    else:
        return "Mas consultas: https://www.entel.bo/HogarInternetFibra"

def obtener_respuesta_subpregunta(subpregunta):
    

    if subpregunta in respuestas_con_subpreguntas:
        return respuestas_subpreguntas[subpregunta]
    else:
        return "Mas consultas: https://www.entel.bo/HogarInternetFibra"

preguntas_con_subpreguntas = {
    "¿Cuáles son las últimas promociones?": [
        {
            "subpregunta": "DESCUENTO PAGO X 3 MESES",
            "respuesta": "Del 17 de abril al 17 de julio, paga por adelantado tus planes de Internet Fibra y Fibra Empresas y recibe un incremento en la velocidad además de un descuento por tu pago adelantado, consulta mas: https://www.entel.bo/PromocionesVigentesInternet"
        },
        {
            "subpregunta": "DESCUENTO PAGO X 3 MESES",
            "respuesta": "Respuesta a la subpregunta 2"
        },
        {
            "subpregunta": "DESCUENTO PAGO X 3 MESES",
            "respuesta": "Respuesta a la subpregunta 3"
        }
    ],
    "Planes": [
        {
            "subpregunta": "FIBRA 15",
            "respuesta": "Respuesta a la subpregunta 1"
        },
        {
            "subpregunta": "FIBRA 30",
            "respuesta": "Respuesta a la subpregunta 2"
        },
        {
            "subpregunta": "FIBRA 65",
            "respuesta": "Respuesta a la subpregunta 3"
        },
        {
            "subpregunta": "FIBRA 105",
            "respuesta": "Respuesta a la subpregunta 4"
        },
        {
            "subpregunta": "FIBRA 150",
            "respuesta": "Respuesta a la subpregunta 5"
        },
        {
            "subpregunta": "FIBRA 170",
            "respuesta": "Respuesta a la subpregunta 6"
        }
    ]
}

bot.polling()
