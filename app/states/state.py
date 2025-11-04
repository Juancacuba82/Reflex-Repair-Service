import json
import logging
from pathlib import Path
from typing import TypedDict, Optional
import reflex as rx
import datetime

REVIEWS_FILENAME = "reviews.json"


class Review(TypedDict):
    name: str
    rating: int
    comment: str


class ContactSubmission(TypedDict):
    name: str
    email: str
    phone: str
    message: str


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


def get_assets_dir() -> Path:
    """Get the path to the assets directory."""
    assets_dir = Path("assets")
    assets_dir.mkdir(parents=True, exist_ok=True)
    return assets_dir


def load_from_json_file(filename: str, default_data: list) -> list:
    """Generic function to load data from a JSON file in the assets directory."""
    file_path = get_assets_dir() / filename
    if file_path.exists() and file_path.stat().st_size > 0:
        try:
            with file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logging.exception(f"Error loading {filename}, recreating it: {e}")
    save_to_json_file(filename, default_data)
    return default_data.copy()


def save_to_json_file(filename: str, data: list):
    """Generic function to save data to a JSON file in the assets directory."""
    file_path = get_assets_dir() / filename
    try:
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        logging.exception(f"Error saving {filename}: {e}")


def load_all_entries_from_file() -> list[Review]:
    """Load all entries from the JSON file."""
    return load_from_json_file(REVIEWS_FILENAME, DEFAULT_REVIEWS)


def save_entries_to_file(entries: list[Review]):
    """Save all entries to the JSON file."""
    save_to_json_file(REVIEWS_FILENAME, entries)


class State(rx.State):
    """The base state for the app."""

    new_review_name: str = ""
    new_review_comment: str = ""
    new_review_rating: int = 0
    hover_rating: int = 0
    _reloader: int = 0

    @rx.var
    def current_year(self) -> int:
        return datetime.date.today().year

    @rx.var
    def reviews(self) -> list[Review]:
        """Computed var to get reviews directly from the file, ensuring it's always fresh."""
        _ = self._reloader
        all_entries = load_all_entries_from_file()
        return [entry for entry in all_entries if entry.get("rating", 0) > 0]

    @rx.event
    def on_load(self):
        """Event handler to ensure reviews are loaded on page load."""
        self._reloader += 1

    @rx.event
    def force_reload_reviews(self):
        """Forces a reload of reviews by updating the dummy reloader var."""
        self._reloader += 1

    @rx.event
    def submit_contact_form(self, form_data: dict):
        """Handles the contact form submission and saves it to reviews.json."""
        name = form_data.get("name", "")
        email = form_data.get("email", "")
        message = form_data.get("message", "")
        if not all([name, email, message]):
            return rx.toast.error("Por favor, completa nombre, email y mensaje.")
        contact_entry: Review = {
            "name": f"[CONTACTO] {name}",
            "rating": 0,
            "comment": f"Email: {email}\nTeléfono: {form_data.get('phone', 'N/A')}\n\nMensaje: {message}",
        }
        try:
            all_entries = load_all_entries_from_file()
            all_entries.append(contact_entry)
            save_entries_to_file(all_entries)
        except Exception as e:
            logging.exception(f"Failed to save contact form submission: {e}")
            return rx.toast.error(
                "Hubo un error al guardar tu mensaje. Inténtalo de nuevo."
            )
        yield rx.toast.success("¡Gracias por tu mensaje! Te contactaremos pronto.")
        yield State.force_reload_reviews

    @rx.event
    def submit_review(self):
        """Handles the review form submission and saves to a shared JSON file."""
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
        current_entries = load_all_entries_from_file()
        current_entries.append(new_review)
        save_entries_to_file(current_entries)
        self.new_review_name = ""
        self.new_review_comment = ""
        self.new_review_rating = 0
        self.hover_rating = 0
        yield rx.toast.success("¡Gracias por tu reseña!")
        yield State.force_reload_reviews

    @rx.event
    def set_hover_rating(self, rating: int):
        self.hover_rating = rating

    @rx.event
    def set_rating(self, rating: int):
        self.new_review_rating = rating