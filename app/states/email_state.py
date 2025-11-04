import reflex as rx
import os
import logging
import aiosmtplib
from email.message import EmailMessage


class EmailState(rx.State):
    @rx.event(background=True)
    async def send_contact_email(self, form_data: dict):
        """Send a contact email in the background."""
        async with self:
            smtp_host = os.getenv("SMTP_HOST")
            smtp_port = os.getenv("SMTP_PORT")
            smtp_user = os.getenv("SMTP_USER")
            smtp_password = os.getenv("SMTP_PASSWORD")
            if not all([smtp_host, smtp_port, smtp_user, smtp_password]):
                logging.error("SMTP environment variables not set. Email not sent.")
                return
            message = EmailMessage()
            message["From"] = smtp_user
            message["To"] = smtp_user
            message["Subject"] = f"Nuevo Contacto de {form_data.get('name')}"
            body = f"Has recibido un nuevo mensaje de contacto:\n\nNombre: {form_data.get('name')}\nEmail: {form_data.get('email')}\nTeléfono: {form_data.get('phone')}\n\nMensaje:\n{form_data.get('message')}"
            message.set_content(body)
            try:
                await aiosmtplib.send(
                    message,
                    hostname=smtp_host,
                    port=int(smtp_port),
                    username=smtp_user,
                    password=smtp_password,
                    use_tls=True,
                )
                logging.info(f"Contact email sent successfully to {smtp_user}")
            except Exception as e:
                logging.exception(f"Failed to send contact email: {e}")