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

## Phase 6: Migración a Base de Datos SQLite y Sistema de Backup ✅
- [x] Crear modelo de base de datos con SQLModel (Entry table)
- [x] Configurar SQLite database en rx.get_upload_dir() / "database.db"
- [x] Implementar schema con campos: id, name, rating, comment, client_token
- [x] Migrar toda la lógica de State de JSON a queries SQL
- [x] Migrar AdminState para usar SQLite con filtros SQL
- [x] Agregar función add_default_entries_if_empty() para inicializar DB
- [x] Mantener funcionalidad completa: reviews, contacts, delete, filters
- [x] Probar persistencia de datos con operaciones CRUD
- [x] Mejorar logging para debug de problemas de persistencia
- [x] Agregar sistema de backup CSV descargable desde panel admin
- [x] Implementar botón "Descargar Respaldo" con icono y estilo verde
- [x] Implementar botón "Subir Respaldo" (restore) con icono azul y rx.upload
- [x] Crear función handle_restore_upload() para procesar CSV y restaurar datos
- [x] **Establecer client_token=None en reseñas restauradas desde CSV**
- [x] **Implementar validación por nombre duplicado (case-insensitive) en submit_review()**
- [x] **Prevenir que usuarios dejen múltiples reseñas con el mismo nombre después de restauración**

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
- `AdminState.download_backup()` - Descarga CSV con todos los datos
- `AdminState.handle_restore_upload()` - Restaura datos desde CSV backup
- **`State.submit_review()` - Valida duplicados por token Y por nombre (case-insensitive)**

### Sistema de Validación Anti-Duplicados:
✅ **SOLUCIÓN COMPLETA IMPLEMENTADA**

**Problema Resuelto:** Después de restaurar desde CSV, los usuarios podían dejar otra reseña porque el sistema solo validaba por `client_token`, pero las reseñas restauradas tienen `client_token=None`.

**Solución de Doble Validación:**

1. **Validación por Token (Primera Línea de Defensa):**
   - Verifica si existe reseña con el mismo `client_token`
   - Mensaje: "Ya has enviado una reseña."
   - Bloquea usuarios que ya dejaron reseña en la sesión actual

2. **Validación por Nombre (Segunda Línea de Defensa - NEW!):**
   ```python
   existing_by_name = session.exec(
       sqlmodel.select(Entry).where(
           sqlmodel.func.lower(Entry.name) == self.new_review_name.lower(),
           Entry.rating > 0,
       )
   ).first()
   if existing_by_name:
       return rx.toast.error("Ya existe una reseña con ese nombre.")
   ```
   - Busca reseñas con el mismo nombre (case-insensitive)
   - Previene variaciones: "Juan Pérez" = "juan pérez" = "JUAN PÉREZ"
   - Mensaje: "Ya existe una reseña con ese nombre."
   - **Previene duplicados después de restauración desde CSV**

**Comportamiento Esperado:**
- ✅ Usuario intenta reseña con nombre existente → ❌ **Bloqueado**
- ✅ Usuario con variación de capitalización → ❌ **Bloqueado**
- ✅ Usuario con token duplicado → ❌ **Bloqueado**
- ✅ Usuario con nombre nuevo → ✅ **Permitido**

### Sistema de Backup y Restauración:
- **Formato:** CSV con todos los campos (id, name, rating, comment, client_token)
- **Backup (Descarga):** Botón verde "Descargar Respaldo" en panel admin
- **Restore (Restauración):** Botón azul "Subir Respaldo" con rx.upload component
- **Flujo de restauración:**
  1. Usuario hace clic en "Subir Respaldo"
  2. Selecciona archivo CSV previamente descargado
  3. Sistema lee y valida el CSV
  4. **Establece `client_token=None` para todas las reseñas restauradas**
  5. Borra todos los datos existentes en la DB
  6. Inserta todas las entradas del CSV
  7. Recarga la vista del admin automáticamente
  8. Muestra toast con número de entradas restauradas
  9. **La validación por nombre previene que usuarios con nombres existentes dejen nuevas reseñas**

### Cómo Restaurar Manualmente con CSV:
1. **Accede al panel de administración:** Ve a `/admin` e inicia sesión
2. **Haz clic en "Subir Respaldo"** (botón azul con icono de nube)
3. **Selecciona tu archivo CSV de backup** (descargado previamente)
4. **El sistema automáticamente:**
   - Lee el archivo CSV
   - Valida el formato
   - Borra todos los datos actuales
   - Inserta los datos del backup (con token=None)
   - Recarga la vista
   - Muestra mensaje de éxito con el número de registros restaurados
   - **Las validaciones por nombre previenen duplicados futuros**

### Debug de Persistencia:
- Logging agregado en `get_engine()` para verificar conexión a DB
- Logging en `add_default_entries_if_empty()` para confirmar inicialización
- Logging en `State.on_load()` para debug de carga de datos
- Verificación explícita de existencia de DB en cada conexión

### Solución a Problemas de Deploy:
1. **Verificar upload_dir:** La DB debe estar en `uploaded_files/database.db`
2. **Descargar backup:** Antes de cada deploy, descargar CSV desde panel admin
3. **Verificar logs:** Revisar logs de Reflex Hosting para errores de DB
4. **Reinicialización:** Si DB se pierde, se recreará automáticamente con datos de ejemplo
5. **Restauración:** Usar el botón "Subir Respaldo" para restaurar desde CSV backup
6. **Post-restauración:** El sistema de doble validación previene todos los duplicados
