"""Generate student-facing assignment handouts for Operación de Modelos.

The PDFs deliberately keep the same compact academic handout shape across
weeks: brief, numbered tasks; explicit evidence; an acceptance checklist; and
the command that proves the work. The source of truth for the exercise itself
remains in each week's ``modules`` directory.
"""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assignments"
LOGO = ROOT / "assets" / "comillas_logo.jpg"

INK = colors.HexColor("#18212B")
MUTED = colors.HexColor("#5C6873")
ACCENT = colors.HexColor("#8C2438")
ACCENT_DARK = colors.HexColor("#641A2A")
GOLD = colors.HexColor("#C7A44A")
PALE = colors.HexColor("#F4F1EC")
PALE_BLUE = colors.HexColor("#EEF3F5")
GRID = colors.HexColor("#D8DDE0")
WHITE = colors.white


@dataclass(frozen=True)
class Assignment:
    week: int
    class_number: int
    title: str
    subtitle: str
    duration: str
    modality: str
    prerequisites: str
    goal: str
    context: list[str]
    materials: list[str]
    tasks: list[tuple[str, str]]
    deliverables: list[tuple[str, str]]
    acceptance: list[str]
    rubric: list[tuple[str, str]]
    commands: list[str]
    notes: list[str]
    source_paths: list[str]


styles = getSampleStyleSheet()
BODY = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9.2,
    leading=13.2,
    textColor=INK,
    spaceAfter=5,
)
BODY_SMALL = ParagraphStyle(
    "BodySmall",
    parent=BODY,
    fontSize=8.1,
    leading=11.1,
    textColor=MUTED,
)
REFERENCE = ParagraphStyle(
    "Reference",
    parent=BODY_SMALL,
    fontSize=7.1,
    leading=8.5,
    spaceBefore=0,
    spaceAfter=0,
)
REFERENCE_HEADING = ParagraphStyle(
    "ReferenceHeading",
    parent=REFERENCE,
    fontName="Helvetica-Bold",
    fontSize=8.1,
    leading=9,
    textColor=ACCENT_DARK,
    spaceBefore=2,
    spaceAfter=2,
)
KICKER = ParagraphStyle(
    "Kicker",
    parent=BODY,
    fontName="Helvetica-Bold",
    fontSize=8.2,
    leading=10,
    textColor=ACCENT,
    tracking=1.2,
    spaceAfter=4,
)
TITLE = ParagraphStyle(
    "AssignmentTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=25,
    textColor=INK,
    spaceAfter=6,
)
SUBTITLE = ParagraphStyle(
    "AssignmentSubtitle",
    parent=BODY,
    fontSize=11.5,
    leading=15,
    textColor=MUTED,
    spaceAfter=11,
)
H1 = ParagraphStyle(
    "Section",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=12.5,
    leading=15,
    textColor=ACCENT_DARK,
    spaceBefore=9,
    spaceAfter=5,
    keepWithNext=True,
)
H2 = ParagraphStyle(
    "Subsection",
    parent=styles["Heading3"],
    fontName="Helvetica-Bold",
    fontSize=9.8,
    leading=12,
    textColor=INK,
    spaceBefore=5,
    spaceAfter=3,
    keepWithNext=True,
)
TASK = ParagraphStyle(
    "Task",
    parent=BODY,
    leftIndent=0,
    firstLineIndent=0,
    spaceAfter=6,
)
TABLE_HEAD = ParagraphStyle(
    "TableHead",
    parent=BODY_SMALL,
    fontName="Helvetica-Bold",
    textColor=WHITE,
    fontSize=7.8,
    leading=9.5,
)
TABLE_CELL = ParagraphStyle(
    "TableCell",
    parent=BODY_SMALL,
    fontSize=7.8,
    leading=10.2,
    textColor=INK,
)
CODE = ParagraphStyle(
    "Code",
    parent=BODY_SMALL,
    fontName="Courier",
    fontSize=7.2,
    leading=9.2,
    textColor=INK,
)
CALLOUT = ParagraphStyle(
    "Callout",
    parent=BODY,
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=12.5,
    textColor=ACCENT_DARK,
    spaceAfter=0,
)
CENTER_SMALL = ParagraphStyle(
    "CenterSmall",
    parent=BODY_SMALL,
    alignment=TA_CENTER,
)


def text(value: str) -> str:
    """Escape plain text for a ReportLab Paragraph."""

    return html.escape(value).replace("\n", "<br/>")


def p(value: str, style: ParagraphStyle = BODY) -> Paragraph:
    return Paragraph(text(value), style)


def markup(value: str, style: ParagraphStyle = BODY) -> Paragraph:
    """Use only for controlled, local markup such as a bold label."""

    return Paragraph(value, style)


def section(title: str, style: ParagraphStyle = H1) -> list[Flowable]:
    return [Paragraph(text(title), style)]


def numbered(items: Iterable[tuple[str, str]]) -> list[Flowable]:
    flowables: list[Flowable] = []
    for number, (title, body) in enumerate(items, start=1):
        flowables.append(
            markup(
                f'<font color="{ACCENT.hexval()}"><b>{number:02d}</b></font> '
                f"<b>{html.escape(title)}</b> - {html.escape(body)}",
                TASK,
            )
        )
    return flowables


def checklist(items: Iterable[str]) -> list[Flowable]:
    return [
        markup(
            f'<font color="{ACCENT.hexval()}">[ ]</font> {html.escape(item)}',
            BODY,
        )
        for item in items
    ]


def make_table(
    headers: list[str],
    rows: list[tuple[str, ...]],
    widths: list[float] | None = None,
) -> Table:
    data = [[Paragraph(text(header), TABLE_HEAD) for header in headers]]
    data.extend(
        [[Paragraph(text(cell), TABLE_CELL) for cell in row] for row in rows]
    )
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), ACCENT_DARK),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.35, GRID),
                ("BACKGROUND", (0, 1), (-1, -1), WHITE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE_BLUE]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def callout(label: str, body: str) -> Table:
    box = Table(
        [[markup(f"<b>{html.escape(label)}</b><br/>{html.escape(body)}", CALLOUT)]],
        colWidths=[170 * mm],
    )
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE),
                ("BOX", (0, 0), (-1, -1), 0.7, GOLD),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return box


