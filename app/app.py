import reflex as rx
from app.states.state import State


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon("computer", class_name="h-8 w-8 text-orange-500"),
                rx.el.span("Juanca PC", class_name="text-2xl font-bold text-gray-800"),
                class_name="flex items-center gap-3",
            ),
            rx.el.nav(
                rx.el.a(
                    "Inicio",
                    href="/",
                    class_name="text-gray-600 hover:text-orange-500 transition-colors",
                ),
                rx.el.a(
                    "Servicios",
                    href="/servicios",
                    class_name="text-gray-600 hover:text-orange-500 transition-colors",
                ),
                rx.el.a(
                    "Reseñas",
                    href="#reseñas",
                    class_name="text-gray-600 hover:text-orange-500 transition-colors",
                ),
                rx.el.a(
                    "Contacto",
                    href="#contacto",
                    class_name="text-gray-600 hover:text-orange-500 transition-colors",
                ),
                class_name="flex items-center gap-6 text-md font-medium",
            ),
            class_name="container mx-auto flex items-center justify-between p-4",
        ),
        class_name="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50",
    )


def hero_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h1(
                "Reparación Profesional de Computadoras",
                class_name="text-4xl md:text-5xl font-extrabold text-gray-900 mb-4",
            ),
            rx.el.p(
                "Soluciones rápidas y confiables para tus equipos, tanto en línea como en nuestro local.",
                class_name="text-lg text-gray-600 mb-8 max-w-2xl",
            ),
            rx.el.a(
                rx.el.button(
                    "Contáctanos Ahora",
                    rx.icon("arrow-right", class_name="ml-2"),
                    class_name="bg-orange-500 text-white px-8 py-3 rounded-lg font-semibold text-lg shadow-md hover:bg-orange-600 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1",
                ),
                href="#contacto",
            ),
            class_name="text-center flex flex-col items-center py-20 px-4",
        ),
        class_name="bg-gray-50",
    )


def services_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Nuestros Servicios",
                class_name="text-3xl font-bold text-center text-gray-800 mb-12",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "monitor-smartphone",
                        class_name="h-12 w-12 text-orange-500 mb-4",
                    ),
                    rx.el.h3(
                        "Reparación Local",
                        class_name="text-xl font-semibold text-gray-800 mb-2",
                    ),
                    rx.el.p(
                        "Visítanos para un diagnóstico y reparación experta de tu equipo.",
                        class_name="text-gray-600 text-center",
                    ),
                    class_name="bg-white p-8 rounded-xl shadow-sm hover:shadow-xl transition-shadow duration-300 flex flex-col items-center",
                ),
                rx.el.div(
                    rx.icon("cloud-cog", class_name="h-12 w-12 text-orange-500 mb-4"),
                    rx.el.h3(
                        "Asistencia Online",
                        class_name="text-xl font-semibold text-gray-800 mb-2",
                    ),
                    rx.el.p(
                        "Soporte remoto para problemas de software y configuraciones.",
                        class_name="text-gray-600 text-center",
                    ),
                    class_name="bg-white p-8 rounded-xl shadow-sm hover:shadow-xl transition-shadow duration-300 flex flex-col items-center",
                ),
                class_name="grid md:grid-cols-2 gap-8",
            ),
            id="servicios",
            class_name="container mx-auto py-16 px-4",
        )
    )


def about_us_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Sobre Nosotros",
                class_name="text-3xl font-bold text-center text-gray-800 mb-8",
            ),
            rx.el.p(
                "Somos un equipo de técnicos apasionados por la tecnología, dedicados a ofrecer soluciones efectivas y transparentes. Con años de experiencia en el sector, garantizamos un servicio de calidad y la satisfacción de nuestros clientes.",
                class_name="max-w-3xl mx-auto text-center text-gray-600 leading-relaxed",
            ),
            class_name="container mx-auto py-16 px-4",
        ),
        class_name="bg-gray-50",
    )


