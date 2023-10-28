
# API de Diccionario

La API de Diccionario es una herramienta que proporciona acceso a un amplio conjunto de datos léxicos y definiciones de palabras. Esta API te permite buscar términos, obtener significados, sinónimos, antónimos y más, lo que la convierte en una valiosa herramienta para aplicaciones y servicios relacionados con el lenguaje.

## Uso

### Consulta de Definiciones

#### Endpoint
```
GET /definiciones/{palabra}
```

Obtén la definición de una palabra específica.

Ejemplo de solicitud:
```
GET /definiciones/gato
```

Respuesta:
```
{
    "palabra": "gato",
    "definicion": "Un mamífero carnívoro de la familia Felidae, conocido por ser un animal doméstico común y por cazar ratones y otros pequeños animales.",
    "ejemplo": "Mi gato es muy juguetón."
}
```

### Consulta de Sinónimos

#### Endpoint
```
GET /sinonimos/{palabra}
```

Obtén una lista de sinónimos para una palabra específica.

Ejemplo de solicitud:
```
GET /sinonimos/felino
```

Respuesta:
```
{
    "palabra": "felino",
    "sinonimos": ["gato", "félido", "mamífero carnívoro"]
}
```

### Consulta de Antónimos

#### Endpoint
```
GET /antonimos/{palabra}
```

Obtén una lista de antónimos para una palabra específica.

Ejemplo de solicitud:
```
GET /antonimos/amigo
```

Respuesta:
```
{
    "palabra": "amigo",
    "antonimos": ["enemigo", "rival", "adversario"]
}
```

## Instalación

1. Clona este repositorio en tu servidor:

```
git clone https://github.com/tu-usuario/api-diccionario.git
```

2. Instala las dependencias:

```
npm install
```

3. Configura las variables de entorno necesarias, como la clave de acceso a la base de datos de diccionario.

4. Inicia el servidor:

```
npm start
```

## Configuración de Variables de Entorno

Asegúrate de configurar las siguientes variables de entorno en un archivo `.env`:

- `DB_URL`: La URL de conexión a la base de datos de diccionario.
- `API_KEY`: Tu clave de acceso a la API.

## Contribuciones

Si deseas contribuir a este proyecto, ¡eres bienvenido! Simplemente sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu contribución.
3. Realiza tus cambios y asegúrate de que todo funcione correctamente.
4. Envía un pull request.

## Contacto

Si tienes alguna pregunta o comentario, no dudes en contactarnos en [tu@email.com](mailto:tu@email.com).

¡Esperamos que esta API de Diccionario sea útil para tus aplicaciones y servicios relacionados con el lenguaje!

