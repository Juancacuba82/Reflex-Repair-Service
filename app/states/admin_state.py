import reflex as rx
import os
from typing import TypedDict
import json
import logging
from pathlib import Path

REVIEWS_FILENAME = "reviews.json"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Proevolution15425*")


class Review(TypedDict):
    name: str
    rating: int
    comment: str
    client_token: str | None


def load_all_entries() -> list[Review]:
    """Load all entries (reviews and contacts) from the JSON file."""
    file_path = get_upload_dir_path() / REVIEWS_FILENAME
    if file_path.exists() and file_path.stat().st_size > 0:
        try:
            with file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logging.exception(f"Error loading {REVIEWS_FILENAME}: {e}")
    return []


def save_all_entries(entries: list[Review]):
    """Save all entries to the JSON file."""
    file_path = get_upload_dir_path() / REVIEWS_FILENAME
    try:
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    except IOError as e:
        logging.exception(f"Error saving {REVIEWS_FILENAME}: {e}")


class AdminState(rx.State):
    is_logged_in: bool = False
    password: str = ""
    error_message: str = ""
    all_entries: list[Review] = []
    filter_mode: str = "all"

    @rx.event
    def login(self, form_data: dict):
        password = form_data.get("password", "")
        if password == ADMIN_PASSWORD:
            self.is_logged_in = True
            self.error_message = ""
            self.password = ""
            return AdminState.load_entries
        else:
            self.error_message = "Contraseña incorrecta."
            self.password = ""

    @rx.event
    def logout(self):
        self.is_logged_in = False
        self.all_entries = []
        self.error_message = ""
        self.password = ""
        return [AdminState.set_is_logged_in(False), rx.redirect("/")]

    @rx.event
    def load_entries(self):
        if not self.is_logged_in:
            self.all_entries = []
            return
        self.all_entries = load_all_entries()

    @rx.var
    def filtered_entries(self) -> list[Review]:
        if self.filter_mode == "reviews":
            return [e for e in self.all_entries if e.get("rating", 0) > 0]
        elif self.filter_mode == "contacts":
            return [e for e in self.all_entries if e.get("rating", 0) == 0]
        return self.all_entries

    @rx.event
    def set_filter_mode(self, mode: str):
        self.filter_mode = mode

    @rx.event
    def delete_entry(self, entry_to_delete: Review):
        current_entries = load_all_entries()
        updated_entries = [
            entry
            for entry in current_entries
            if not (
                entry.get("client_token") == entry_to_delete.get("client_token")
                and entry["name"] == entry_to_delete["name"]
                and (entry.get("comment") == entry_to_delete.get("comment"))
                and (entry.get("rating") == entry_to_delete.get("rating"))
            )
        ]
        save_all_entries(updated_entries)
        yield AdminState.load_entries
        from app.states.state import State

        yield State.force_reload_reviews
        yield rx.toast.success("Entrada eliminada correctamente.")