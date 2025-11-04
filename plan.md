# Plan: Aplicación de Reparación de Computadoras con Sistema de Calificaciones

## Phase 1: Página Principal y Navegación ✅
- [x] Crear estructura base con header, navegación y footer
- [x] Diseñar hero section con información del servicio
- [x] Implementar sección de servicios (reparación local y online)
- [x] Agregar sección "Sobre Nosotros" y formulario de contacto
- [x] Aplicar Material Design 3 con colores naranja y gris, tipografía Poppins

---

## Phase 2: Sistema de Calificaciones y Comentarios ✅
- [x] Crear componente de calificación con estrellas (1-5)
- [x] Implementar formulario para dejar comentarios
- [x] Crear sistema de almacenamiento de reseñas persistente en el servidor (archivo JSON)
- [x] Diseñar galería de reseñas con calificaciones y comentarios
- [x] Agregar validación de formularios
- [x] Implementar almacenamiento compartido entre todos los usuarios usando assets/reviews.json
- [x] **Sistema de persistencia usa assets/reviews.json para git**

---

## Phase 3: Página de Servicios Detallada y Optimización Final ✅
- [x] Crear página dedicada para servicios detallados en `/servicios`
- [x] Implementar cards con elevación Material Design para cada servicio (6 servicios completos)
- [x] Agregar animaciones y transiciones suaves (hover, transform, shadow)
- [x] Optimizar responsive design para móviles y tablets (grid adaptativo)
- [x] Pulir UI/UX con feedback visual y estados de hover mejorados
- [x] Actualizar navegación del header para incluir link a la página de servicios

---

## Phase 4: Sistema Unificado de Almacenamiento ✅
- [x] Unificar almacenamiento de contactos y reseñas en un solo archivo reviews.json
- [x] Implementar sistema de rating=0 para contactos privados (no visibles en página)
- [x] Agregar filtro en computed var para mostrar solo reseñas con rating > 0
- [x] Eliminar sistema de email y archivo contacts.json separado
- [x] Simplificar código eliminando dependencias innecesarias (aiosmtplib)
- [x] Mantener prefijo [CONTACTO] en nombre para fácil identificación en archivo JSON

---

## Phase 5: Panel de Administración ✅
- [x] Crear página de administración en `/admin` con autenticación por contraseña
- [x] Implementar sistema de login con almacenamiento de sesión segura
- [x] Diseñar vista de listado de todas las reseñas y contactos
- [x] Agregar funcionalidad para eliminar reseñas específicas con confirmación
- [x] Implementar filtros para separar reseñas públicas de contactos privados

---

## Phase 6: Migración a Base de Datos SQLite Persistente ✅
- [x] Crear modelo de base de datos con SQLModel (Entry table)
- [x] Configurar SQLite database en rx.get_upload_dir() / "database.db"
- [x] Implementar schema con campos: id, name, rating, comment, client_token
- [x] Migrar toda la lógica de State de JSON a queries SQL
- [x] Migrar AdminState para usar SQLite con filtros SQL
- [x] Agregar función add_default_entries_if_empty() para inicializar DB
- [x] Mantener funcionalidad completa: reviews, contacts, delete, filters
- [x] Probar persistencia de datos con operaciones CRUD

---

## Phase 7: Funcionalidades Avanzadas del Panel Admin 
- [ ] Agregar funcionalidad para editar reseñas existentes
- [ ] Implementar estadísticas del panel (total de reseñas, promedio de calificación)
- [ ] Crear sistema de respuesta a contactos desde el panel
- [ ] Agregar logs de acciones administrativas

---

## Phase 8: Seguridad y UX del Panel Admin 
- [ ] Implementar protección contra fuerza bruta en login
- [ ] Agregar sistema de logout y gestión de sesiones mejorado
- [ ] Crear diseño responsive del panel para móviles
- [ ] Implementar confirmaciones visuales para acciones destructivas

---

## Notas Técnicas

### Sistema de Base de Datos Actual:
- **Tipo:** SQLite con SQLModel/SQLAlchemy
- **Ubicación:** `rx.get_upload_dir() / "database.db"`
- **Persistencia:** ✅ Garantizada en Reflex hosting (upload_dir persiste entre deploys)
- **Ventajas:** Transacciones ACID, queries SQL, mejor rendimiento, sin race conditions

### Modelo de Datos:
```python
class Entry(sqlmodel.SQLModel, table=True):
    id: Optional[int] (primary key)
    name: str
    rating: int (0 para contactos, 1-5 para reseñas)
    comment: str
    client_token: Optional[str] (para verificar si usuario ya dejó reseña)
```

### Funciones Principales:
- `get_engine()` - Crea/conecta a la base de datos SQLite
- `add_default_entries_if_empty()` - Inicializa DB con 2 reseñas de ejemplo
- `State.reviews` - Computed var que query reseñas (rating > 0)
- `State.has_submitted_review` - Verifica si usuario ya dejó reseña
- `AdminState.filtered_entries` - Filtra entre todos/reseñas/contactos