def code_block(commands: list[str]) -> Preformatted:
    return Preformatted("\n\n".join(commands), CODE)


def header_footer(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, height - 18 * mm, width - doc.rightMargin, height - 18 * mm)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(ACCENT_DARK)
    canvas.drawString(doc.leftMargin, height - 14 * mm, "OPERACION DE MODELOS")
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(
        width - doc.rightMargin,
        height - 14 * mm,
        f"MUIAAp  |  semana {doc.assignment.week:02d}  |  clase {doc.assignment.class_number}",
    )
    canvas.setStrokeColor(GRID)
    canvas.line(doc.leftMargin, 15 * mm, width - doc.rightMargin, 15 * mm)
    canvas.setFont("Helvetica", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 10.5 * mm, "Comillas ICAI  |  Material de trabajo")
    canvas.drawRightString(width - doc.rightMargin, 10.5 * mm, f"{canvas.getPageNumber():02d}")
    canvas.restoreState()


def title_block(assignment: Assignment) -> list[Flowable]:
    logo = Image(str(LOGO), width=62 * mm, height=62 * mm * 187 / 710)
    logo.hAlign = "LEFT"
    meta = make_table(
        ["DURACION", "MODALIDAD", "PREREQUISITOS"],
        [(assignment.duration, assignment.modality, assignment.prerequisites)],
        widths=[43 * mm, 48 * mm, 79 * mm],
    )
    return [
        logo,
        Spacer(1, 4),
        Paragraph(
            text(f"ASSIGNMENT {assignment.week}.{assignment.class_number}"),
            KICKER,
        ),
        Paragraph(text(assignment.title), TITLE),
        Paragraph(text(assignment.subtitle), SUBTITLE),
        meta,
        Spacer(1, 8),
    ]


def build_story(assignment: Assignment) -> list[Flowable]:
    story: list[Flowable] = []
    story.extend(title_block(assignment))
    story.extend(section("1. Encargo"))
    story.append(p(assignment.goal))
    story.append(callout("Regla de continuidad", assignment.context[0]))
    story.append(Spacer(1, 5))

    story.extend(section("2. Punto de partida"))
    story.extend([p(f"- {item}", BODY) for item in assignment.context[1:]])
    story.extend(section("3. Material que recibes"))
    story.extend([p(f"- {item}", BODY) for item in assignment.materials])

    story.extend(section("4. Tareas"))
    story.extend(numbered(assignment.tasks))

    story.extend(section("5. Entrega"))
    story.append(
        make_table(
            ["Evidencia", "Que debe permitir comprobar"],
            assignment.deliverables,
            widths=[52 * mm, 118 * mm],
        )
    )
    story.append(Spacer(1, 7))

    story.extend(section("6. Criterios de aceptacion"))
    story.extend(checklist(assignment.acceptance))

    story.extend(section("7. Rubrica orientativa"))
    story.append(
        make_table(
            ["Criterio", "Puntos"],
            assignment.rubric,
            widths=[145 * mm, 25 * mm],
        )
    )

    story.extend(section("8. Comprobacion"))
    story.append(code_block(assignment.commands))
    story.append(Spacer(1, 6))

    story.extend(section("9. Notas y limites"))
    story.extend([p(f"- {item}", BODY) for item in assignment.notes])
    story.extend(section("Referencia en el repositorio", REFERENCE_HEADING))
    story.extend([p(path, REFERENCE) for path in assignment.source_paths])
    return story


def assignment(
    week: int,
    class_number: int,
    title: str,
    subtitle: str,
    duration: str,
    modality: str,
    prerequisites: str,
    goal: str,
    context: list[str],
    materials: list[str],
    tasks: list[tuple[str, str]],
    deliverables: list[tuple[str, str]],
    acceptance: list[str],
    rubric: list[tuple[str, str]],
    commands: list[str],
    notes: list[str],
    source_paths: list[str],
) -> Assignment:
    return Assignment(
        week=week,
        class_number=class_number,
        title=title,
        subtitle=subtitle,
        duration=duration,
        modality=modality,
        prerequisites=prerequisites,
        goal=goal,
        context=context,
        materials=materials,
        tasks=tasks,
        deliverables=deliverables,
        acceptance=acceptance,
        rubric=rubric,
        commands=commands,
        notes=notes,
        source_paths=source_paths,
    )


