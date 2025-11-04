import reflex as rx
from typing import TypedDict


class Service(TypedDict):
    icon: str
    title: str
    description: str
    details: list[str]


class ServicesState(rx.State):
    services: list[Service] = [
        {
            "icon": "wrench",
            "title": "Reparación de Hardware",
            "description": "Solución a problemas con componentes físicos de tu PC o laptop.",
            "details": [
                "Diagnóstico de fallos de hardware",
                "Reemplazo de componentes (RAM, disco duro, SSD)",
                "Reparación de placa base",
                "Limpieza interna y mantenimiento preventivo",
            ],
        },
        {
            "icon": "shield-check",
            "title": "Eliminación de Virus y Malware",
            "description": "Limpiamos tu equipo de software malicioso y mejoramos su seguridad.",
            "details": [
                "Escaneo profundo y eliminación de virus",
                "Protección contra ransomware y spyware",
                "Instalación y configuración de antivirus",
                "Asesoramiento sobre prácticas seguras en línea",
            ],
        },
        {
            "icon": "laptop-cog",
            "title": "Optimización de Sistema Operativo",
            "description": "Mejoramos la velocidad y rendimiento de tu sistema operativo Windows.",
            "details": [
                "Limpieza de archivos basura y temporales",
                "Optimización del arranque y apagado",
                "Actualización de drivers y software",
                "Configuración para máximo rendimiento",
            ],
        },
        {
            "icon": "database-backup",
            "title": "Recuperación de Datos",
            "description": "Rescatamos tus archivos importantes de discos duros dañados.",
            "details": [
                "Recuperación de archivos borrados accidentalmente",
                "Extracción de datos de discos duros con fallos",
                "Clonación de discos duros a nuevas unidades",
                "Configuración de sistemas de backup automático",
            ],
        },
        {
            "icon": "router",
            "title": "Configuración de Redes",
            "description": "Instalación y configuración de redes WiFi y cableadas en tu hogar u oficina.",
            "details": [
                "Instalación de routers y puntos de acceso",
                "Solución de problemas de conexión a Internet",
                "Mejora de la cobertura y velocidad del WiFi",
                "Configuración de red para teletrabajo",
            ],
        },
        {
            "icon": "cloud-cog",
            "title": "Asistencia Remota",
            "description": "Soporte técnico inmediato sin necesidad de moverte de tu casa.",
            "details": [
                "Resolución de problemas de software a distancia",
                "Instalación y configuración de programas",
                "Asistencia con cuentas de correo y servicios en la nube",
                "Clases personalizadas sobre uso de software",
            ],
        },
    ]