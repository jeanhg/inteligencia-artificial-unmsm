# Guía para agregar trabajos semanales

## 1. Subir los tres materiales

En la carpeta `semanas/semana-XX/` correspondiente, agrega los archivos cuando estén terminados:

    semanas/semana-01/
    ├── index.html
    ├── README.md
    ├── informe/
    │   └── informe.pdf
    ├── presentacion/
    │   └── presentacion.pptx
    └── ejemplo/
        ├── README.md
        ├── main.py
        └── requirements.txt

Las carpetas `informe/`, `presentacion/` y `ejemplo/` de la primera semana ya tienen archivos `.gitkeep`. En otras semanas créalas cuando corresponda. No necesitas publicar archivos vacíos fingiendo una entrega.

## 2. Habilitar el enlace

Edita `data/semanas.json`. Busca la semana que acabas de completar y cambia solo los campos de `materials` para los archivos que ya existen.

Ejemplo para la semana 01:

    "materials": {
      "informe": {
        "url": "semanas/semana-01/informe/informe.pdf",
        "label": "Ver informe PDF"
      },
      "presentacion": {
        "url": "semanas/semana-01/presentacion/presentacion.pptx",
        "label": "Descargar PPT"
      },
      "ejemplo": {
        "url": "semanas/semana-01/ejemplo/README.md",
        "label": "Ver código e instrucciones"
      }
    }

Si uno de los materiales todavía no se entregó, deja su valor en `null`. No actives rutas inexistentes. Puedes enlazar a un cuaderno de Colab usando una URL completa.

## 3. Comprobar la página

- Entra a la página principal y verifica que la tarjeta de la semana aparezca en el catálogo.
- Abre el detalle de la semana y verifica cada enlace activado.
- Descarga el PPT y abre el PDF para comprobar que funcionan.
- Si publicas Python, incluye instrucciones y dependencias en `ejemplo/README.md`. GitHub Pages sirve archivos estáticos: para ejecutar Python en la nube puedes usar Google Colab o un despliegue específico.

## 4. Activar GitHub Pages (primera vez)

Ve a `Settings → Pages → Build and deployment`, selecciona `Deploy from a branch`, rama `main`, carpeta `/(root)` y guarda. La dirección prevista del sitio será:

https://jeanhg.github.io/inteligencia-artificial-unmsm/

No compartas ese enlace como sitio activo hasta que Pages indique que el despliegue terminó.

## 5. Seguridad y buenas prácticas

Evita subir claves API, credenciales, datos personales de terceros o archivos ajenos sin permiso. Usa nombres de archivos estables, documenta el origen de datos y conserva referencias bibliográficas en cada informe.
