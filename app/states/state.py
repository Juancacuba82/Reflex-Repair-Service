import json
import logging
from pathlib import Path
from typing import TypedDict, Optional
import reflex as rx

REVIEWS_FILENAME = "reviews.json"


class Review(TypedDict):
    name: str
    rating: int
    comment: str


DEFAULT_REVIEWS: list[Review] = [
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
_reviews_cache: Optional[list[Review]] = None


def get_reviews_file_path() -> Path:
    """Get the path to the reviews JSON file inside the assets directory."""
    assets_dir = Path("assets")
    assets_dir.mkdir(parents=True, exist_ok=True)
    return assets_dir / REVIEWS_FILENAME


def load_reviews_from_file() -> list[Review]:
    """Load reviews from the JSON file, using a global cache."""
    global _reviews_cache
    if _reviews_cache is not None:
        return _reviews_cache
    reviews_file = get_reviews_file_path()
    if reviews_file.exists():
        try:
            with reviews_file.open("r", encoding="utf-8") as f:
                _reviews_cache = json.load(f)
                return _reviews_cache
        except (IOError, json.JSONDecodeError) as e:
            logging.exception(f"Error loading reviews file: {e}")
    _reviews_cache = DEFAULT_REVIEWS.copy()
    save_reviews_to_file(_reviews_cache)
    return _reviews_cache


def save_reviews_to_file(reviews: list[Review]):
    """Save reviews to the JSON file and update the global cache."""
    global _reviews_cache
    _reviews_cache = reviews
    reviews_file = get_reviews_file_path()
    try:
        reviews_file.parent.mkdir(parents=True, exist_ok=True)
        with reviews_file.open("w", encoding="utf-8") as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)
    except IOError as e:
        logging.exception(f"Error saving reviews file: {e}")


class State(rx.State):
    """The base state for the app."""

    new_review_name: str = ""
    new_review_comment: str = ""
    new_review_rating: int = 0
    hover_rating: int = 0

    @rx.var
    def reviews(self) -> list[Review]:
        """Computed var to get reviews from the shared source."""
        return load_reviews_from_file()

    @rx.event
    def on_load(self):
        """Event handler to ensure reviews are loaded on page load."""
        load_reviews_from_file()

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
        """Handles the review form submission and saves to a shared JSON file."""
        if (
            not self.new_review_name
            or not self.new_review_comment
            or self.new_review_rating == 0
        ):
            return rx.toast.error("Por favor, completa todos los campos de la reseña.")
        current_reviews = load_reviews_from_file().copy()
        new_review: Review = {
            "name": self.new_review_name,
            "rating": self.new_review_rating,
            "comment": self.new_review_comment,
        }
        current_reviews.append(new_review)
        save_reviews_to_file(current_reviews)
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