ASSIGNMENTS = [
    assignment(
        1,
        1,
        "Configuracion inicial del entorno",
        "Dejar listo el equipo para la primera practica tecnica",
        "45-60 min antes de la clase 2",
        "Individual",
        "Ordenador personal y acceso a internet",
        (
            "Instalar y verificar uv, Git y, si corresponde, Git Bash. Crear "
            "ademas una cuenta de Databricks Free Edition para poder empezar la "
            "practica de MLflow en la clase 2."
        ),
        [
            "Esta practica es de puesta a punto: no exige analizar un notebook ni entregar una ficha de riesgos.",
            "Si una herramienta ya esta instalada, conserva la instalacion y verifica su version.",
            "En Windows, Git Bash se instala como parte de Git for Windows; en macOS y Linux se usa la terminal del sistema.",
            "En Databricks selecciona Free Edition, no Free Trial, y no introduzcas datos de pago.",
        ],
        [
            "Documentacion oficial de instalacion de uv",
            "Instalador oficial de Git; Git for Windows incluye Git Bash",
            "Pagina oficial de alta de Databricks Free Edition",
            "Una terminal local y un navegador actualizado",
        ],
        [
            ("Comprueba el punto de partida", "Abre una terminal y verifica si ya responden uv --version y git --version. En Windows, abre tambien Git Bash y ejecuta bash --version."),
            ("Instala uv", "Sigue el instalador oficial para tu sistema operativo. Cierra y abre de nuevo la terminal si el comando no aparece en PATH."),
            ("Instala Git y Git Bash", "En Windows usa Git for Windows y confirma que Git Bash aparece en el menu de aplicaciones. En macOS o Linux instala Git y verifica la terminal disponible."),
            ("Crea el workspace", "Registra una cuenta de Databricks Free Edition, completa el alta y comprueba que puedes entrar en tu workspace sin iniciar un trial de pago."),
            ("Prepara la evidencia", "Anota sistema operativo, versiones de uv y Git, resultado de bash --version cuando aplique y la confirmacion de acceso al workspace. Oculta correos, tokens y datos personales."),
        ],
        [
            ("Checklist de herramientas", "Sistema operativo, version de uv, version de Git y version de Bash cuando corresponda."),
            ("Acceso a Databricks", "Confirmacion de entrada al workspace de Free Edition, sin credenciales ni datos de pago."),
            ("Incidencias", "Si algo falla, mensaje de error, paso intentado y siguiente accion; no basta con decir que no funciona."),
        ],
        [
            "uv --version devuelve una version y el comando funciona en una terminal nueva.",
            "git --version devuelve una version; en Windows Git Bash tambien abre y ejecuta bash --version.",
            "La cuenta de Databricks permite entrar en un workspace Free Edition.",
            "La evidencia permite al docente identificar rapidamente quien esta bloqueado y por que.",
            "No se entregan contrasenas, tokens, correos completos ni datos de pago.",
        ],
        [("uv y verificacion", "3"), ("Git y Git Bash", "3"), ("Databricks Free Edition", "3"), ("Evidencia y seguridad", "1")],
        [
            "Ejecutar uv --version.",
            "Ejecutar git --version.",
            "En Windows, abrir Git Bash y ejecutar bash --version.",
            "Entrar en el workspace de Databricks Free Edition.",
        ],
        [
            "No instales todavia las dependencias del proyecto: la estructura y el entorno del repositorio se trabajaran en S2.",
            "No selecciones Free Trial ni introduzcas tarjeta para esta asignatura.",
            "No compartas credenciales ni capturas con informacion personal visible.",
        ],
        [
            "uv: docs.astral.sh/uv/getting-started/installation/",
            "Git: git-scm.com/install/",
            "Git for Windows: gitforwindows.org/",
            "Databricks Free Edition: docs.databricks.com/aws/en/getting-started/free-edition",
        ],
    ),
    assignment(
        1,
        2,
        "Ciclo observable de ML y AgentOps",
        "Runs comparables, gate, Registry, API local y evaluacion",
        "2 horas en clase + trabajo autonomo",
        "Parejas en Databricks Free Edition",
        "Assignment 1.1 completado y acceso a Databricks",
        (
            "Construir evidencia trazable de un ciclo de ML: comparar candidatos, "
            "aplicar un gate sin contaminar test, registrar el ganador, servirlo "
            "localmente y completar una traza y evaluacion determinista de agente."
        ),
        [
            "La clase 1 deja preparado el equipo y el workspace; la ficha de operacion se construye dentro de esta practica.",
            "El modo obligatorio de AgentOps/LLMOps es determinista; una llamada real a un endpoint es opcional y solo se hace si el docente lo indica.",
            "Cada run debe ser comparable: mismo split, nombres estables, tags de contexto y artefactos auditables.",
            "La API local es una practica de contrato y observabilidad; no es un despliegue publico ni sustituye Model Serving.",
        ],
        [
            "notebooks/01_tracking_mlops.ipynb",
            "notebooks/02_agent_llmops.ipynb con USE_LLM = False",
            "Databricks Experiments, Unity Catalog si esta disponible y el entorno verificado en S1.1",
            "exercise/01_tracking_mlops y exercise/02_agent_llmops como guias de detalle",
        ],
        [
            ("Configura el contexto", "Usa un alias de equipo no personal, el dataset de la practica y un experimento reconocible. No registres secretos, correos ni datos sensibles."),
            ("Genera candidatos", "Ejecuta seis candidatos con los mismos datos de particion. Registra parametros, metricas de entrenamiento/validacion, tags y artefactos auxiliares."),
            ("Aplica el gate", "Define una regla reproducible sobre validacion, descarta candidatos que no la cumplen y abre el test reservado solo para el ganador."),
            ("Registra y sirve", "Registra el modelo ganador, asigna el alias Champion si el entorno lo permite y prueba la API local con casos de exito y error. Apagala al terminar."),
            ("Traza y evalua", "Ejecuta el agente determinista, localiza route_question y retrieve_course_context, corre el scorer y explica por que no basta para autorizar produccion."),
        ],
        [
            ("Tabla de runs", "Seis runs con nombres, parametros, metricas, tags y artefactos."),
            ("Decision de modelo", "Regla del gate, ganador, test reservado, version y alias."),
            ("API local", "Resultados de checks validos e invalidos, identificador del run y apagado confirmado."),
            ("AgentOps/LLMOps", "Identificador de traza, scorer ejecutado y limite del criterio."),
            ("Ficha de operacion", "Experimento, gate, riesgos observados y evidencia nueva o pendiente."),
        ],
        [
            "Los runs contienen contexto suficiente para comparar y reproducir.",
            "El test aparece una sola vez para el ganador y no se usa para escogerlo.",
            "El modelo registrado conserva firma, version y alias cuando el entorno lo permite.",
            "La API muestra exito y errores sin dejar un proceso abierto.",
            "No aparecen secretos ni datos sensibles en runs, trazas o artefactos.",
        ],
        [("Tracking completo", "2"), ("Gate y test reservado", "2"), ("Registry/API", "2"), ("Trazas y evaluacion prudente", "2"), ("Evidencia y seguridad", "2")],
        [
            "Abrir la carpeta semana1 como Git Folder en Databricks.",
            "Ejecutar las celdas sin resolver y completar los TODO.",
            "Abrir Experiments y guardar capturas o enlaces de la tabla de runs.",
            "Entregar la ficha junto con identificadores de runs, traza y artefactos.",
        ],
        [
            "No compartas tokens personales ni copies credenciales al notebook.",
            "El alias Champion no equivale a aprobacion para produccion.",
            "Si Registry no esta disponible, documenta la limitacion y conserva la evidencia de tracking y API local.",
        ],
        [
            "semana1/modules/01-mlflow-databricks-foundations/exercises/01_tracking_mlops/README.md",
            "semana1/modules/01-mlflow-databricks-foundations/exercises/02_agent_llmops/README.md",
        ],
    ),
    assignment(
        3,
        1,
        "Lienzo de inferencia, contratos y preprocesado",
        "Especificar la frontera antes de escribir el modulo",
        "1 hora teoria + 1 hora demo guiada",
        "Parejas",
        "Entregable S2 y cinco muestras de vino",
        (
            "Definir el contrato que conecta una fila nueva con un modelo ya "
            "entrenado: campos, tipos, rangos, orden del vector, salida y fallos "
            "esperados."
        ),
        [
            "La semana 3 no entrena un modelo nuevo: el artefacto preentrenado lo distribuye el docente.",
            "El objetivo de esta practica es producir una especificacion ejecutable para la clase 2.",
            "sample_id identifica la solicitud pero no entra en el vector numerico del modelo.",
            "El orden de las once caracteristicas es parte del contrato, no un detalle de implementacion.",
        ],
        [
            "assets/03-wine-quality/inference_samples.csv",
            "exercises/01-local-inference/01.01-contract-and-preprocess-canvas/problem/",
            "notebook 01-inferencia-y-contratos-alumno.ipynb",
            "Esquema de salida con quality_band, confidence y versiones",
        ],
        [
            ("Clasifica las piezas", "Separa datos historicos de entrenamiento, artefacto entregado y datos nuevos de inferencia. Justifica que recibe cada frontera."),
            ("Construye la tabla de campos", "Para las once features indica nombre canonico, tipo, unidad, rango razonable y si admite valores ausentes."),
            ("Fija el orden", "Escribe el orden exacto del vector y demuestra por que cambiar dos columnas puede producir una prediccion silenciosamente incorrecta."),
            ("Diseña fallos", "Propone una fila valida, una columna desconocida, una fila fuera de rango y el momento del flujo en el que cada una debe fallar."),
            ("Define aceptacion", "Escribe tres criterios que el modulo de la clase 2 debera demostrar con tests y con un comando local."),
        ],
        [
            ("Tabla de contrato", "Once campos con nombres, tipos, unidades y limites."),
            ("Mapa de flujo", "CSV -> solicitud -> preprocesado -> vector -> artefacto -> prediccion."),
            ("Casos de fallo", "Dos entradas invalidas y etapa de rechazo esperada."),
            ("Criterios de aceptacion", "Tres reglas comprobables para el modulo local."),
        ],
        [
            "No se incluye sample_id en el vector del modelo.",
            "Los nombres y el orden de las once features coinciden con el artefacto de S3.",
            "La salida conserva categoria, confianza, version de modelo y version de preprocesado.",
            "Cada caso invalido tiene una razon y una etapa de fallo definida.",
            "Otra pareja puede implementar el modulo de la clase 2 usando solo el lienzo.",
        ],
        [("Contrato completo", "3"), ("Preprocesado y orden", "3"), ("Casos de fallo", "2"), ("Criterios ejecutables", "2")],
        [
            "Abrir el notebook o la hoja compartida de la practica.",
            "Completar el lienzo y discutirlo con otra pareja.",
            "Guardar una copia en el entregable del proyecto y anotar dudas para la clase 2.",
        ],
        [
            "No escribas todavia contracts.py ni inference.py.",
            "No añadas la etiqueta de calidad a las muestras de entrada.",
            "No confundas una confianza del modelo con una garantia del resultado.",
        ],
        [
            "semana3/modules/03-inference-contracts/exercises/01-local-inference/01.01-contract-and-preprocess-canvas/problem/readme.md",
            "semana3/modules/03-inference-contracts/guides/class-1-practices.md",
        ],
    ),
    assignment(
        3,
        2,
        "Modulo local de inferencia",
        "Convertir el lienzo en un comando reproducible",
        "2 horas",
        "Parejas, learning by doing",
        "Assignment 3.1 y starter con tests",
        (
            "Implementar un modulo local que lea un CSV, valide cada fila, "
            "preprocese en el orden entrenado, cargue el modelo ya entrenado y "
            "escriba predicciones sin dejar una salida parcial si falla una fila."
        ),
        [
            "Trabaja exclusivamente en problem/starter; la carpeta solutions es referencia del debrief.",
            "El `.joblib` ya contiene el estimador, feature_names y model_version; no hay que reentrenarlo.",
            "Las pruebas describen la interfaz publica: contratos, carga, inferencia y CLI.",
            "La implementacion debe dejar preparado el bundle que S4 empaquetara.",
        ],
        [
            "problem/starter/ con pyproject.toml, tests y TODOs",
            "models/wine_quality_classifier.joblib entregado por el docente",
            "assets/inference_samples.csv con cinco muestras",
            "Lienzo de contrato de la clase 1",
        ],
        [
            ("Lee la especificacion", "Ejecuta la suite roja y convierte cada nombre de test en una regla de la API local."),
            ("Implementa contratos", "Completa request y prediction con Pydantic; rechaza extras, tipos imposibles y valores fuera de rango."),
            ("Implementa preprocesado", "Construye un vector estable con las once features y una version explicita; no mezcles sample_id."),
            ("Implementa carga e inferencia", "Valida el payload del artefacto antes de invocar predict/predict_proba y valida la salida resultante."),
            ("Completa el CLI", "Lee todas las filas, acumula predicciones y escribe el CSV solo cuando el conjunto es valido."),
            ("Amplia los errores", "Prueba columna extra, segunda fila invalida y artefacto incompatible; confirma que no queda CSV parcial."),
        ],
        [
            ("Codigo del starter", "contracts.py, preprocess.py, inference.py y predict_file.py completados."),
            ("Tests", "Suite en verde, incluyendo casos de error y ausencia de salida parcial."),
            ("Comando", "CSV de cinco filas con sample_id, categoria, confianza y versiones."),
            ("Nota tecnica", "Responsabilidad de cada modulo y dos decisiones de diseño."),
        ],
        [
            "uv run pytest termina sin fallos.",
            "El cargador comprueba feature_names y la interfaz minima del estimador.",
            "El vector respeta el orden del entrenamiento y excluye sample_id.",
            "Una fila invalida no deja un fichero de salida parcial.",
            "El CSV de salida contiene sample_id, quality_band, confidence, model_version y preprocessing_version.",
        ],
        [("Contratos y validacion", "2"), ("Preprocesado e inferencia", "3"), ("CLI y atomicidad", "3"), ("Tests y explicacion", "2")],
        [
            "cd exercises/01-local-inference/01.02-wine-quality-inference-module/problem/starter",
            "uv sync",
            "uv run pytest",
            "uv run ruff check src tests",
            "uv run ruff format --check src tests",
            "uv run python -m model_inference.predict_file --input assets/inference_samples.csv --output .tmp/wine_predictions.csv",
        ],
        [
            "No leas CSV desde preprocess.py ni cargues joblib desde el CLI.",
            "No subas el artefacto binario al repositorio.",
            "Si el modelo real no esta disponible, usa los clasificadores pequeños de los tests para comprobar la interfaz.",
        ],
        [
            "semana3/modules/03-inference-contracts/exercises/01-local-inference/01.02-wine-quality-inference-module/problem/readme.md",
            "semana3/modules/03-inference-contracts/guides/class-2-workshop.md",
        ],
    ),
    assignment(
        4,
        1,
        "Contrato del artefacto y manifiesto",
        "Decidir que debe viajar con un modelo serializado",
        "1 hora teoria + 1 hora practica guiada",
        "Parejas",
        "Modulo local de S3 y payload joblib legado",
        (
            "Diseñar un bundle inspeccionable que separe el binario del estimador "
            "de los metadatos que permiten validar compatibilidad antes de inferir."
        ),
        [
            "Esta practica no implementa artifact.py: produce las decisiones que la clase 2 convertira en funciones y tests.",
            "El manifiesto debe poder leerlo una persona sin deserializar el estimador.",
            "La compatibilidad incluye schema, modelo, preprocesado, features, etiquetas e interfaz del estimador.",
            "joblib.load exitoso no significa artefacto compatible ni seguro por si solo.",
        ],
        [
            "notebook 01-artefacto-y-manifiesto-alumno.ipynb",
            "payload legado de S3 con estimator, feature_names y model_version",
            "exercises/01.01-artifact-contract/problem/readme.md",
            "Explainer con las seis claves del manifiesto",
        ],
        [
            ("Clasifica el contenido", "Asigna cada dato a model.joblib, manifest.json o codigo: estimador, versiones, nombres, etiquetas y reglas."),
            ("Completa el manifiesto", "Propone schema_version, model_version, preprocessing_version, feature_names, output_labels y estimator_type."),
            ("Escribe invariantes", "Define al menos tres condiciones que deben bloquear la carga o la inferencia antes de escribir resultados."),
            ("Rompe el contrato", "Altera orden de columnas, version de preprocesado, etiqueta de salida y tipo de estimador; predice el error y su etapa."),
            ("Decide la politica de filas", "Explica que debe pasar si la segunda fila de un CSV es invalida y por que no se debe publicar una salida parcial."),
        ],
        [
            ("Tabla de almacenamiento", "Que vive en binario, manifiesto y codigo, con justificacion."),
            ("Manifiesto propuesto", "JSON con las seis claves obligatorias y valores coherentes con S3."),
            ("Matriz de invariantes", "Cambio, comprobacion, error esperado y etapa de rechazo."),
            ("Politica de errores", "Decision sobre filas invalidas y salida atomica."),
        ],
        [
            "feature_names conserva exactamente los nombres y el orden de S3.",
            "preprocessing_version no se confunde con model_version.",
            "output_labels limita las categorias que puede exponer la respuesta.",
            "Se comprueba la interfaz predict/predict_proba del estimador.",
            "La politica de filas evita salidas parciales.",
        ],
        [("Separacion binario/metadatos", "2"), ("Manifiesto e invariantes", "4"), ("Casos invalidos", "2"), ("Decision de atomicidad", "2")],
        [
            "Abrir el notebook guiado o el notebook del alumnado.",
            "Completar el lienzo y contrastarlo con otra pareja.",
            "Guardar el manifiesto propuesto y la matriz de compatibilidad.",
        ],
        [
            "No implementes todavia save_model_bundle ni load_model_bundle.",
            "No presentes el manifiesto como una garantia de seguridad del binario.",
            "El clasificador pequeño del notebook es suficiente para probar la idea.",
        ],
        [
            "semana4/modules/04-model-packaging/exercises/01-model-packaging/01.01-artifact-contract/problem/readme.md",
            "semana4/modules/04-model-packaging/guides/class-1-practices.md",
        ],
    ),
    assignment(
        4,
        2,
        "Bundle serializado y CLI validado",
        "Guardar, cargar y consumir un modelo sin salida parcial",
        "2 horas",
        "Parejas, taller sobre starter",
        "Assignment 4.1 y contratos de S3",
        (
            "Implementar la nueva frontera de empaquetado: manifest.json, "
            "model.joblib, carga validada, inferencia validada y CLI que procesa "
            "todas las filas antes de publicar el resultado."
        ),
        [
            "Trabaja en problem/starter; contracts.py y preprocess.py de S3 ya estan preparados.",
            "Los tests usan un DummyClassifier para evitar descargas y binarios grandes.",
            "La carga debe validar metadatos antes de deserializar el objeto.",
            "El bundle sera la dependencia comun de la interfaz Streamlit de S5 y la API posterior.",
        ],
        [
            "problem/starter/ con TODOs en artifact.py y predict_file.py",
            "tests/ como especificacion ejecutable",
            "Lienzo de la clase 1",
            "CSV de muestras de semana 3 y bundle real opcional del docente",
        ],
        [
            ("Implementa el manifiesto", "Completa ArtifactManifest y create_manifest con campos estrictos, versiones, orden y etiquetas."),
            ("Implementa el guardado", "Escribe manifest.json y model.joblib de forma reproducible y valida la interfaz del estimador."),
            ("Implementa la carga", "Rechaza archivos ausentes, JSON incompatible y estimadores no compatibles antes de inferir."),
            ("Valida la salida", "Completa infer_wine_quality y exige etiqueta, confianza, modelo y preprocesado validos."),
            ("Completa el CLI", "Lee, valida e infiere todas las filas; abre la salida solo al final y conserva el esquema estable."),
            ("Añade un caso de fallo", "Incluye un manifest corrupto, una fila fuera de rango o una salida de modelo no permitida y prueba su mensaje."),
        ],
        [
            ("Bundle", "Directorio con manifest.json y model.joblib generado localmente."),
            ("Tests", "Suite en verde para guardado, carga, incompatibilidad, salida y CLI."),
            ("CSV de inferencia", "Salida con cinco predicciones y metadatos de version."),
            ("Nota de compatibilidad", "Dos ejemplos de cambios que deben bloquearse y por que."),
        ],
        [
            "El manifiesto no admite campos desconocidos ni versiones incompatibles.",
            "La carga valida el manifiesto antes de deserializar el estimador.",
            "La salida del modelo cumple el contrato de S3.",
            "Una fila posterior invalida no deja CSV publicado.",
            "El comando funciona sin depender del estado del notebook.",
        ],
        [("Manifiesto y guardado", "3"), ("Carga e inferencia", "3"), ("CLI y atomicidad", "2"), ("Tests y extension", "2")],
        [
            "cd exercises/01-model-packaging/01.02-serializable-inference-module/problem/starter",
            "uv sync",
            "uv run pytest",
            "uv run ruff check src tests",
            "uv run ruff format --check src tests",
            "uv run python -m model_packaging.predict_file --bundle models/wine_quality_bundle --input ../semana3/assets/03-wine-quality/inference_samples.csv --output .tmp/wine_predictions.csv",
        ],
        [
            "No dupliques el contrato ni el preprocesado de S3.",
            "No subas model.joblib al repositorio si la carpeta models esta ignorada.",
            "El bundle solo debe cargarse desde una fuente de confianza.",
        ],
        [
            "semana4/modules/04-model-packaging/exercises/01-model-packaging/01.02-serializable-inference-module/problem/readme.md",
            "semana4/modules/04-model-packaging/guides/class-2-workshop.md",
        ],
    ),
    assignment(
        5,
        1,
        "Contrato de formulario y Streamlit basico",
        "Traducir el contrato de S4 a una primera pantalla",
        "1 hora teoria + 1 hora demo guiada",
        "Parejas",
        "Bundle de S4 y app mental de Streamlit",
        (
            "Diseñar una interfaz minima para que una persona introduzca los once "
            "campos del contrato, envie una peticion completa y entienda el "
            "resultado sin conocer el modelo."
        ),
        [
            "S5 no vuelve a entrenar, preprocesar ni cargar joblib desde app.py: usa un gateway.",
            "El formulario evita inferir con cada cambio de widget.",
            "La app basica no introduce aun session_state, cache_resource ni maquina de estados; eso pertenece a S6.",
            "La tabla de campos sera el acuerdo que implementara la practica 5.2.",
        ],
        [
            "manifest_example.json de S4",
            "assets/03-wine-quality/inference_samples.csv",
            "notebook 01-streamlit-basics-guiada.ipynb",
            "exercises/01-ui-form-contract/problem/",
        ],
        [
            ("Predice el rerun", "Explica que lineas se ejecutan al cambiar un widget y al enviar un formulario; anota que no queda persistente."),
            ("Diseña el formulario", "Para cada feature fija label, widget, tipo, minimo, maximo y valor inicial sin cambiar el nombre del contrato."),
            ("Define el momento de inferencia", "Describe por que `st.form_submit_button` debe ser el unico disparador de la peticion."),
            ("Diseña la salida", "Decide que mostrar: categoria, confianza reportada, version de modelo, version de preprocesado y mensaje de limite."),
            ("Prepara S6", "Escribe dos limitaciones de esta app que una interfaz avanzada debera resolver."),
        ],
        [
            ("Tabla del formulario", "Los once campos con mapeo contrato -> widget y limites."),
            ("Mapa de rerun", "Prediccion de comportamiento al editar y enviar."),
            ("Boceto de resultado", "Categoria, confianza, versiones y error basico."),
            ("Handoff a S6", "Dos limitaciones concretas y observables."),
        ],
        [
            "La tabla contiene exactamente las once features del contrato.",
            "No se infiere al cambiar un widget, solo al enviar el formulario.",
            "El resultado conserva versiones y no promete certeza.",
            "El diseño no introduce un contrato paralelo al de S4.",
            "Otra pareja puede implementar la pantalla leyendo la tabla.",
        ],
        [("Mapeo de contrato", "3"), ("Modelo de rerun", "2"), ("Diseño de resultado", "3"), ("Handoff a S6", "2")],
        [
            "Abrir el notebook guiado y el lienzo de contrato.",
            "Completar la tabla y contrastar tres filas con S4.",
            "Guardar el diseño como especificacion de la practica 5.2.",
        ],
        [
            "No implementes aun session_state ni cache_resource.",
            "Los limites de widgets ayudan a UX, pero la validacion definitiva queda en el gateway.",
            "La confianza es una señal del modelo, no una garantía.",
        ],
        [
            "semana5/modules/05-streamlit-basic-model-ui/exercises/01-ui-form-contract/problem/README.md",
            "semana5/modules/05-streamlit-basic-model-ui/guides/class-1-practices.md",
        ],
    ),
    assignment(
        5,
        2,
        "Primera interfaz Streamlit del modelo",
        "Implementar formulario, gateway y resultado visible",
        "2 horas",
        "Parejas, taller sobre starter",
        "Assignment 5.1 y gateway preparado",
        (
            "Completar una app Streamlit minima que consuma el gateway de S4, "
            "presente una prediccion y traduzca un fallo de inferencia a un mensaje "
            "comprensible."
        ),
        [
            "El starter trae contrato, gateway demo, adaptador del bundle y presentacion minima; el foco es app.py.",
            "La solucion de S5 se convertira literalmente en el punto de partida de S6.",
            "DemoGateway permite trabajar sin un binario; MODEL_UI_BUNDLE activa el bundle real.",
            "La app no debe importar ni llamar predict_proba directamente.",
        ],
        [
            "exercises/02-first-streamlit/problem/starter/",
            "Tabla del formulario de la practica 5.1",
            "DemoGateway o bundle de S4",
            "Streamlit instalado como extra de app",
        ],
        [
            ("Lee el starter", "Ejecuta los tests y localiza FEATURE_FIELDS, collect_values, gateway.predict y render_prediction."),
            ("Implementa el formulario", "Dibuja los once number_input dentro de st.form y devuelve submitted junto con un diccionario de nombres canonicos."),
            ("Conecta el gateway", "Invoca `predict(values)` solo cuando el formulario se envia; no copies preprocesado ni carga de joblib."),
            ("Presenta el resultado", "Muestra categoria, confianza, model_version y preprocessing_version con copy corto y honesto."),
            ("Gestiona un error", "Simula bundle ausente o entrada invalida y muestra un error util sin traceback para la persona."),
            ("Documenta el limite", "Anota que el resultado se pierde o se reconstruye tras un rerun y por que S6 necesitara estado."),
        ],
        [
            ("App funcional", "Formulario completo y boton que ejecuta la inferencia."),
            ("Resultado", "Categoria, confianza y versiones visibles."),
            ("Error", "Caso de fallo reproducible con mensaje y siguiente accion."),
            ("Evidencia", "Captura o registro de la app y nota de dos limites para S6."),
        ],
        [
            "La app arranca con DemoGateway desde checkout limpio.",
            "Los once widgets respetan nombres y rangos del contrato.",
            "La inferencia solo ocurre al enviar el formulario.",
            "La pantalla muestra categoria, confianza y versiones.",
            "No hay logica de entrenamiento, predict_proba ni joblib.load en app.py.",
        ],
        [("Formulario y contrato", "3"), ("Integracion del gateway", "2"), ("Presentacion y error", "3"), ("Evidencia y limite", "2")],
        [
            "cd modules/05-streamlit-basic-model-ui/exercises/02-first-streamlit/problem/starter",
            "uv sync",
            "uv run pytest",
            "uv run ruff check src tests",
            "uv run ruff format --check src tests",
            "uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py",
        ],
        [
            "No añadas aun st.session_state, st.cache_resource ni callbacks complejos.",
            "No subas un modelo binario al repositorio.",
            "La app debe quedar ejecutable para que S6 pueda refactorizarla, no reemplazarla.",
        ],
        [
            "semana5/modules/05-streamlit-basic-model-ui/exercises/02-first-streamlit/README.md",
            "semana5/modules/05-streamlit-basic-model-ui/guides/class-2-workshop.md",
        ],
    ),
    assignment(
        6,
        1,
        "Mapa de estado de la app de S5",
        "Diseñar reruns, cache, estados y recuperacion",
        "1 hora teoria + 1 hora demo guiada",
        "Parejas",
        "App funcional de S5",
        (
            "Inspeccionar la app de S5 y especificar que debe persistir, que debe "
            "cachearse, que eventos producen cada transicion y que debe ver la "
            "persona durante una inferencia."
        ),
        [
            "S6 no rediseña el formulario: conserva FEATURE_FIELDS, collect_values y el gateway de S5.",
            "Una variable local puede desaparecer al rerun; session_state conserva estado de sesion, no sustituye un almacen de datos.",
            "cache_resource es para el gateway o bundle reutilizable, no para respuestas personales.",
            "Una respuesta valida pero lenta sigue siendo success con una señal tecnica.",
        ],
        [
            "App de S5 entregada por la pareja o solucion base",
            "exercises/01-ui-contract/problem/01-estado-streamlit-alumno.ipynb",
            "Contrato y manifest de S4",
            "Demo guiada de estados de S6",
        ],
        [
            ("Inspecciona S5", "Localiza formulario, gateway, llamada predict y puntos donde un rerun puede perder el resultado."),
            ("Diseña session_state", "Decide claves minimas para last_state, telemetry y valores de retry; justifica que no guardaras en telemetria."),
            ("Diseña la cache", "Indica que funcion se envuelve con st.cache_resource y por que no debe cachearse el payload de una persona."),
            ("Define transiciones", "Completa idle -> loading -> success/error con evento, mensaje, accion permitida y evidencia."),
            ("Diseña recuperacion", "Incluye entrada invalida, bundle ausente, fallo transitorio, retry y clear sin borrar telemetria."),
        ],
        [
            ("Contrato de sesion", "Claves, tipos, ciclo de vida y politica de limpieza."),
            ("Maquina de estados", "Tabla de estados, eventos, mensajes, acciones y evidencia."),
            ("Decision de cache", "Recurso cacheable, argumento de cache y dato excluido."),
            ("Plan de implementacion", "Relacion entre requisitos, funciones y tests de la practica 6.2."),
        ],
        [
            "El diseño parte de una limitacion observable de S5.",
            "Distingue estado de sesion, recurso cacheado y datos de una peticion.",
            "Las transiciones tienen eventos y acciones observables.",
            "La confianza no se presenta como certeza ni la latencia como error de modelo.",
            "Otra pareja puede implementar el taller sin inventar estados.",
        ],
        [("Lectura de S5", "2"), ("Estado y cache", "3"), ("Transiciones y recuperacion", "3"), ("Plan implementable", "2")],
        [
            "Abrir la app de S5 y el notebook de diseño.",
            "Completar tablas de estado, cache y transiciones.",
            "Contrastar el plan con los tests del starter de la practica 6.2.",
        ],
        [
            "No copies el formulario para crear una segunda app.",
            "No guardes los valores completos de entrada en Telemetry.",
            "Los umbrales de confianza y latencia son politicas de UX de la demo, no calibracion del modelo.",
        ],
        [
            "semana6/modules/06-ux-model-consumption/exercises/01-ui-contract/problem/README.md",
            "semana6/modules/06-ux-model-consumption/guides/class-1-practices.md",
        ],
    ),
    assignment(
        6,
        2,
        "Evolucion robusta de la interfaz de S5",
        "Estado explicito, gateway cacheado y UX operable",
        "2 horas",
        "Parejas, refactor sobre snapshot",
        "Assignment 6.1 y app de S5",
        (
            "Refactorizar la app de S5 para soportar reruns de forma explicita, "
            "conservar el ultimo resultado, comunicar loading/success/error, "
            "reintentar fallos y registrar telemetria agregada sin payloads."
        ),
        [
            "El starter es un snapshot de S5: el formulario y el gateway ya estan hechos.",
            "Los TODO nuevos estan en session.py, policies.py, presentation.py, controller.py y app.py.",
            "PredictionController no importa Streamlit; en S7 la misma frontera podra consumir HTTP.",
            "El resultado lento sigue siendo valido: above_target es una señal, no un error de contrato.",
        ],
        [
            "exercises/02-robust-streamlit/problem/starter/",
            "Tests de controller, presentation, gateway, session y telemetry",
            "Snapshot de S5 con sus once campos",
            "DemoGateway, UnavailableGateway y politicas proporcionadas",
        ],
        [
            ("Completa la sesion", "Inicializa de forma idempotente last_state, telemetry y last_values; clear vuelve a idle sin borrar contadores."),
            ("Implementa politicas", "Clasifica confianza low/medium/high y latencia within_target/above_target con limites explicitos."),
            ("Construye la vista", "Traduce PredictionPayload a un view model con copy seguro, versiones y mensaje de latencia."),
            ("Implementa el controlador", "Emite loading, mide latencia, valida la salida, traduce excepciones, crea request_id y registra agregados."),
            ("Cablea Streamlit", "Usa cache_resource para el gateway, session_state para estado observable, placeholder/status para loading y botones de retry/clear."),
            ("Prueba cuatro recorridos", "Exito, error de contrato, bundle ausente y respuesta lenta; verifica que no se muestran traceback ni features en telemetry."),
        ],
        [
            ("Diff de evolucion", "Identifica que se conserva de S5 y que se añade en S6."),
            ("App avanzada", "Resultado persistente, cache, loading, error, retry y clear funcionales."),
            ("Tests", "Suite verde y casos de confianza/latencia comprobados."),
            ("Telemetria", "Snapshot con contadores, errores, latencias y versiones, sin payload."),
            ("Evidencia visual", "Capturas o registro de exito, fallo, retry y limpieza."),
        ],
        [
            "La app mantiene el formulario y el contrato de S5.",
            "El gateway se carga como recurso y no por cada rerun.",
            "Se observan idle, loading, success y error.",
            "Retry y clear funcionan; clear conserva telemetria.",
            "Confianza y latencia se comunican sin sobreafirmar.",
            "Los errores tienen recuperacion y request_id, sin traceback ni payload.",
        ],
        [("Sesion y cache", "2"), ("Politicas y view model", "2"), ("Controlador", "3"), ("App y UX", "2"), ("Evidencia", "1")],
        [
            "cd modules/06-ux-model-consumption/exercises/02-robust-streamlit/problem/starter",
            "uv sync",
            "uv run pytest",
            "uv run ruff check src tests",
            "uv run ruff format --check src tests",
            "uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py",
        ],
        [
            "No reimplementes collect_values ni el contrato de S4.",
            "No uses cache_resource como cache global de respuestas por usuario.",
            "La solucion docente se consulta en el debrief, no para copiar TODOs.",
        ],
        [
            "semana6/modules/06-ux-model-consumption/exercises/02-robust-streamlit/README.md",
            "semana6/modules/06-ux-model-consumption/guides/class-2-workshop.md",
        ],
    ),
]


def generate(assignment_data: Assignment) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = (
        f"semana{assignment_data.week:02d}_clase{assignment_data.class_number:02d}_"
        f"assignment.pdf"
    )
    output = OUTPUT_DIR / filename
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=25 * mm,
        bottomMargin=22 * mm,
        title=f"Operación de Modelos - Semana {assignment_data.week} Clase {assignment_data.class_number}",
        author="Comillas ICAI - MUIAAp",
        subject=assignment_data.title,
    )
    doc.assignment = assignment_data
    doc.build(
        build_story(assignment_data),
        onFirstPage=header_footer,
        onLaterPages=header_footer,
    )
    return output


def main() -> None:
    for assignment_data in ASSIGNMENTS:
        print(generate(assignment_data))


if __name__ == "__main__":
    main()
