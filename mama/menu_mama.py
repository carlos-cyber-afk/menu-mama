import streamlit as st
import requests
import random
from datetime import datetime

# ==================== MENSAJES DE AMOR ====================
mensajes_amor = [
    "Mamá, gracias por ser mi hogar, mi apoyo y mi mayor bendición. Te amo con todo mi corazón.",
    "Cada día estoy más agradecido de tenerte como mamá. Eres la mejor del mundo ❤️",
    "Mamá, tu amor es la receta más deliciosa de mi vida. Gracias por todo.",
    "Aunque no siempre lo diga, eres la persona más importante de mi vida. Te quiero muchísimo.",
    "Mamá, tu sonrisa ilumina mis días. Gracias por ser tan increíble.",
    "No hay nadie como tú. Eres mi ejemplo, mi amiga y mi todo. Te amo infinito.",
    "Por todas las veces que cocinaste con amor... Gracias mamá ❤️",
]

def get_mensaje_del_dia():
    dia_del_año = datetime.now().timetuple().tm_yday
    return mensajes_amor[dia_del_año % len(mensajes_amor)]

# ==================== CONFIGURACIÓN ====================
st.set_page_config(page_title="Para Mamá ❤️", layout="centered", initial_sidebar_state="collapsed")

if 'pantalla' not in st.session_state:
    st.session_state.pantalla = "bienvenida"

# ===================== PANTALLA DE BIENVENIDA =====================
if st.session_state.pantalla == "bienvenida":
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #1a0033, #4a0033); }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <h1 style='text-align: center; color: #ff69b4; margin-top: 60px; font-size: 42px;'>
        ❤️ Para la mejor mamá del mundo ❤️
        </h1>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='background: rgba(255,255,255,0.95); padding: 45px 30px; border-radius: 25px; 
                    margin: 40px auto; max-width: 700px; box-shadow: 0 15px 35px rgba(255,105,180,0.3);
                    text-align: center; font-size: 24px; line-height: 1.5; color: #333; border: 3px solid #ff69b4;'>
            {get_mensaje_del_dia()}
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🍽️ Ver Menús Semanales", type="primary", use_container_width=True):
            st.session_state.pantalla = "app"
            st.rerun()

# ===================== APLICACIÓN PRINCIPAL =====================
else:
    st.title("🍽️ Menú Semanal Inteligente")
    st.markdown("### ¿Qué ingredientes tienes en casa?")

    st.info("💡 **Consejo**: Una vez cargadas las recetas, toca los 3 puntos ⋮ en Chrome → 'Traducir' para ver todo en español")

    ingredientes_input = st.text_input(
        "Ingredientes (separados por coma):", 
        placeholder="pollo, arroz, tomate, cebolla, papa..."
    )

    col1, col2, col3 = st.columns(3)
    num_personas = col2.number_input("Número de personas", min_value=1, value=4)
    modo_random = col3.checkbox("Sin ingredientes → Recetas aleatorias", value=False)

    if st.button("🎲 Generar Opciones de Menú", type="primary", use_container_width=True):
        st.info("Buscando recetas...")

        opciones = ["A", "B", "C", "D", "E", "F", "G"]
        
        for letra in opciones:
            with st.expander(f"🍽️ **Opción {letra}**", expanded=False):
                
                if ingredientes_input.strip() and not modo_random:
                    ing = ingredientes_input.split(",")[0].strip()
                    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ing}"
                else:
                    url = "https://www.themealdb.com/api/json/v1/1/random.php"
                
                try:
                    response = requests.get(url)
                    data = response.json()
                    
                    if not data.get("meals"):
                        st.warning("No se encontraron recetas.")
                        continue
                    
                    meal_data = data["meals"][0]
                    meal_id = meal_data["idMeal"]
                    
                    detail = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}").json()
                    meal = detail["meals"][0]
                    
                    st.subheader(meal["strMeal"])
                    st.image(meal["strMealThumb"], use_column_width=True)
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        dificultad = random.choices(["Fácil", "Medio", "Difícil"], weights=[45, 40, 15])[0]
                        st.write(f"**Dificultad:** {dificultad}")
                    with col_b:
                        st.write(f"**Para:** {num_personas} personas")
                    with col_c:
                        st.write(f"**Tipo:** {meal['strCategory']}")
                    
                    st.markdown("**🛒 Ingredientes:**")
                    for i in range(1, 21):
                        ing_name = meal.get(f"strIngredient{i}")
                        ing_measure = meal.get(f"strMeasure{i}")
                        if ing_name and ing_name.strip():
                            st.write(f"- {ing_measure} {ing_name}")
                    
                    st.markdown("**👩‍🍳 Preparación:**")
                    st.write(meal["strInstructions"])
                    
                    if meal.get("strYoutube"):
                        st.video(meal["strYoutube"])
                        
                except:
                    st.error("Error de conexión. Revisa tu internet.")

    if st.button("← Volver al mensaje de inicio"):
        st.session_state.pantalla = "bienvenida"
        st.rerun()

st.caption("Hecho con mucho amor para la mejor mamá del mundo ❤️")
