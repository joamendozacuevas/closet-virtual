1. Apartado de Negocio: El Problema Global y la Prueba de Concepto (POC)
El Problema Global
El problema principal es no saber exactamente qué ropa tengo en mi clóset, lo que dificulta la elección diaria y la creación de combinaciones óptimas. La solución completa a largo plazo es un aplicativo o inventario digital que permita visualizar todas las prendas disponibles y entregue recomendaciones de vestuario para saber qué puedo combinar y ponerme en el día a día.
La Prueba de Concepto (POC) para ES1
Para cumplir con los requisitos de la evaluación actual, la solución se acotará a un Filtro de Selección de Prenda (Validador de Ocasión). En lugar de recomendar un outfit completo desde una base de datos, el programa evaluará si una prenda específica recién ingresada o seleccionada es apta para usarla en una ocasión determinada. El programa tomará la decisión comparando el nivel de formalidad requerido para la salida con el nivel de formalidad intrínseco de la prenda.
Dato 1: Nivel de formalidad de la prenda (escala numérica, ej. 1 a 10).
Dato 2: Nivel de formalidad requerido para la ocasión (escala numérica, ej. 1 a 10).
Los 4 Resultados Posibles de la Decisión:
Dato Inválido: El nivel ingresado es negativo o supera el límite de la escala (ej. mayor a 10).
Aceptado: El nivel de formalidad de la prenda coincide (o tiene una diferencia aceptable) con el nivel de la ocasión. La prenda es ideal.
Rechazo 1 (Demasiado informal): El nivel de la prenda es considerablemente menor al requerido por la ocasión.
Rechazo 2 (Demasiado formal): El nivel de la prenda es considerablemente mayor al requerido (sobrevestido).

2. Apartado Técnico: Priorización MoSCoW
Must (Imprescindible - El MVP/POC para esta entrega)
Estas son las funciones exactas que se programarán y evaluarán en la versión actual.
Pedir por consola el nombre de la prenda y los dos datos numéricos: nivel de formalidad de la prenda y el nivel requerido para la ocasión.
Evaluar la decisión mediante una estructura de if / elif / else para resolver obligatoriamente los 4 casos descritos.
Mostrar por consola un mensaje claro con el resultado (aceptación o motivo específico de rechazo).
Guardar cada intento de validación como un registro en un archivo local datos.json.
Leer el archivo datos.json y mostrar una tabla resumen en consola (usando el paquete tabulate).
Crear una vista simple en Django que lea el archivo datos.json y lo despliegue en un template HTML.
Should (Importante - Próximos pasos tras el POC)
Funciones de alto valor que no entrarán en esta versión de consola, pero darán forma a la aplicación real.
Cargar y leer una base de datos real (o un JSON inicial robusto) que contenga todas las prendas de mi clóset con sus respectivas características.
Implementar validación de errores (ej. que el programa no se caiga si se ingresa texto en lugar de un número).
Filtrar la búsqueda por tipo de prenda (pantalón, camisa, abrigo).
Could (Deseable)
Características que harían el aplicativo excelente, si hubiera tiempo o recursos extra.
Subir fotos de cada prenda para tener un visualizador gráfico real del clóset.
Asignar colores a las prendas y crear reg
las de combinación cromática.
Conectar el recomendador a una API del clima para sugerir abrigos si hace frío.
Won't (Fuera por ahora)
Queda explícitamente fuera del alcance de las primeras versiones.
Implementar un sistema de registro de usuarios y contraseñas.
Funcionalidad de red social o compartir "outfits" con otras personas.