def contact_form() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Formulario de Contacto",
                class_name="text-3xl font-bold text-center text-gray-800 mb-8",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.input(
                        placeholder="Nombre",
                        name="name",
                        class_name="w-full p-3 rounded-md border border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-transparent transition",
                    ),
                    rx.el.input(
                        placeholder="Email",
                        name="email",
                        type="email",
                        class_name="w-full p-3 rounded-md border border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-transparent transition",
                    ),
                    rx.el.input(
                        placeholder="Teléfono",
                        name="phone",
                        class_name="w-full p-3 rounded-md border border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-transparent transition",
                    ),
                    rx.el.textarea(
                        placeholder="Mensaje",
                        name="message",
                        class_name="w-full p-3 rounded-md border border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-transparent transition",
                        rows=5,
                    ),
                    rx.el.button(
                        "Enviar Mensaje",
                        type="submit",
                        class_name="w-full bg-orange-500 text-white p-4 rounded-lg font-semibold shadow-md hover:bg-orange-600 hover:shadow-lg transition-all duration-300",
                    ),
                    class_name="space-y-4 max-w-xl mx-auto",
                ),
                on_submit=State.submit_contact_form,
                reset_on_submit=True,
                class_name="w-full",
            ),
            id="contacto",
            class_name="container mx-auto py-16 px-4",
        )
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.p(
                f"© 2014-{State.current_year} Juanca PC. Todos los derechos reservados.",
                class_name="text-gray-500",
            ),
            rx.el.div(
                rx.el.a(
                    rx.icon(
                        "twitter",
                        class_name="h-6 w-6 text-gray-500 hover:text-orange-500",
                    ),
                    href="#",
                ),
                rx.el.a(
                    rx.icon(
                        "facebook",
                        class_name="h-6 w-6 text-gray-500 hover:text-orange-500",
                    ),
                    href="#",
                ),
                rx.el.a(
                    rx.icon(
                        "instagram",
                        class_name="h-6 w-6 text-gray-500 hover:text-orange-500",
                    ),
                    href="#",
                ),
                class_name="flex gap-4",
            ),
            class_name="container mx-auto flex justify-between items-center py-6 px-4",
        ),
        class_name="bg-gray-100 border-t border-gray-200",
    )


def star(is_filled: rx.Var[bool]) -> rx.Component:
    return rx.icon(
        "star",
        class_name=rx.cond(
            is_filled,
            "h-8 w-8 text-yellow-400 fill-yellow-400",
            "h-8 w-8 text-gray-300",
        ),
    )


def review_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Deja tu Reseña", class_name="text-2xl font-bold text-gray-800 mb-4"),
        rx.el.div(
            rx.el.input(
                placeholder="Tu Nombre",
                on_change=State.set_new_review_name,
                class_name="w-full p-3 rounded-md border border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-transparent transition",
                default_value=State.new_review_name,
            ),
            rx.el.div(
                rx.el.p("Calificación:", class_name="text-gray-600 font-medium mb-2"),
                rx.el.div(
                    rx.foreach(
                        rx.Var.range(1, 6),
                        lambda i: rx.el.button(
                            star(
                                (i <= State.hover_rating)
                                | (i <= State.new_review_rating)
                            ),
                            on_click=lambda: State.set_rating(i),
                            on_mouse_enter=lambda: State.set_hover_rating(i),
                            on_mouse_leave=lambda: State.set_hover_rating(0),
                            class_name="p-1",
                        ),
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center gap-4",
            ),
            rx.el.textarea(
                placeholder="Tu comentario...",
                on_change=State.set_new_review_comment,
                class_name="w-full p-3 rounded-md border border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-transparent transition",
                rows=4,
                default_value=State.new_review_comment,
            ),
            rx.el.button(
                "Enviar Reseña",
                on_click=State.submit_review,
                class_name="w-full bg-orange-500 text-white p-3 rounded-lg font-semibold shadow-md hover:bg-orange-600 transition-colors",
            ),
            class_name="space-y-4",
        ),
        class_name="bg-white p-8 rounded-xl shadow-lg w-full max-w-2xl mx-auto",
    )


def review_card(review: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(review["name"], class_name="font-semibold text-gray-800"),
            rx.el.div(
                rx.foreach(
                    rx.Var.range(review["rating"]),
                    lambda i: rx.icon(
                        "star", class_name="h-5 w-5 text-yellow-400 fill-yellow-400"
                    ),
                ),
                class_name="flex",
            ),
            class_name="flex items-center justify-between mb-2",
        ),
        rx.el.p(review["comment"], class_name="text-gray-600"),
        class_name="bg-white p-6 rounded-xl shadow-sm",
    )


def reviews_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Lo que dicen nuestros clientes",
                class_name="text-3xl font-bold text-center text-gray-800 mb-12",
            ),
            rx.el.div(
                rx.foreach(State.reviews, review_card),
                class_name="grid md:grid-cols-2 gap-8 mb-12",
            ),
            review_form(),
            id="reseñas",
            class_name="container mx-auto py-16 px-4",
        ),
        class_name="bg-gray-50",
    )


from app.pages.servicios import servicios


def index() -> rx.Component:
    return rx.el.main(
        header(),
        hero_section(),
        services_section(),
        about_us_section(),
        reviews_section(),
        contact_form(),
        footer(),
        class_name="font-['Poppins'] bg-white",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, on_load=State.on_load)
app.add_page(servicios, route="/servicios")