import reflex as rx


def service_card(service: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(service["icon"], class_name="h-10 w-10 text-orange-500"),
            class_name="mb-4",
        ),
        rx.el.h3(service["title"], class_name="text-xl font-bold text-gray-800 mb-2"),
        rx.el.p(service["description"], class_name="text-gray-600 mb-4 h-20"),
        rx.el.ul(
            rx.foreach(
                service["details"],
                lambda detail: rx.el.li(
                    rx.icon(
                        "square_check",
                        class_name="h-5 w-5 text-green-500 mr-2 shrink-0",
                    ),
                    rx.el.span(detail, class_name="text-gray-700"),
                    class_name="flex items-start",
                ),
            ),
            class_name="space-y-2 text-sm",
        ),
        class_name="bg-white p-6 rounded-xl shadow-md hover:shadow-2xl transition-shadow duration-300 transform hover:-translate-y-2 flex flex-col",
    )