import reflex as rx
from app.app import header, footer
from app.states.services_state import ServicesState
from app.components.service_card import service_card


def servicios() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.section(
            rx.el.div(
                rx.el.h1(
                    "Nuestros Servicios Detallados",
                    class_name="text-4xl md:text-5xl font-extrabold text-gray-900 mb-4 text-center",
                ),
                rx.el.p(
                    "Explora la gama completa de soluciones que ofrecemos para mantener tus equipos en perfecto estado.",
                    class_name="text-lg text-gray-600 mb-12 max-w-3xl mx-auto text-center",
                ),
                rx.el.div(
                    rx.foreach(ServicesState.services, service_card),
                    class_name="grid md:grid-cols-2 lg:grid-cols-3 gap-8",
                ),
                class_name="container mx-auto py-20 px-4",
            ),
            class_name="bg-gray-50",
        ),
        rx.el.div(footer(), id="asistencia-remota"),
        class_name="font-['Poppins'] bg-white",
    )