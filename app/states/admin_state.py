import reflex as rx
import os
from typing import TypedDict
import logging
import sqlmodel
from app.states.state import Entry, get_engine
import csv
import io
import reflex as rx

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Proevolution15425*")


class AdminState(rx.State):
    is_logged_in: bool = False
    password: str = ""
    error_message: str = ""
    all_entries: list[dict] = []
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
        try:
            engine = get_engine()
            with sqlmodel.Session(engine) as session:
                entries = session.exec(sqlmodel.select(Entry)).all()
                self.all_entries = [entry.model_dump() for entry in entries]
        except Exception as e:
            logging.exception(f"Failed to load entries for admin: {e}")
            self.all_entries = []

    @rx.var
    def filtered_entries(self) -> list[dict]:
        if self.filter_mode == "reviews":
            return [e for e in self.all_entries if e.get("rating", 0) > 0]
        elif self.filter_mode == "contacts":
            return [e for e in self.all_entries if e.get("rating", 0) == 0]
        return self.all_entries

    @rx.event
    def set_filter_mode(self, mode: str):
        self.filter_mode = mode

    @rx.event
    def delete_entry(self, entry_to_delete: dict):
        entry_id = entry_to_delete.get("id")
        if not entry_id:
            return rx.toast.error("No se pudo eliminar la entrada: ID no encontrado.")
        try:
            engine = get_engine()
            with sqlmodel.Session(engine) as session:
                db_entry = session.get(Entry, entry_id)
                if db_entry:
                    session.delete(db_entry)
                    session.commit()
                else:
                    return rx.toast.error(
                        "La entrada no fue encontrada en la base de datos."
                    )
        except Exception as e:
            logging.exception(f"Failed to delete entry {entry_id}: {e}")
            return rx.toast.error("Ocurrió un error al eliminar la entrada.")
        yield AdminState.load_entries
        from app.states.state import State

        yield State.force_reload_reviews
        yield rx.toast.success("Entrada eliminada correctamente.")

    @rx.event
    async def handle_restore_upload(self, files: list[rx.UploadFile]):
        """Handles the CSV backup file upload and restores the data."""
        if not self.is_logged_in:
            yield rx.toast.error("Acceso denegado.")
            return
        if not files:
            yield rx.toast.error("No se seleccionó ningún archivo.")
            return
        try:
            file = files[0]
            csv_data = await file.read()
            csv_text = csv_data.decode("utf-8")
            reader = csv.DictReader(io.StringIO(csv_text))
            new_entries = []
            for row in reader:
                try:
                    entry = Entry(
                        name=row["name"],
                        rating=int(row["rating"]),
                        comment=row["comment"],
                        client_token=row.get("client_token") or None,
                    )
                    new_entries.append(entry)
                except (KeyError, ValueError) as e:
                    logging.exception(
                        f"Saltando fila inválida en CSV: {row}, error: {e}"
                    )
                    continue
            if not new_entries:
                yield rx.toast.error(
                    "El archivo CSV está vacío o en un formato incorrecto."
                )
                return
            engine = get_engine()
            with sqlmodel.Session(engine) as session:
                session.exec(sqlmodel.delete(Entry))
                for entry in new_entries:
                    session.add(entry)
                session.commit()
            yield AdminState.load_entries
            from app.states.state import State

            yield State.force_reload_reviews
            yield rx.toast.success(
                f"¡Restauración completada! Se cargaron {len(new_entries)} entradas."
            )
        except Exception as e:
            logging.exception(f"Error al restaurar desde el backup: {e}")
            yield rx.toast.error("Ocurrió un error durante la restauración.")

    @rx.event
    def download_backup(self):
        """Downloads all entries as a CSV file."""
        if not self.is_logged_in:
            return rx.toast.error("Acceso denegado.")
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "name", "rating", "comment", "client_token"])
        for entry in self.all_entries:
            writer.writerow(
                [
                    entry.get("id"),
                    entry.get("name"),
                    entry.get("rating"),
                    entry.get("comment"),
                    entry.get("client_token"),
                ]
            )
        csv_data = output.getvalue()
        return rx.download(data=csv_data, filename="juanca_pc_backup.csv")