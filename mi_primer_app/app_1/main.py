import flet as ft
import qrcode
import os
from time import sleep


def main(page: ft.Page):
    def change_status_entry(e):
        email_entry.disabled= False if email_check.value else True
        email_entry.expand=True if email_check.value else False
        telefono_entry.disabled= False if telefono_check.value else True
        telefono_entry.expand= True if telefono_check.value else False
        empresa_entry.disabled= False if empresa_check.value else True
        empresa_entry.expand= True if empresa_check.value else False
        telefono_sec_entry.disabled= False if telefono_sec_check.value else True
        telefono_sec_entry.expand= True if telefono_sec_check.value else False
        cumple_entry.disabled= False if cumple_check.value else True
        cumple_entry.expand= True if cumple_check.value else False
        page.update()

    apellido_check= ft.Checkbox(disabled=True, value=True)
    apellido_entry = ft.TextField(expand=True, border_color="green" if apellido_check.value else "none" , label="Apellido")
    nombre_check= ft.Checkbox(disabled=True, value=True)
    nombre_entry = ft.TextField(expand=True, border_color="green" if apellido_check.value else "none", label="Nombre")
    email_check= ft.Checkbox(value=False, on_change=change_status_entry)
    email_entry = ft.TextField(border_color="green" if apellido_check.value else "none" , disabled=True,label="Email")
    telefono_check= ft.Checkbox(value=False, on_change=change_status_entry)
    telefono_entry = ft.TextField(border_color="green" if apellido_check.value else "none", disabled=True, label="Telefono")
    empresa_check= ft.Checkbox(value=False, on_change=change_status_entry)
    empresa_entry = ft.TextField(border_color="green" if apellido_check.value else "none", disabled=True, label="Empresa")
    telefono_sec_check= ft.Checkbox(value=False, on_change=change_status_entry)
    telefono_sec_entry = ft.TextField(border_color="green" if apellido_check.value else "none", disabled=True, label="Telefono Secundario")
    cumple_check= ft.Checkbox(value=False, on_change=change_status_entry)
    cumple_entry = ft.TextField(border_color="green" if apellido_check.value else "none", disabled=True, label="Cumpleaños")
    resultados_vcard= ft.Text(expand=True)
    resultados_qr= ft.Text(expand=True)
    
    # Lista para almacenar múltiples contactos en formato vCard
    contacts = []
    row1= ft.Row(
        [
            apellido_entry,
            apellido_check,
        ]
    )
    row2= ft.Row(
        [
            nombre_entry,
            nombre_check,
        ]
    )
    row3= ft.Row(
        [
            email_entry,
            email_check,
        ]
    )
    row4= ft.Row(
        [
            telefono_entry,
            telefono_check,
        ]
    )
    row5= ft.Row(
        [
            empresa_entry,
            empresa_check,
        ]
    )
    row6= ft.Row(
        [
            telefono_sec_entry,
            telefono_sec_check,
        ]
    )
    row7= ft.Row(
        [
            cumple_entry,
            cumple_check,
        ]
    )
    def generate_qr(e):
        if (nombre_entry.value!="" and nombre_check.value) and (apellido_entry!="" and apellido_check):
            
            apellido = apellido_entry.value 
            nombre = nombre_entry.value
            email = email_entry.value if email_check.value else ""
            telefono = telefono_entry.value if telefono_check.value else ""
            empresa = empresa_entry.value if empresa_check.value else ""
            telefono_sec = telefono_sec_entry.value if telefono_sec_check.value else ""
            cumple = cumple_entry.value if cumple_check.value else ""
            
            vcard = create_vcard(apellido, nombre, email, telefono, empresa, telefono_sec, cumple)
            contacts.append(vcard)
            
            apellido_entry.value=""
            nombre_entry.value=""
            email_entry.value=""
            telefono_entry.value=""
            empresa_entry.value=""
            telefono_sec_entry.value=""
            cumple_entry.value=""
            resultados_vcard.value=""
            resultados_vcard.value=contacts
            page.update()
        else:
            resultados_vcard.value=""
            resultados_vcard.value="Introduzca minimo el nombre Y apellido y marque las casillas"
            page.update()
            
    
    def create_vcard(apellido, nombre, email, telefono, empresa, telefono_sec, cumple):
        if nombre!="":        
            vcard = f"BEGIN:VCARD\nVERSION:3.0\nN:{apellido};{nombre}\nFN:{nombre} {apellido}\n"
            
            if email:
                vcard += f"EMAIL:{email}\n"

            if telefono:
                vcard += f"TEL:{telefono}\n"

            if telefono_sec:
                vcard += f"TEL:{telefono_sec}\n"

            if empresa:
                vcard += f"ORG:{empresa}\n"

            if cumple:
                vcard += f"BDAY:{cumple}\n"

            vcard += "END:VCARD"
            return vcard
        
    def save_qr_codes(e):
        if len(contacts)>0:
            carpeta = "images"
            ruta = os.path.join(os.getcwd(), carpeta)

            # Comprueba si la carpeta no existe
            if not os.path.exists(ruta):
                # Crea la carpeta
                os.makedirs(ruta)
                
                resultados_qr.value=""
                resultados_qr.value ="QR Codes Saved", f"Se ha ceador exitosamente Carpeta {carpeta}."
                page.update()
                sleep(1.5)
            else:
                resultados_qr.value=""
                resultados_qr.value="La carpeta", ruta, "ya existe"
                page.update()
                sleep(1.5)
            for index, contact in enumerate(contacts):
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(contact)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(f"images/contact_qr_{index}_{contact}.png")




            resultados_qr.value=""
            resultados_qr.value ="QR Codes Saved", f"Se han generado y guardado {len(contacts)} códigos QR."
            page.update()
    def clear_contacts(e):
        contacts.clear()
        resultados_qr.value=""
        resultados_vcard.value=""
        page.update()


        



    page.add(
        row1,
        row2,
        row3,
        row4,
        row5,
        row6,
        row7,
        ft.Row(
            [
                ft.ElevatedButton(
                    "Generar Contacots", 
                    on_click=generate_qr, 
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Gruardar Qr", 
                    on_click=save_qr_codes, 
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Limpiar Contactos", 
                    on_click=clear_contacts, 
                    expand=True,
                ),
            ]
        ),
        ft.Row(
            [
                resultados_vcard,
                resultados_qr,
            ]
        ),
        
        )

    


ft.app(main)
