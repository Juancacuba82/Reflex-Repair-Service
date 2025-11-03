import reflex as rx
from typing import TypedDict


class Review(TypedDict):
    name: str
    rating: int
    comment: str


class State(rx.State):
    """The base state for the app."""

    reviews: list[Review] = [
        {
            "name": "Cliente Satisfecho",
            "rating": 5,
            "comment": "¡Excelente servicio! Mi computadora funciona como nueva. Rápido y profesional.",
        },
        {
            "name": "Usuario Agradecido",
            "rating": 4,
            "comment": "Buena atención y resolvieron mi problema de software a distancia. Lo recomiendo.",
        },
    ]
    new_review_name: str = ""
    new_review_comment: str = ""
    new_review_rating: int = 0
    hover_rating: int = 0

    @rx.event
    def submit_contact_form(self, form_data: dict):
        """Handles the contact form submission."""
        contact_name = form_data.get("name", "")
        contact_email = form_data.get("email", "")
        contact_phone = form_data.get("phone", "")
        contact_message = form_data.get("message", "")
        print(
            f"New contact form submission:\nName: {contact_name}\nEmail: {contact_email}\nPhone: {contact_phone}\nMessage: {contact_message}"
        )
        return rx.toast.success("¡Gracias por tu mensaje! Te contactaremos pronto.")

    @rx.event
    def submit_review(self):
        """Handles the review form submission."""
        if (
            not self.new_review_name
            or not self.new_review_comment
            or self.new_review_rating == 0
        ):
            return rx.toast.error("Por favor, completa todos los campos de la reseña.")
        new_review: Review = {
            "name": self.new_review_name,
            "rating": self.new_review_rating,
            "comment": self.new_review_comment,
        }
        self.reviews.append(new_review)
        self.new_review_name = ""
        self.new_review_comment = ""
        self.new_review_rating = 0
        self.hover_rating = 0
        return rx.toast.success("¡Gracias por tu reseña!")

    @rx.event
    def set_hover_rating(self, rating: int):
        self.hover_rating = rating

    @rx.event
    def set_rating(self, rating: int):
        self.new_review_rating = rating