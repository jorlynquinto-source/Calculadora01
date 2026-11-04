import streamlit as st
import re
from itertools import product
import pandas as pd

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="Calculadora Tabla de la Verdad",
    page_icon="🧮",
    layout="centered"
)

# ============================================================
# DISEÑO VISUAL - CSS
# ============================================================
st.markdown("""
<style>

/* Fondo general */
.stApp {
    background-color: #E5E7EB;
}

/* Contenedor principal */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Título principal */
h1 {
    color: #243B53 !important;
    text-align: center;
    font-weight: 800 !important;
}

/* Subtítulos */
h2, h3 {
    color: #334E68 !important;
    font-weight: 700 !important;
}

/* Texto */
p, label {
    color: #334155;
}

/* Botones generales */
.stButton button {
    background-color: #3B82F6;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    transition: 0.2s;
}

/* Efecto al pasar el mouse */
.stButton button:hover {
    background-color: #1D4ED8;
    color: white;
    border: none;
    transform: scale(1.02);
}

/* Botones de variables */
div[class*="st-key-btn_p"] button,
div[class*="st-key-btn_q"] button,
div[class*="st-key-btn_r"] button,
div[class*="st-key-btn_s"] button,
div[class*="st-key-btn_t"] button,
div[class*="st-key-btn_u"] button {
    background-color: #2563EB;
}

/* Botones de operadores */
div[class*="st-key-btn_AND"] button,
div[class*="st-key-btn_OR"] button,
div[class*="st-key-btn_NOT"] button,
div[class*="st-key-btn_XOR"] button,
div[class*="st-key-btn_IMPLIES"] button,
div[class*="st-key-btn_IFF"] button {
    background-color: #8B5CF6;
}

/* Botón principal */
button[kind="primary"] {
    background-color: #16A34A !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: bold !important;
    padding: 12px !important;
}

button[kind="primary"]:hover {
    background-color: #15803D !important;
}

/* Pantalla de expresión */
.stCodeBlock {
    background-color: #1E293B;
    border-radius: 12px;
    padding: 10px;
}

/* Tablas */
.stDataFrame {
    background-color: white;
    border-radius: 12px;
    padding: 8px;
}

/* Métricas */
[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    border-left: 5px solid #3B82F6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Mensajes */
.stAlert {
    border-radius: 12px;
}

/* Separadores */
hr {
    border-color: #CBD5E1;
}

/* Tarjeta del grupo */
.grupo-card {
    background: linear-gradient(145deg, #243B53, #334E68);
    padding: 22px;
    border-radius: 16px;
    color: white;
    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    margin-top: 20px;
}

.grupo-card h3 {
    color: #93C5FD !important;
    text-align: center;
    margin-bottom: 15px;
}

.grupo-card p {
    color: white !important;
    font-size: 16px;
    margin: 12px 0;
}

.grupo-card .integrante {
    background-color: rgba(255,255,255,0.10);
    padding: 10px;
    border-radius: 8px;
    margin: 8px 0;
}

/* Barra lateral */
section[data-testid="stSidebar"] {
    background-color: #CBD5E1;
}

</style>
""", unsafe_allow_html=True)

st.title("🧮 Calculadora de Tabla de la Verdad")
st.markdown(
    "Construye tu expresión haciendo clic. "
    "El resultado se muestra en **0 y 1**."
)

