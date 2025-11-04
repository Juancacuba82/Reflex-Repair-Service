import reflex as rx
from app.states.admin_state import AdminState
from app.app import footer


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("computer", class_name="h-12 w-12 text-orange-500"),
            rx.el.h2(
                "Panel de Administración",
                class_name="text-3xl font-bold text-gray-800 mt-4",
            ),
            rx.el.p(
                "Inicia sesión para gestionar el contenido.", class_name="text-gray-500"
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.input(
                        placeholder="Contraseña",
                        type="password",
                        name="password",
                        class_name="w-full p-3 rounded-md border border-gray-300 focus:ring-2 focus:ring-orange-500",
                    ),
                    rx.cond(
                        AdminState.error_message != "",
                        rx.el.p(
                            AdminState.error_message,
                            class_name="text-red-500 text-sm mt-2",
                        ),
                        None,
                    ),
                    rx.el.button(
                        "Entrar",
                        type="submit",
                        class_name="w-full bg-orange-500 text-white p-3 rounded-lg font-semibold shadow-md hover:bg-orange-600 transition-colors mt-4",
                    ),
                    class_name="space-y-4",
                ),
                on_submit=AdminState.login,
                reset_on_submit=True,
                class_name="mt-8 w-full max-w-sm",
            ),
            class_name="flex flex-col items-center text-center",
        ),
        class_name="flex justify-center items-center min-h-screen bg-gray-50 p-4",
    )


def admin_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.h1(
                    "Panel de Administración",
                    class_name="text-2xl font-bold text-gray-800",
                ),
                rx.el.button(
                    "Cerrar Sesión",
                    on_click=AdminState.logout,
                    class_name="bg-red-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-red-600 transition-colors",
                ),
                class_name="container mx-auto flex items-center justify-between p-4",
            ),
            class_name="bg-white shadow-md sticky top-0 z-10",
        ),
        rx.el.main(
            rx.el.div(
                rx.el.h2(
                    "Reseñas y Contactos",
                    class_name="text-3xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Todos",
                        on_click=lambda: AdminState.set_filter_mode("all"),
                        class_name=rx.cond(
                            AdminState.filter_mode == "all",
                            "bg-orange-500 text-white px-4 py-2 rounded-lg font-semibold",
                            "bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-semibold",
                        ),
                    ),
                    rx.el.button(
                        "Reseñas",
                        on_click=lambda: AdminState.set_filter_mode("reviews"),
                        class_name=rx.cond(
                            AdminState.filter_mode == "reviews",
                            "bg-orange-500 text-white px-4 py-2 rounded-lg font-semibold",
                            "bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-semibold",
                        ),
                    ),
                    rx.el.button(
                        "Contactos",
                        on_click=lambda: AdminState.set_filter_mode("contacts"),
                        class_name=rx.cond(
                            AdminState.filter_mode == "contacts",
                            "bg-orange-500 text-white px-4 py-2 rounded-lg font-semibold",
                            "bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-semibold",
                        ),
                    ),
                    class_name="flex gap-4 mb-8",
                ),
                rx.el.div(
                    rx.foreach(AdminState.filtered_entries, entry_card),
                    class_name="grid gap-6 md:grid-cols-2 lg:grid-cols-3",
                ),
                class_name="container mx-auto py-10 px-4",
            )
        ),
        footer(),
        class_name="bg-gray-50 min-h-screen",
    )


def entry_card(entry: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(entry["name"], class_name="font-bold text-lg truncate"),
                rx.cond(
                    entry["rating"].to(int) > 0,
                    rx.el.div(
                        rx.el.span(
                            entry["rating"].to_string() + "/5",
                            class_name="font-semibold",
                        ),
                        rx.icon(
                            "star",
                            class_name="h-5 w-5 text-yellow-400 fill-yellow-400 ml-1",
                        ),
                        class_name="flex items-center text-sm bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full",
                    ),
                    rx.el.span(
                        "CONTACTO",
                        class_name="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-semibold",
                    ),
                ),
                class_name="flex justify-between items-center mb-3",
            ),
            rx.el.p(
                entry["comment"],
                class_name="text-gray-600 text-sm whitespace-pre-wrap h-24 overflow-y-auto",
            ),
            class_name="flex-grow",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4 mr-2"),
                "Eliminar",
                on_click=lambda: AdminState.delete_entry(entry),
                class_name="bg-red-100 text-red-700 px-4 py-2 rounded-lg font-semibold hover:bg-red-200 transition-colors text-sm flex items-center",
            ),
            class_name="mt-4 pt-4 border-t border-gray-200 flex justify-end",
        ),
        class_name="bg-white p-6 rounded-xl shadow-lg flex flex-col justify-between h-full",
    )


def admin() -> rx.Component:
    return rx.cond(AdminState.is_logged_in, admin_dashboard(), login_page())