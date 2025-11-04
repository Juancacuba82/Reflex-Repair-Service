import logging
from typing import TypedDict, Optional
import reflex as rx
import datetime
import sqlmodel
from pathlib import Path


class Entry(sqlmodel.SQLModel, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    name: str
    rating: int
    comment: str
    client_token: Optional[str] = sqlmodel.Field(index=True)


def get_db_path() -> Path:
    db_path = rx.get_upload_dir() / "database.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_engine():
    db_url = f"sqlite:///{get_db_path()}"
    logging.info(f"Connecting to database at: {db_url}")
    engine = sqlmodel.create_engine(db_url)
    sqlmodel.SQLModel.metadata.create_all(engine)
    logging.info("Database tables checked/created.")
    return engine


_db_initialized = False


def add_default_entries_if_empty():
    global _db_initialized
    if _db_initialized:
        logging.info("DB already initialized in this session. Skipping.")
        return
    try:
        logging.info("Checking if default entries are needed.")
        engine = get_engine()
        with sqlmodel.Session(engine) as session:
            count = session.exec(sqlmodel.select(sqlmodel.func.count(Entry.id))).one()
            if count == 0:
                logging.info("No entries found. Adding default entries.")
                default_entries = [
                    Entry(
                        name="Cliente Satisfecho",
                        rating=5,
                        comment="¡Excelente servicio! Mi computadora funciona como nueva. Rápido y profesional.",
                        client_token="default_token_1",
                    ),
                    Entry(
                        name="Usuario Agradecido",
                        rating=4,
                        comment="Buena atención y resolvieron mi problema de software a distancia. Lo recomiendo.",
                        client_token="default_token_2",
                    ),
                ]
                for entry in default_entries:
                    session.add(entry)
                session.commit()
                logging.info("Default entries added successfully.")
            else:
                logging.info(
                    f"Database already contains {count} entries. No action needed."
                )
    except Exception as e:
        logging.exception(f"Error during DB initialization: {e}")
    finally:
        _db_initialized = True


class State(rx.State):
    """The base state for the app."""

    new_review_email: str = ""
    new_review_comment: str = ""
    new_review_rating: int = 0
    hover_rating: int = 0
    _reloader: int = 0

    def _get_all_entries(self) -> list[Entry]:
        try:
            engine = get_engine()
            with sqlmodel.Session(engine) as session:
                return session.exec(sqlmodel.select(Entry)).all()
        except Exception as e:
            logging.exception(f"Error fetching entries from DB: {e}")
            return []

    @rx.var
    def current_year(self) -> int:
        return datetime.date.today().year

    @rx.var
    def reviews(self) -> list[dict]:
        """Computed var to get reviews directly from the database."""
        _ = self._reloader
        add_default_entries_if_empty()
        all_entries = self._get_all_entries()
        reviews_list = [entry.model_dump() for entry in all_entries if entry.rating > 0]
        return reviews_list

    @rx.var
    def has_submitted_review(self) -> bool:
        """Check if the current user has already submitted a review."""
        _ = self._reloader
        client_token = self.router.session.client_token
        if not client_token:
            return False
        try:
            engine = get_engine()
            with sqlmodel.Session(engine) as session:
                statement = sqlmodel.select(Entry).where(
                    Entry.client_token == client_token, Entry.rating > 0
                )
                return session.exec(statement).first() is not None
        except Exception as e:
            logging.exception(f"Error checking for submitted review: {e}")
            return False

    @rx.event
    def on_load(self):
        """Event handler to ensure reviews are loaded on page load."""
        logging.info("Page loaded. Running DB checks and reloading state.")
        add_default_entries_if_empty()
        yield State.force_reload_reviews()

    @rx.event
    def force_reload_reviews(self):
        """Forces a reload of reviews by updating the dummy reloader var."""
        self._reloader += 1

    @rx.event
    def submit_contact_form(self, form_data: dict):
        """Handles the contact form submission and saves it to the database."""
        name = form_data.get("name", "")
        email = form_data.get("email", "")
        message = form_data.get("message", "")
        if not all([name, email, message]):
            return rx.toast.error("Por favor, completa nombre, email y mensaje.")
        contact_entry = Entry(
            name=f"[CONTACTO] {name}",
            rating=0,
            comment=f"Email: {email}\nCelular: {form_data.get('phone', 'N/A')}\n\nMensaje: {message}",
            client_token=self.router.session.client_token,
        )
        try:
            engine = get_engine()
            with sqlmodel.Session(engine) as session:
                session.add(contact_entry)
                session.commit()
        except Exception as e:
            logging.exception(f"Failed to save contact form submission: {e}")
            return rx.toast.error(
                "Hubo un error al guardar tu mensaje. Inténtalo de nuevo."
            )
        yield rx.toast.success("¡Gracias por tu mensaje! Te contactaremos pronto.")
        yield State.force_reload_reviews

    @rx.event
    def submit_review(self):
        """Handles the review form submission and saves to the database."""
        if (
            not self.new_review_email
            or not self.new_review_comment
            or self.new_review_rating == 0
        ):
            return rx.toast.error("Por favor, completa todos los campos de la reseña.")
        if self.has_submitted_review:
            return rx.toast.error("Ya has enviado una reseña con este dispositivo.")
        try:
            engine = get_engine()
            with sqlmodel.Session(engine) as session:
                existing_by_email = session.exec(
                    sqlmodel.select(Entry).where(
                        sqlmodel.func.lower(Entry.name)
                        == self.new_review_email.lower(),
                        Entry.rating > 0,
                    )
                ).first()
                if existing_by_email:
                    return rx.toast.error(
                        "Ya existe una reseña con ese email. Por favor, utiliza otro."
                    )
                new_review_entry = Entry(
                    name=self.new_review_email,
                    rating=self.new_review_rating,
                    comment=self.new_review_comment,
                    client_token=self.router.session.client_token,
                )
                session.add(new_review_entry)
                session.commit()
        except Exception as e:
            logging.exception(f"Failed to save review: {e}")
            return rx.toast.error("Hubo un error al guardar tu reseña.")
        self.new_review_email = ""
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