# ============================================================
# GRUPO NÚMERO 4 - BARRA LATERAL
# ============================================================
st.sidebar.markdown("""
<div class="grupo-card">
    <h3>👥 GRUPO N.º 4</h3>
    <hr style="border-color: #64748B;">
    <p><b>Integrantes:</b></p>
    <div class="integrante">👤 Ariel</div>
    <div class="integrante">👤 Nallely</div>
    <div class="integrante">👤 Geremy</div>
    <hr style="border-color: #64748B;">
    <p style="text-align:center; font-size:13px;">
        🎓 Estructuras Discretas
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# ESTADO DE LA SESIÓN
# ============================================================
if "expr" not in st.session_state:
    st.session_state.expr = ""

# ============================================================
# CONSTRUCTOR DE EXPRESIÓN
# ============================================================
st.subheader("🛠️ Constructor de Expresión")

# Variables
st.markdown("**Variables:**")
cols = st.columns(6)
variables = ["p", "q", "r", "s", "t", "u"]

for i, v in enumerate(variables):
    with cols[i % 6]:
        if st.button(
            f"{v}",
            key=f"btn_{v}",
            use_container_width=True
        ):
            st.session_state.expr += f" {v} "

# Operadores
st.markdown("**Operadores:**")
cols = st.columns(6)

operadores = [
    ("∧", "AND"),
    ("∨", "OR"),
    ("¬", "NOT"),
    ("⊕", "XOR"),
    ("→", "IMPLIES"),
    ("↔", "IFF")
]

for i, (symbol, name) in enumerate(operadores):
    with cols[i % 6]:
        if st.button(
            f"{symbol}",
            key=f"btn_{name}",
            use_container_width=True
        ):
            st.session_state.expr += f" {symbol} "

# Paréntesis y controles
col_paren1, col_paren2, col_limpiar, col_borrar = st.columns(4)

with col_paren1:
    if st.button("(", use_container_width=True):
        st.session_state.expr += "("

with col_paren2:
    if st.button(")", use_container_width=True):
        st.session_state.expr += ")"

with col_limpiar:
    if st.button("🗑️ Limpiar Todo", use_container_width=True):
        st.session_state.expr = ""

with col_borrar:
    if st.button("⌫ Borrar Último", use_container_width=True):
        expr = st.session_state.expr.rstrip()
        if expr:
            st.session_state.expr = expr[:-1]

st.markdown("---")

# Preview de la expresión
st.markdown("**Expresión actual:**")
st.code(
    st.session_state.expr.strip() or "(vacío)",
    language="text"
)

# ============================================================
# LÓGICA CENTRAL - PARSER MEJORADO
# ============================================================

def normalizar_expresion(expr: str) -> str:
    """
    Convierte símbolos lógicos a expresiones Python evaluables.
    """
    e = expr.strip()

    # Reemplazar símbolos lógicos
    e = e.replace("∧", " and ")
    e = e.replace("∨", " or ")
    e = e.replace("¬", " not ")
    e = e.replace("⊕", " xor ")

    # Manejar implicación
    e = re.sub(
        r'(\w+)\s*→\s*(\w+)',
        r'(not \1 or \2)',
        e
    )
    e = re.sub(
        r'\(([^()]+)\)\s*→\s*(\w+)',
        r'(not (\1) or \2)',
        e
    )
    e = re.sub(
        r'(\w+)\s*→\s*\(([^()]+)\)',
        r'(not \1 or (\2))',
        e
    )
    e = re.sub(
        r'\(([^()]+)\)\s*→\s*\(([^()]+)\)',
        r'(not (\1) or (\2))',
        e
    )

    # Manejar bicondicional
    e = re.sub(
        r'(\w+)\s*↔\s*(\w+)',
        r'(\1 == \2)',
        e
    )
    e = re.sub(
        r'\(([^()]+)\)\s*↔\s*(\w+)',
        r'((\1) == \2)',
        e
    )
    e = re.sub(
        r'(\w+)\s*↔\s*\(([^()]+)\)',
        r'(\1 == (\2))',
        e
    )
    e = re.sub(
        r'\(([^()]+)\)\s*↔\s*\(([^()]+)\)',
        r'((\1) == (\2))',
        e
    )

    # Limpiar espacios múltiples
    e = re.sub(r'\s+', ' ', e).strip()

    return e


def extraer_variables(expr: str) -> list:
    """Extrae las variables únicas de la expresión."""
    return sorted(set(re.findall(r'\b[p-ut]\b', expr)))


def xor(a, b):
    """Función XOR lógica."""
    return bool(a) != bool(b)


def generar_tabla(expr_raw: str):
    """
    Genera la tabla de verdad completa.
    Retorna: (variables, tabla)
    """
    if not expr_raw.strip():
        return [], []

    expr_norm = normalizar_expresion(expr_raw)
    variables = extraer_variables(expr_norm)

    if not variables:
        return [], []

    tabla = []

    # Generar todas las combinaciones posibles
    for valores in product([0, 1], repeat=len(variables)):

        # Crear entorno de evaluación
        entorno = {
            v: bool(val)
            for v, val in zip(variables, valores)
        }

        entorno['xor'] = xor

        try:
            resultado = eval(
                expr_norm,
                {"__builtins__": {}},
                entorno
            )

            fila = list(valores) + [int(bool(resultado))]
            tabla.append(fila)

        except Exception:
            return [], []

    return variables, tabla


# ============================================================
# EJEMPLOS PREDEFINIDOS
# ============================================================
st.markdown("---")
st.markdown("**Ejemplos rápidos:**")

ejemplos = {
    "p ∧ q": "Conjunción simple",
    "p ∨ q": "Disyunción simple",
    "p ⊕ q": "XOR",
    "p → q": "Condicional",
    "p ↔ q": "Bicondicional",
    "¬p": "Negación",
    "(p → q) ↔ (¬q → ¬p)": "Ley de contrarrecíproca",
    "p ∨ ¬p": "Tautología",
    "p ∧ ¬p": "Contradicción"
}

cols = st.columns(3)

for i, (expr, desc) in enumerate(ejemplos.items()):
    with cols[i % 3]:
        if st.button(
            f"{expr}",
            key=f"ejemplo_{i}",
            use_container_width=True
        ):
            st.session_state.expr = expr

st.markdown("---")

# ============================================================
# GENERAR TABLA
# ============================================================
if st.button(
    "🚀 Generar Tabla",
    type="primary",
    use_container_width=True
):

    if not st.session_state.expr.strip():
        st.warning("⚠️ Ingresa o construye una expresión primero.")

    else:
        vars_encontradas, tabla = generar_tabla(
            st.session_state.expr
        )

        if not vars_encontradas:
            st.error(
                "❌ Expresión inválida o sin variables detectadas."
            )

            st.info("""
            **Posibles causas:**
            - Variables no válidas (usa solo: p, q, r, s, t, u)
            - Operadores mal escritos
            - Paréntesis desbalanceados
            """)

        else:
            # Crear DataFrame
            cols_df = vars_encontradas + ["Resultado"]
            df = pd.DataFrame(tabla, columns=cols_df)

            # Mostrar resultados
            st.success(
                f"✅ Tabla generada para "
                f"{len(vars_encontradas)} variable(s) - "
                f"{len(tabla)} filas"
            )

            # Clasificar tipo de proposición
            resultados = df["Resultado"].tolist()

            if all(r == 1 for r in resultados):
                st.info(
                    "📊 **Tipo: TAUTOLOGÍA** "
                    "(siempre verdadera)"
                )

            elif all(r == 0 for r in resultados):
                st.error(
                    "📊 **Tipo: CONTRADICCIÓN** "
                    "(siempre falsa)"
                )

            else:
                st.info(
                    "📊 **Tipo: CONTINGENCIA** "
                    "(depende de los valores)"
                )

            # Mostrar tabla
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # Estadísticas
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total de filas", len(tabla))

            with col2:
                verdaderos = sum(resultados)
                st.metric("Verdaderos (1)", verdaderos)

            with col3:
                falsos = len(tabla) - verdaderos
                st.metric("Falsos (0)", falsos)

            # Descargar CSV
            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "📥 Descargar CSV",
                csv,
                "tabla_verdad.csv",
                "text/csv",
                use_container_width=True
            )

# ============================================================
# GUÍA DE REFERENCIA
# ============================================================
with st.expander("📚 Guía de Operadores"):

    st.markdown("""
    | Símbolo | Nombre | Significado |
    |:-------:|:-------|:------------|
    | **∧** | Conjunción | AND - Verdadero si AMBOS son verdaderos |
    | **∨** | Disyunción | OR - Verdadero si al menos UNO es verdadero |
    | **¬** | Negación | NOT - Invierte el valor |
    | **⊕** | XOR | Verdadero si son DIFERENTES |
    | **→** | Condicional | Falso solo si p=1 y q=0 |
    | **↔** | Bicondicional | Verdadero si ambos son IGUALES |

    **Variables permitidas:** p, q, r, s, t, u

    **Ejemplos:**
    - `p ∧ q` → Conjunción simple
    - `(p ∨ q) → r` → Condicional con disyunción
    - `¬p ⊕ q` → XOR con negación
    - `(p → q) ↔ (¬q → ¬p)` → Ley de contrarrecíproca
    """)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")

st.markdown("""
<div style="
    text-align: center;
    color: #64748B;
    font-size: 0.9em;
    padding: 10px;
">
    <p>🎓 <strong>Estructuras Discretas</strong> - Ingeniería en Software</p>
    <p>💻 Desarrollado con Python y Streamlit</p>
    <p>👥 Grupo N.º 4 - Ariel, Nayeli y Jeremy</p>
</div>
""", unsafe_allow_html=True)