import streamlit as st
import pandas as pd
import qrcode
import random
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import matplotlib.ticker as ticker

# streamlit run SimuladorEquipos.py

st.set_page_config(page_title="Electricity Market Simulator", layout="wide")

# ==========================================
# 🌐 SISTEMA DE TRADUCCIONES
# ==========================================
LANG_OPTIONS = {"🇬🇧 English": "en", "🇪🇸 Español": "es", "🇫🇷 Français": "fr"}

TRADUCCIONES = {
    "es": {
        "page_title": "Simulador Mercado Eléctrico",
        "language_screen_title": "⚡ Electricity Market Simulator",
        "language_screen_subtitle": "Choose the game language / Elige el idioma / Choisissez la langue",
        "welcome_title": "⚡ ¡Bienvenido! Eres el operador del mercado (REE)",
        "choose_language": "🌐 Elige el idioma de la partida:",
        "generate_room": "👥 Generar Sala",
        "waiting_room": "⚡ Sala de Espera",
        "scan_to_join": "### 📲 ¡Escanea para participar!",
        "registered_companies": "Empresas registradas:",
        "waiting_connections": "Esperando conexiones...",
        "start_game": "🚀 Empezar Partida",
        "need_2_players": "¡Se necesitan al menos 2 empresas!",
        "operator_name": "REE",
        "ree_control": "⚡ REE - Control Central",
        "demand": "🏭 DEMANDA",
        "renewables": "🌱 RENOV.",
        "to_cover": "⚡ A CUBRIR",
        "plant_params": "**📋 Parámetros de las Centrales**",
        "max_power": "Potencia Máxima (MW)",
        "op_cost": "Coste Operativo (€/MWh)",
        "ramp_cost": "Cambio de Potencia (€/MW)",
        "startup_cost": "Coste Arranque/Parada (€)",
        "companies_submitted": "Empresas que han enviado sus ofertas:",
        "clear_market": "⚖️ Casar Mercado",
        "all_offers_required": "⏳ Esperando ofertas de todas las empresas… ({received} de {total})",
        "nobody_offered": "Nadie ha enviado ofertas aún.",
        "blackout_alert": "🚨 ¡ALERTA APAGÓN! 🚨",
        "blackout_msg": "El sistema eléctrico está al borde del colapso. El mercado ha sido anulado.",
        "redo_offers": "🔄 Obligar a rehacer Ofertas",
        "market_price": "💰 Precio Final del Mercado:",
        "next_hour": "⏭️ Avanzar a la Siguiente Hora",
        "final_results": "🎉 ¡La jornada ha terminado! Aquí tenéis los resultados finales.",
        "final_ranking": "🏆 CLASIFICACIÓN FINAL 🏆",
        "medals": ["🥇 1º PUESTO", "🥈 2º PUESTO", "🥉 3º PUESTO", "🏅 4º PUESTO", "🏅 5º PUESTO"],
        "register_title": "🏢 Registro de Empresa",
        "company_name": "Nombre de tu empresa:",
        "accept": "Aceptar",
        "invalid_name": "Nombre inválido o ya en uso.",
        "registered_ok": "✅ ¡Tu empresa **{nombre}** se ha registrado! La partida empezará pronto…",
        "late_arrival": "Llegaste tarde, la partida ya ha empezado.",
        "market_closed": "🎉 ¡El mercado ha cerrado por hoy!",
        "check_screen": "Mira la pantalla del profesor para ver la clasificación final.",
        "hour_label": "HORA",
        "demand_to_cover": "DEMANDA A CUBRIR (MW)",
        "current_balance": "SALDO ACTUAL:",
        "prepare_offer": "📝 Prepara tu Oferta",
        "previous_mw": "Anterior: {mw} MW",
        "offer_sent": "📤 Oferta enviada a REE.",
        "waiting_others": "Esperando a que el resto de empresas envíen y REE case el mercado…",
        "send_offer": "⚖️ Enviar Oferta",
        "blackout_player": "🚨 ¡APAGÓN! No se cubrió la demanda. Prepárate para rehacer la oferta.",
        "market_cleared": "✅ Mercado Casado. Aquí están tus resultados:",
        "offer_power_mw": "Oferta - Potencia (MW)",
        "offer_price": "Oferta - Precio (€/MWh)",
        "sold_power_mw": "Despachado - Potencia (MW)",
        "clearing_price_row": "Precio de Cierre (€/MWh)",
        "income": "Ingresos (€)",
        "op_costs": "Costes Operativos (€)",
        "penalties": "Penalizaciones (€)",
        "net_profit": "Beneficio Neto (€)",
        "total_balance": "💵 SALDO TOTAL:",
        "waiting_host": "Esperando a que el Operador del Mercado inicie la siguiente hora…",
        "room_not_found": "❌ Esta sala no existe o la partida ya terminó.",
        "reconnect_title": "🔄 Reconectar a la partida",
        "reconnect_info": "Tu sesión se ha cerrado. Introduce tu nombre de empresa para reconectarte:",
        "reconnect_btn": "Reconectarme",
        "reconnect_error": "No se encontró ninguna empresa con ese nombre en esta sala.",
        "merit_order_title": "Curva de Oferta (Merit Order)",
        "merit_order_x": "% Demanda Cubierta",
        "merit_order_y": "Precio (€/MWh)",
        "table_company": "Empresa",
        "table_net_profit": "Beneficio Neto (€)",
        "param_label": "Parámetro",
        "final_merit_title": "📊 Curva Merit Order - Histórico",
        "final_hour": "Hora",
        # Nombres de tecnología
        "tech_Nuclear":         "Nuclear ⚛️",
        "tech_Coal":            "Carbón ⚫",
        "tech_CombinedCycle":   "Ciclo Combinado ☁️",
        "tech_Gas":             "Gas ♨️",
    },
    "en": {
        "page_title": "Electricity Market Simulator",
        "language_screen_title": "⚡ Electricity Market Simulator",
        "language_screen_subtitle": "Choose the game language / Elige el idioma / Choisissez la langue",
        "welcome_title": "⚡ Welcome! You are the market operator (TSO)",
        "choose_language": "🌐 Choose the game language:",
        "generate_room": "👥 Create Room",
        "waiting_room": "⚡ Waiting Room",
        "scan_to_join": "### 📲 Scan to join!",
        "registered_companies": "Registered companies:",
        "waiting_connections": "Waiting for connections...",
        "start_game": "🚀 Start Game",
        "need_2_players": "At least 2 companies are required!",
        "operator_name": "TSO",
        "ree_control": "⚡ TSO - Central Control",
        "demand": "🏭 DEMAND",
        "renewables": "🌱 RENEW.",
        "to_cover": "⚡ TO COVER",
        "plant_params": "**📋 Plant Parameters**",
        "max_power": "Max Capacity (MW)",
        "op_cost": "Operating Cost (€/MWh)",
        "ramp_cost": "Ramp Cost (€/MW)",
        "startup_cost": "Start/Stop Cost (€)",
        "companies_submitted": "Companies that have submitted offers:",
        "clear_market": "⚖️ Clear Market",
        "all_offers_required": "⏳ Waiting for all companies to submit… ({received} of {total})",
        "nobody_offered": "Nobody has submitted offers yet.",
        "blackout_alert": "🚨 BLACKOUT ALERT! 🚨",
        "blackout_msg": "The power system is on the verge of collapse. The market has been cancelled.",
        "redo_offers": "🔄 Force re-submission of Offers",
        "market_price": "💰 Final Market Clearing Price:",
        "next_hour": "⏭️ Advance to Next Hour",
        "final_results": "🎉 The trading session is over! Here are the final results.",
        "final_ranking": "🏆 FINAL RANKING 🏆",
        "medals": ["🥇 1st PLACE", "🥈 2nd PLACE", "🥉 3rd PLACE", "🏅 4th PLACE", "🏅 5th PLACE"],
        "register_title": "🏢 Company Registration",
        "company_name": "Your company name:",
        "accept": "Accept",
        "invalid_name": "Invalid name or already in use.",
        "registered_ok": "✅ Your company **{nombre}** has been registered! The game will start soon…",
        "late_arrival": "You arrived late, the game has already started.",
        "market_closed": "🎉 The market has closed for today!",
        "check_screen": "Check the teacher's screen for the final ranking.",
        "hour_label": "HOUR",
        "demand_to_cover": "DEMAND TO COVER (MW)",
        "current_balance": "CURRENT BALANCE:",
        "prepare_offer": "📝 Prepare your Offer",
        "previous_mw": "Previous: {mw} MW",
        "offer_sent": "📤 Offer submitted to TSO.",
        "waiting_others": "Waiting for other companies to submit and TSO to clear the market…",
        "send_offer": "⚖️ Submit Offer",
        "blackout_player": "🚨 BLACKOUT! Demand was not covered. Prepare to resubmit your offer.",
        "market_cleared": "✅ Market Cleared. Here are your results:",
        "offer_power_mw": "Offer - Power (MW)",
        "offer_price": "Offer - Price (€/MWh)",
        "sold_power_mw": "Dispatched - Power (MW)",
        "clearing_price_row": "Clearing Price (€/MWh)",
        "income": "Revenue (€)",
        "op_costs": "Operating Costs (€)",
        "penalties": "Penalties (€)",
        "net_profit": "Net Profit (€)",
        "total_balance": "💵 TOTAL BALANCE:",
        "waiting_host": "Waiting for the Market Operator (Host) to start the next hour…",
        "room_not_found": "❌ This room doesn't exist or the game has ended.",
        "reconnect_title": "🔄 Reconnect to the game",
        "reconnect_info": "Your session has ended. Enter your company name to reconnect:",
        "reconnect_btn": "Reconnect",
        "reconnect_error": "No company with that name was found in this room.",
        "merit_order_title": "Supply Curve (Merit Order)",
        "merit_order_x": "% Demand Covered",
        "merit_order_y": "Price (€/MWh)",
        "table_company": "Company",
        "table_net_profit": "Net Profit (€)",
        "param_label": "Parameter",
        "final_merit_title": "📊 Merit Order Curve - History",
        "final_hour": "Hour",
        # Technology names
        "tech_Nuclear":         "Nuclear ⚛️",
        "tech_Coal":            "Coal ⚫",
        "tech_CombinedCycle":   "Combined Cycle ☁️",
        "tech_Gas":             "Gas ♨️",
    },
    "fr": {
        "page_title": "Simulateur Marché Électrique",
        "language_screen_title": "⚡ Electricity Market Simulator",
        "language_screen_subtitle": "Choose the game language / Elige el idioma / Choisissez la langue",
        "welcome_title": "⚡ Bienvenue ! Vous êtes l'opérateur du marché (RTE)",
        "choose_language": "🌐 Choisissez la langue du jeu :",
        "generate_room": "👥 Créer une Salle",
        "waiting_room": "⚡ Salle d'Attente",
        "scan_to_join": "### 📲 Scannez pour participer !",
        "registered_companies": "Entreprises inscrites :",
        "waiting_connections": "En attente de connexions...",
        "start_game": "🚀 Démarrer la Partie",
        "need_2_players": "Il faut au moins 2 entreprises !",
        "operator_name": "RTE",
        "ree_control": "⚡ RTE - Contrôle Central",
        "demand": "🏭 DEMANDE",
        "renewables": "🌱 RENOUV.",
        "to_cover": "⚡ À COUVRIR",
        "plant_params": "**📋 Paramètres des Centrales**",
        "max_power": "Puissance Maximale (MW)",
        "op_cost": "Coût Opérationnel (€/MWh)",
        "ramp_cost": "Coût de Modulation (€/MW)",
        "startup_cost": "Coût Démarrage/Arrêt (€)",
        "companies_submitted": "Entreprises ayant soumis leurs offres :",
        "clear_market": "⚖️ Équilibrer le Marché",
        "all_offers_required": "⏳ En attente des offres de toutes les entreprises… ({received} sur {total})",
        "nobody_offered": "Personne n'a encore soumis d'offre.",
        "blackout_alert": "🚨 ALERTE COUPURE ! 🚨",
        "blackout_msg": "Le système électrique est au bord de l'effondrement. Le marché a été annulé.",
        "redo_offers": "🔄 Forcer la re-soumission des Offres",
        "market_price": "💰 Prix d'Équilibre Final du Marché :",
        "next_hour": "⏭️ Passer à l'Heure Suivante",
        "final_results": "🎉 La session de trading est terminée ! Voici les résultats finaux.",
        "final_ranking": "🏆 CLASSEMENT FINAL 🏆",
        "medals": ["🥇 1ère PLACE", "🥈 2ème PLACE", "🥉 3ème PLACE", "🏅 4ème PLACE", "🏅 5ème PLACE"],
        "register_title": "🏢 Inscription de l'Entreprise",
        "company_name": "Nom de votre entreprise :",
        "accept": "Accepter",
        "invalid_name": "Nom invalide ou déjà utilisé.",
        "registered_ok": "✅ Votre entreprise **{nombre}** a été enregistrée ! La partie commencera bientôt…",
        "late_arrival": "Vous êtes arrivé en retard, la partie a déjà commencé.",
        "market_closed": "🎉 Le marché a fermé pour aujourd'hui !",
        "check_screen": "Regardez l'écran du professeur pour le classement final.",
        "hour_label": "HEURE",
        "demand_to_cover": "DEMANDE À COUVRIR (MW)",
        "current_balance": "SOLDE ACTUEL :",
        "prepare_offer": "📝 Préparez votre Offre",
        "previous_mw": "Précédent : {mw} MW",
        "offer_sent": "📤 Offre soumise au RTE.",
        "waiting_others": "En attente que les autres entreprises soumettent et que le RTE équilibre le marché…",
        "send_offer": "⚖️ Soumettre l'Offre",
        "blackout_player": "🚨 COUPURE ! La demande n'a pas été couverte. Préparez-vous à re-soumettre.",
        "market_cleared": "✅ Marché Équilibré. Voici vos résultats :",
        "offer_power_mw": "Offre - Puissance (MW)",
        "offer_price": "Offre - Prix (€/MWh)",
        "sold_power_mw": "Dispatché - Puissance (MW)",
        "clearing_price_row": "Prix d'Équilibre (€/MWh)",
        "income": "Revenus (€)",
        "op_costs": "Coûts Opérationnels (€)",
        "penalties": "Pénalités (€)",
        "net_profit": "Bénéfice Net (€)",
        "total_balance": "💵 SOLDE TOTAL :",
        "waiting_host": "En attente que l'Opérateur du Marché lance l'heure suivante…",
        "room_not_found": "❌ Cette salle n'existe pas ou la partie est terminée.",
        "reconnect_title": "🔄 Reconnecter à la partie",
        "reconnect_info": "Votre session s'est fermée. Entrez le nom de votre entreprise pour vous reconnecter :",
        "reconnect_btn": "Me reconnecter",
        "reconnect_error": "Aucune entreprise avec ce nom n'a été trouvée dans cette salle.",
        "merit_order_title": "Courbe d'Offre (Merit Order)",
        "merit_order_x": "% Demande Couverte",
        "merit_order_y": "Prix (€/MWh)",
        "table_company": "Entreprise",
        "table_net_profit": "Bénéfice Net (€)",
        "param_label": "Paramètre",
        "final_merit_title": "📊 Courbe Merit Order - Historique",
        "final_hour": "Heure",
        # Noms des technologies
        "tech_Nuclear":         "Nucléaire ⚛️",
        "tech_Coal":            "Charbon ⚫",
        "tech_CombinedCycle":   "Cycle Combiné ☁️",
        "tech_Gas":             "Gaz ♨️",
    },
}

def t(key, **kwargs):
    lang = st.session_state.get("idioma", "en")
    text = TRADUCCIONES.get(lang, TRADUCCIONES["en"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text


# --- MEMORIA COMPARTIDA ---
@st.cache_resource
def obtener_base_de_datos():
    return {"salas": {}}

db = obtener_base_de_datos()

HORARIOS = [
    {"hora": "08:00 - 09:00", "demanda": 8790, "renovables": 4900},
    {"hora": "09:00 - 10:00", "demanda": 9271, "renovables": 6600},
    {"hora": "10:00 - 11:00", "demanda": 9700, "renovables": 8800},
    {"hora": "11:00 - 12:00", "demanda": 9100, "renovables": 4100},
    {"hora": "12:00 - 13:00", "demanda": 8750, "renovables": 2750},
]

# Internal tech names → display per language (for player results table)
TECH_DISPLAY = {
    "es": {
        "Nuclear":         "☢️ Nuclear",
        "Carbón":          "🪨 Carbón",
        "Ciclo Combinado": "💨 Ciclo",
        "Gas":             "🔥 Gas",
    },
    "en": {
        "Nuclear":         "☢️ Nuclear",
        "Carbón":          "🪨 Coal",
        "Ciclo Combinado": "💨 Combined Cycle",
        "Gas":             "🔥 Gas",
    },
    "fr": {
        "Nuclear":         "☢️ Nucléaire",
        "Carbón":          "🪨 Charbon",
        "Ciclo Combinado": "💨 Cycle Combiné",
        "Gas":             "🔥 Gaz",
    },
}

def tech_display(tech_internal):
    lang = st.session_state.get("idioma", "en")
    return TECH_DISPLAY.get(lang, TECH_DISPLAY["en"]).get(tech_internal, tech_internal)


# ==========================================
# 📊 GRÁFICO MERIT ORDER
# ==========================================
def grafico_merit_order(df_resultado, demanda_residual, precio_marginal):
    """
    Dibuja la curva de oferta (merit order) con:
    - Nombre de cada equipo encima de su(s) columna(s)
    - Soporte correcto para precios negativos
    - Labels de tecnología traducidos
    """
    lang = st.session_state.get("idioma", "en")

    # Internal tech name → translated display name for legend
    TECH_LEGEND = {
        "es": {
            "Nuclear":         "Nuclear ⚛️",
            "Carbón":          "Carbón ⚫",
            "Ciclo Combinado": "Ciclo ☁",
            "Gas":             "Gas ♨",
        },
        "en": {
            "Nuclear":         "Nuclear ⚛️",
            "Carbón":          "Coal ⚫",
            "Ciclo Combinado": "Comb. Cycle ☁",
            "Gas":             "Gas ♨",
        },
        "fr": {
            "Nuclear":         "Nucléaire ⚛️",
            "Carbón":          "Charbon ⚫",
            "Ciclo Combinado": "Cycle Combiné ☁",
            "Gas":             "Gaz ♨",
        },
    }
    DICT_TECH_LEGEND = TECH_LEGEND.get(lang, TECH_LEGEND["en"])

    COLORES_TECH = {
        "Nuclear ⚛️":       "#62ff3b",
        "Coal ⚫":           "#4e4859",
        "Carbón ⚫":         "#4e4859",
        "Charbon ⚫":        "#4e4859",
        "Comb. Cycle ☁":    "#322fc4",
        "Ciclo ☁":          "#322fc4",
        "Cycle Combiné ☁":  "#322fc4",
        "Nucléaire ⚛️":     "#62ff3b",
        "Gas ♨":             "#f7b10c",
        "Gaz ♨":             "#f7b10c",
    }

    df_sorted = df_resultado.copy()
    df_sorted["_tech_legend"] = df_sorted["Tecnología"].map(
        lambda x: DICT_TECH_LEGEND.get(x, x)
    )
    df_sorted = df_sorted.sort_values("Precio (€/MWh)").reset_index(drop=True)
    df_sorted = df_sorted[df_sorted["Potencia Ofertada (MW)"] > 0].copy()

    if df_sorted.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.text(0.5, 0.5, "No power was offered.\nEmpty market.",
                ha='center', va='center', fontsize=15, color="red")
        ax.axis('off')
        return fig

    total_ofertado      = df_sorted["Potencia Ofertada (MW)"].sum()
    min_precio_ofertado = df_sorted["Precio (€/MWh)"].min()
    max_precio_ofertado = df_sorted["Precio (€/MWh)"].max()

    # Límites eje Y con soporte para precios negativos
    y_min = min(0, min_precio_ofertado * 1.3 if min_precio_ofertado < 0 else 0)
    y_max = max(180, precio_marginal * 1.3 if precio_marginal > 0 else 180,
                max_precio_ofertado * 1.1 if max_precio_ofertado > 0 else 180)

    COLOR_EJES = "#7c7c7c"
    COLOR_GRID = "#e8e8e8"

    fig, ax = plt.subplots(figsize=(11, 5.5))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    cumulative = 0
    labels_agregadas = set()
    y_range = y_max - y_min

    for _, row in df_sorted.iterrows():
        tech_leg = row["_tech_legend"]
        mw       = row["Potencia Ofertada (MW)"]
        price    = row["Precio (€/MWh)"]
        equipo   = row["Equipo"]

        x_start = (cumulative / demanda_residual) * 100
        x_width = (mw / demanda_residual) * 100

        within_demand = x_start < 100
        color = COLORES_TECH.get(tech_leg, "#F5B731") if within_demand else "#f3f3f3"
        label_leyenda = tech_leg if (tech_leg not in labels_agregadas and within_demand) else None
        labels_agregadas.add(tech_leg)

        rect_bottom = min(0, price)
        rect_height = abs(price) if price != 0 else 0.5

        rect = plt.Rectangle(
            (x_start, rect_bottom), x_width, rect_height,
            facecolor=color, edgecolor="white", linewidth=1,
            zorder=2, label=label_leyenda
        )
        ax.add_patch(rect)

        # ── Etiqueta del equipo: dentro de la barra si cabe, encima si no ──
        if within_demand and x_width > 1.5:
            cx = x_start + x_width / 2
            bar_h = abs(price)  # altura visual de la barra

            if bar_h > y_range * 0.10:
                # Cabe dentro: texto blanco centrado verticalmente, rotado
                cy = rect_bottom + bar_h / 2
                ax.text(
                    cx, cy, equipo,
                    ha='center', va='center',
                    fontsize=6.5, fontweight='bold',
                    color='white', rotation=90,
                    zorder=7, clip_on=True,
                )
            else:
                # Barra baja: texto pequeño justo encima de la barra
                cy = max(price, 0) + y_range * 0.025
                ax.text(
                    cx, cy, equipo,
                    ha='center', va='bottom',
                    fontsize=6, fontweight='bold',
                    color='#1e3a8a', rotation=90,
                    zorder=7, clip_on=True,
                )

        cumulative += mw

    # Línea de precio marginal
    ax.fill_between([0, 100], y_min, precio_marginal, color="#FEFCE8", alpha=0.6, zorder=0)
    ax.hlines(precio_marginal, 0, 100, colors="#1E3A8A", linestyles="--", linewidth=1.5, zorder=4)
    ax.vlines(100, y_min, precio_marginal, colors="#1E3A8A", linestyles="--", linewidth=1.5, zorder=4)
    ax.plot(100, precio_marginal, "o", color="#fc0303", markersize=8, zorder=5)

    # Línea en y=0 si hay precios negativos
    if y_min < 0:
        ax.hlines(0, 0, (total_ofertado / demanda_residual) * 100,
                  colors="#888888", linestyles="-", linewidth=0.8, zorder=3)

    # Etiqueta del equipo encima de su bloque
    for equipo, (x0, x1, price_top) in equipo_x_ranges.items():
        x_center = (x0 + x1) / 2
        y_top = max(price_top, 0) + (y_max - y_min) * 0.03
        ax.text(
            x_center, y_top, equipo,
            ha='center', va='bottom', fontsize=8, fontweight='bold',
            color='#1e3a8a', zorder=7,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor='#1e3a8a', alpha=0.8, linewidth=0.7)
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLOR_EJES)
    ax.spines["bottom"].set_color(COLOR_EJES)

    x_limit = max(110, (total_ofertado / demanda_residual) * 100)
    ax.set_xlim(-1, x_limit)
    ax.set_ylim(y_min, y_max)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(50))
    ax.xaxis.set_major_formatter(ticker.PercentFormatter())
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d€'))
    ax.grid(axis='y', linestyle='-', color=COLOR_GRID, linewidth=0.5, zorder=1)

    ax.set_xlabel(t("merit_order_x"), fontsize=10, color=COLOR_EJES)
    ax.set_ylabel(t("merit_order_y"), fontsize=10, color=COLOR_EJES)
    ax.set_title(t("merit_order_title"), fontsize=12, fontweight='bold', color='#1e3a8a')

    offset_label = (y_max - y_min) * 0.02
    ax.text(101, precio_marginal + offset_label,
            f"{precio_marginal:,.2f} €",
            fontsize=10, color="#1E3A8A", ha='left', va='bottom',
            fontweight="bold", zorder=6)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.14),
              ncol=4, frameon=False, fontsize=10, handlelength=1.5)

    plt.tight_layout()
    return fig


# ==========================================
# 🔀 ENRUTADOR
# ==========================================
params     = st.query_params
sala_url   = params.get("sala",   None)
equipo_url = params.get("equipo", None)

if sala_url:
    st.session_state.rol          = "jugador"
    st.session_state.sala_activa  = sala_url

    if equipo_url and "mi_equipo" not in st.session_state:
        sala_tmp = db["salas"].get(sala_url, {})
        if equipo_url in sala_tmp.get("equipos", []):
            st.session_state.mi_equipo = equipo_url
            if "idioma" in sala_tmp:
                st.session_state.idioma = sala_tmp["idioma"]
else:
    if "rol" not in st.session_state:
        st.session_state.rol = "host"


# ==========================================
# 👑 VISTA DEL HOST
# ==========================================
if st.session_state.rol == "host":

    # ── PASO 0: ELEGIR IDIOMA (pantalla exclusiva, todo en inglés) ────────────
    if "idioma" not in st.session_state:
        st.markdown(
            "<h1 style='text-align:center;margin-top:60px;'>⚡ Electricity Market Simulator</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center;color:#6b7280;font-size:1.2rem;margin-bottom:40px;'>"
            "Choose the language for this game session"
            "</p>",
            unsafe_allow_html=True,
        )

        col_en, col_es, col_fr = st.columns(3)
        with col_en:
            st.markdown(
                "<div style='text-align:center;font-size:4rem;line-height:1;'>🇬🇧</div>",
                unsafe_allow_html=True,
            )
            if st.button("English", use_container_width=True, type="primary"):
                st.session_state.idioma = "en"
                st.rerun()
        with col_es:
            st.markdown(
                "<div style='text-align:center;font-size:4rem;line-height:1;'>🇪🇸</div>",
                unsafe_allow_html=True,
            )
            if st.button("Español", use_container_width=True, type="primary"):
                st.session_state.idioma = "es"
                st.rerun()
        with col_fr:
            st.markdown(
                "<div style='text-align:center;font-size:4rem;line-height:1;'>🇫🇷</div>",
                unsafe_allow_html=True,
            )
            if st.button("Français", use_container_width=True, type="primary"):
                st.session_state.idioma = "fr"
                st.rerun()
        st.stop()

    # ── PASO 1: CREAR SALA ────────────────────────────────────────────────────
    if "sala_activa" not in st.session_state:
        st.title("⚡ " + t("page_title"))

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"### {t('welcome_title')}")

            if st.button(t("generate_room"), type="primary", use_container_width=True):
                nuevo_pin = str(random.randint(1000, 9999))
                db["salas"][nuevo_pin] = {
                    "estado":  "esperando",
                    "equipos": [],
                    "idioma":  st.session_state.idioma,
                }
                st.session_state.sala_activa = nuevo_pin
                st.rerun()
        st.stop()

    sala_id = st.session_state.sala_activa
    sala    = db["salas"][sala_id]

    if "idioma" in sala:
        st.session_state.idioma = sala["idioma"]

    estado_sala = sala["estado"]

    # ── LOBBY DE ESPERA (HOST) ────────────────────────────────────────────────
    if estado_sala == "esperando":
        st.title(t("waiting_room"))
        URL_BASE       = "https://simuladormercado2-tf9xg2yjxcjjfs5dufe6jl.streamlit.app"
        url_invitacion = f"{URL_BASE}/?sala={sala_id}"

        col_izq, col_der = st.columns([1.2, 0.8])
        with col_izq:
            st.markdown(t("scan_to_join"))
            st.code(url_invitacion)
            equipos_unidos = sala["equipos"]
            st.markdown(f"**{t('registered_companies')} {len(equipos_unidos)}**")

            if len(equipos_unidos) > 0:
                nombres_html = " ".join([
                    f"<span style='background-color:#1e3a8a;color:white;padding:5px 10px;"
                    f"border-radius:8px;margin:3px;display:inline-block;font-size:0.9rem;'>{eq}</span>"
                    for eq in equipos_unidos
                ])
                st.markdown(nombres_html, unsafe_allow_html=True)
            else:
                st.info(t("waiting_connections"))

            st_autorefresh(interval=2000, key="refresh_host_lobby")

        with col_der:
            qr = qrcode.make(url_invitacion)
            st.image(qr.get_image(), width=220)

        st.markdown("<div style='margin-top:-20px;'></div>", unsafe_allow_html=True)

        if st.button(t("start_game"), type="primary", use_container_width=True):
            if len(equipos_unidos) >= 2:
                factor = 4 / len(equipos_unidos)
                sala["estado"] = "jugando"
                sala["TECNOLOGIAS"] = {
                    "Nuclear":         {"pot_max": int(970*factor), "coste_op": 8.0,   "max_cambio": int(100*factor), "coste_cambio": 70,  "coste_pa": 150000},
                    "Carbón":          {"pot_max": int(830*factor), "coste_op": 86.0,  "max_cambio": int(200*factor), "coste_cambio": 50,  "coste_pa": 70000},
                    "Ciclo Combinado": {"pot_max": int(800*factor), "coste_op": 121.0, "max_cambio": int(400*factor), "coste_cambio": 30,  "coste_pa": 10000},
                    "Gas":             {"pot_max": int(500*factor), "coste_op": 168.0, "max_cambio": int(500*factor), "coste_cambio": 0,   "coste_pa": 0},
                }
                sala["dinero_acumulado"]          = {eq: 500000 for eq in equipos_unidos}
                sala["energia_acumulada"]          = {eq: {tech: 0 for tech in sala["TECNOLOGIAS"]} for eq in equipos_unidos}
                sala["ronda_actual"]               = 0
                sala["fase"]                       = "ofertando"
                sala["ofertas"]                    = {}
                sala["potencia_asignada_anterior"] = {}
                sala["hubo_apagon"]                = False
                sala["historico_resultados"]       = []
                st.rerun()
            else:
                st.error(t("need_2_players"))

    # ── JUEGO ACTIVO (HOST) ───────────────────────────────────────────────────
    elif estado_sala == "jugando":
        ronda = sala["ronda_actual"]

        # ── FIN DE JUEGO ──────────────────────────────────────────────────────
        if ronda >= len(HORARIOS):
            st.success(t("final_results"))
            st.balloons()
            st.markdown(f"<h1 style='text-align:center;'>{t('final_ranking')}</h1>",
                        unsafe_allow_html=True)

            clasificacion = sorted(sala["dinero_acumulado"].items(),
                                   key=lambda x: x[1], reverse=True)
            cols_lb  = st.columns(len(sala["equipos"]))
            medallas = t("medals")
            for i, (equipo_lb, saldo_lb) in enumerate(clasificacion):
                with cols_lb[i]:
                    with st.container(border=True):
                        st.markdown(f"<h3 style='text-align:center;'>{medallas[i]}</h3>",
                                    unsafe_allow_html=True)
                        st.markdown(f"<h4 style='text-align:center;'>{equipo_lb}</h4>",
                                    unsafe_allow_html=True)
                        color = "#28a745" if saldo_lb >= 0 else "#dc3545"
                        st.markdown(
                            f"<h2 style='text-align:center;color:{color};'>"
                            f"{saldo_lb:,.0f} €</h2>",
                            unsafe_allow_html=True,
                        )

            # ── GRÁFICAS MERIT ORDER HISTÓRICAS ───────────────────────────────
            historico = sala.get("historico_resultados", [])
            if historico:
                st.markdown(f"## {t('final_merit_title')}")
                for entrada in historico:
                    st.markdown(f"**{t('final_hour')}: {entrada['hora']}**")
                    df_h = pd.DataFrame(entrada["df_records"])
                    fig_h = grafico_merit_order(
                        df_h, entrada["demanda_residual"], entrada["precio_marginal"]
                    )
                    st.pyplot(fig_h)
                    plt.close(fig_h)

                    # Tabla beneficio por equipo en esa hora (traducida)
                    resumen_h = (
                        df_h.groupby("Equipo")["Beneficio Neto (€)"]
                        .sum()
                        .reset_index()
                        .rename(columns={
                            "Equipo":            t("table_company"),
                            "Beneficio Neto (€)": t("table_net_profit"),
                        })
                    )
                    resumen_h[t("table_net_profit")] = resumen_h[
                        t("table_net_profit")
                    ].apply(lambda x: f"{x:,.0f} €")
                    st.table(resumen_h.style.hide(axis="index"))
            st.stop()

        datos_hora       = HORARIOS[ronda]
        demanda_total    = datos_hora["demanda"]
        renovables       = datos_hora["renovables"]
        demanda_residual = demanda_total - renovables
        pct_renovables   = (renovables / demanda_total) * 100
        pct_residual     = 100 - pct_renovables

        st.title(f"{t('ree_control')} | {datos_hora['hora']}")

        # Panel de demanda
        html_visual = f"""
<div style="background-color:#fffbeb;padding:10px;border-radius:10px;border:2px solid #f59e0b;
            margin-bottom:5px;box-shadow:1px 1px 3px rgba(0,0,0,0.05);">
    <div style="display:flex;justify-content:space-around;text-align:center;align-items:center;flex-wrap:wrap;">
        <div style="margin:2px;">
            <p style="color:#b45309;margin:0;font-size:0.8rem;font-weight:bold;">{t('demand')}</p>
            <h3 style="color:#d97706;margin:0;font-size:1.4rem;">{demanda_total} MW</h3>
        </div>
        <div style="font-size:1.2rem;color:#9ca3af;">-</div>
        <div style="margin:2px;">
            <p style="color:#166534;margin:0;font-size:0.8rem;font-weight:bold;">{t('renewables')}</p>
            <h3 style="color:#22c55e;margin:0;font-size:1.4rem;">{renovables} MW</h3>
        </div>
        <div style="font-size:1.2rem;color:#9ca3af;">=</div>
        <div style="margin:2px;padding:2px 10px;background-color:#fef3c7;border-radius:8px;border:1.5px dashed #ea580c;">
            <p style="color:#ea580c;margin:0;font-size:0.8rem;font-weight:bold;">{t('to_cover')}</p>
            <h3 style="color:#ea580c;margin:0;font-size:1.8rem;">{demanda_residual} MW</h3>
        </div>
    </div>
    <div style="margin-top:8px;">
        <div style="width:100%;background-color:#e5e7eb;border-radius:8px;height:18px;display:flex;overflow:hidden;border:1px solid #ccc;">
            <div style="width:{pct_renovables}%;background-color:#22c55e;display:flex;align-items:center;justify-content:center;color:white;font-size:0.7rem;font-weight:bold;">🌱 {pct_renovables:.0f}%</div>
            <div style="width:{pct_residual}%;background-color:#f59e0b;display:flex;align-items:center;justify-content:center;color:white;font-size:0.7rem;font-weight:bold;">🔥 {pct_residual:.0f}%</div>
        </div>
    </div>
</div>"""
        st.markdown(html_visual, unsafe_allow_html=True)

        # Tabla parámetros centrales (traducida)
        with st.container():
            st.markdown(t("plant_params"))
            datos_t = {t("param_label"): [t("max_power"), t("op_cost"), t("ramp_cost"), t("startup_cost")]}
            for tech, info in sala["TECNOLOGIAS"].items():
                datos_t[tech_display(tech)] = [
                    f"{info['pot_max']} ",
                    f"{info['coste_op']} ",
                    f"{info['coste_cambio']} ",
                    f"{info['coste_pa']:,} ",
                ]
            df_host = pd.DataFrame(datos_t)
            st.table(df_host.style.hide(axis="index"))

        # ── FASE: OFERTANDO ───────────────────────────────────────────────────
        if sala["fase"] == "ofertando":
            ofertas_recibidas = len(sala["ofertas"])
            total_equipos     = len(sala["equipos"])
            todas_enviadas    = ofertas_recibidas == total_equipos

            st.metric(t("companies_submitted"), f"{ofertas_recibidas} de {total_equipos}")
            st.progress(ofertas_recibidas / total_equipos)

            st_autorefresh(interval=2000, key="refresh_host_ofertando")

            if not todas_enviadas:
                st.warning(t("all_offers_required",
                             received=ofertas_recibidas, total=total_equipos))

            if st.button(
                t("clear_market"),
                type="primary",
                use_container_width=True,
                disabled=not todas_enviadas,
            ):
                todas_las_ofertas = []
                for lista_equipo in sala["ofertas"].values():
                    todas_las_ofertas.extend(lista_equipo)

                df = pd.DataFrame(todas_las_ofertas)
                df = df.sort_values(by="Precio (€/MWh)").reset_index(drop=True)
                df["Potencia Acumulada (MW)"] = df["Potencia Ofertada (MW)"].cumsum()
                df["Potencia Previa (MW)"]    = df["Potencia Acumulada (MW)"] - df["Potencia Ofertada (MW)"]

                def calcular_asignacion(row):
                    if row["Potencia Previa (MW)"] >= demanda_residual:
                        return 0
                    elif row["Potencia Acumulada (MW)"] <= demanda_residual:
                        return row["Potencia Ofertada (MW)"]
                    else:
                        return demanda_residual - row["Potencia Previa (MW)"]

                df["Potencia Asignada (MW)"] = df.apply(calcular_asignacion, axis=1)
                ofertas_aceptadas = df[df["Potencia Asignada (MW)"] > 0]
                precio_marginal = (
                    df.iloc[0]["Precio (€/MWh)"] if ofertas_aceptadas.empty
                    else ofertas_aceptadas.iloc[-1]["Precio (€/MWh)"]
                )

                df["Ingresos (€)"]  = df["Potencia Asignada (MW)"] * precio_marginal
                df["Costes Op (€)"] = df["Potencia Asignada (MW)"] * df["Coste Op (€/MWh)"]

                if sala["ronda_actual"] == 0:
                    df["Penalización Cambio (€)"]          = 0
                    df["Penalización Parada/Arranque (€)"] = 0
                else:
                    df["Cambio Carga (MW)"]       = abs(df["Potencia Asignada (MW)"] - df["Potencia Anterior (MW)"])
                    df["Penalización Cambio (€)"] = df["Cambio Carga (MW)"] * df["Coste Cambio (€/MW)"]

                    def calcular_pa(row):
                        if row["Potencia Anterior (MW)"] == 0 and row["Potencia Asignada (MW)"] > 0:
                            return row["Coste P/A Fijo (€)"]
                        elif row["Potencia Anterior (MW)"] > 0 and row["Potencia Asignada (MW)"] == 0:
                            return row["Coste P/A Fijo (€)"]
                        return 0

                    df["Penalización Parada/Arranque (€)"] = df.apply(calcular_pa, axis=1)

                df["Beneficio Neto (€)"] = (
                    df["Ingresos (€)"]
                    - df["Costes Op (€)"]
                    - df["Penalización Cambio (€)"]
                    - df["Penalización Parada/Arranque (€)"]
                )

                total_asignado = df["Potencia Asignada (MW)"].sum()
                if total_asignado < demanda_residual:
                    sala["hubo_apagon"] = True
                else:
                    sala["hubo_apagon"] = False
                    for _, row in df.iterrows():
                        eq   = row["Equipo"]
                        tech = row["Tecnología"]
                        clave = f"{eq}_{tech}"
                        sala["potencia_asignada_anterior"][clave] = row["Potencia Asignada (MW)"]
                        sala["dinero_acumulado"][eq]  += row["Beneficio Neto (€)"]
                        sala["energia_acumulada"][eq][tech] += row["Potencia Asignada (MW)"]

                    # Guardar en histórico para la gráfica final
                    sala["historico_resultados"].append({
                        "hora":             datos_hora["hora"],
                        "demanda_residual": demanda_residual,
                        "precio_marginal":  float(precio_marginal),
                        "df_records":       df.to_dict("records"),
                    })

                sala["resultados_df"]   = df.to_dict("records")
                sala["precio_marginal"] = float(precio_marginal)
                sala["fase"]            = "resultados"
                st.rerun()

        # ── FASE: RESULTADOS (HOST) ────────────────────────────────────────────
        elif sala["fase"] == "resultados":
            if sala["hubo_apagon"]:
                df_res    = pd.DataFrame(sala["resultados_df"])
                fig_merit = grafico_merit_order(df_res, demanda_residual, sala["precio_marginal"])

                st.markdown(
                    "<h1 style='text-align:center;color:#ff0000;font-size:4em;'>"
                    f"{t('blackout_alert')}</h1>",
                    unsafe_allow_html=True,
                )
                st.error(t("blackout_msg"))
                st.pyplot(fig_merit)
                plt.close(fig_merit)

                if st.button(t("redo_offers"), type="primary"):
                    sala["fase"]        = "ofertando"
                    sala["ofertas"]     = {}
                    sala["hubo_apagon"] = False
                    st.rerun()
            else:
                # Solo mostrar precio de cierre (sin gráfica ni tabla de beneficios)
                st.success(
                    f"### {t('market_price')} **{sala['precio_marginal']:,.2f} €/MWh**"
                )

                if st.button(t("next_hour"), type="primary", use_container_width=True):
                    sala["ronda_actual"] += 1
                    sala["fase"]         = "ofertando"
                    sala["ofertas"]      = {}
                    st.rerun()


# ==========================================
# 📱 VISTA DEL JUGADOR
# ==========================================
if st.session_state.rol == "jugador":
    sala_id = st.session_state.sala_activa

    if sala_id not in db["salas"]:
        st.error(t("room_not_found"))
        st.stop()

    sala        = db["salas"][sala_id]
    estado_sala = sala["estado"]

    if "idioma" in sala:
        st.session_state.idioma = sala["idioma"]

    # ── REGISTRO / RECONEXIÓN ─────────────────────────────────────────────────
    if estado_sala == "esperando":
        st.title(t("register_title"))

        if "mi_equipo" not in st.session_state:
            nombre_equipo = st.text_input(t("company_name"))
            if st.button(t("accept"), type="primary"):
                if nombre_equipo and nombre_equipo not in sala["equipos"]:
                    sala["equipos"].append(nombre_equipo)
                    st.session_state.mi_equipo = nombre_equipo
                    st.query_params["sala"]   = sala_id
                    st.query_params["equipo"] = nombre_equipo
                    st.rerun()
                else:
                    st.error(t("invalid_name"))
        else:
            st.success(t("registered_ok", nombre=st.session_state.mi_equipo))
            st_autorefresh(interval=2000, key="refresh_jugador_lobby")
        st.stop()

    elif estado_sala == "jugando" and "mi_equipo" not in st.session_state:
        # ── PANTALLA DE RECONEXIÓN ─────────────────────────────────────────────
        st.title(t("reconnect_title"))
        st.info(t("reconnect_info"))

        # Mostrar QR para facilitar el reingreso con el mismo enlace de sala
        URL_BASE       = "https://simuladormercado2-tf9xg2yjxcjjfs5dufe6jl.streamlit.app"
        url_sala       = f"{URL_BASE}/?sala={sala_id}"
        st.markdown("**Scan to return to this room:**")
        qr_reconex = qrcode.make(url_sala)
        st.image(qr_reconex.get_image(), width=180)

        nombre_reconex = st.text_input(t("company_name"), key="reconex_input")
        if st.button(t("reconnect_btn"), type="primary"):
            if nombre_reconex in sala["equipos"]:
                st.session_state.mi_equipo = nombre_reconex
                st.query_params["sala"]   = sala_id
                st.query_params["equipo"] = nombre_reconex
                st.rerun()
            else:
                st.error(t("reconnect_error"))
        st.stop()

    # ── JUEGO ACTIVO (JUGADOR) ────────────────────────────────────────────────
    mi_equipo = st.session_state.mi_equipo
    ronda     = sala["ronda_actual"]

    if ronda >= len(HORARIOS):
        st.success(t("market_closed"))
        st.info(t("check_screen"))
        st.stop()

    datos_hora       = HORARIOS[ronda]
    demanda_residual = datos_hora["demanda"] - datos_hora["renovables"]

    # FIX #2: Sin mensaje informativo MW/MWh — solo título y hora/demanda
    st.title(f"🏢 {mi_equipo}")

    col_hora, col_demanda = st.columns(2)
    with col_hora:
        st.markdown(
            f"<div style='background-color:#f0f9ff;padding:8px 14px;border-radius:8px;"
            f"border:1px solid #bae6fd;text-align:center;'>"
            f"<span style='color:#0369a1;font-size:0.85rem;font-weight:bold;'>🕒 {t('hour_label')}</span><br>"
            f"<span style='color:#0c4a6e;font-size:1.1rem;font-weight:800;'>{datos_hora['hora']}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col_demanda:
        st.markdown(
            f"<div style='background-color:#fef3c7;padding:8px 14px;border-radius:8px;"
            f"border:1px solid #fbbf24;text-align:center;'>"
            f"<span style='color:#92400e;font-size:0.85rem;font-weight:bold;'>🏭 {t('demand_to_cover')}</span><br>"
            f"<span style='color:#78350f;font-size:1.1rem;font-weight:800;'>{demanda_residual} MW</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    saldo_actual = sala["dinero_acumulado"].get(mi_equipo, 0)
    st.markdown(f"""
        <div style="background-color:#f8fafc;padding:8px 15px;border-radius:8px;
                    border:1px solid #cbd5e1;margin:10px 0;display:flex;
                    align-items:center;gap:10px;">
            <span style="font-size:1.2rem;">💰</span>
            <span style="color:#475569;font-size:0.9rem;font-weight:bold;">{t('current_balance')}</span>
            <span style="color:#1e293b;font-size:1.1rem;font-weight:800;margin-left:auto;">
                {saldo_actual:,.0f} €
            </span>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── FASE: ENVIAR OFERTAS ──────────────────────────────────────────────────
    if sala["fase"] == "ofertando":
        if mi_equipo in sala["ofertas"]:
            st.success(t("offer_sent"))
            st.info(t("waiting_others"))
            st_autorefresh(interval=2000, key="refresh_jugador_esperando")
        else:
            st.subheader(t("prepare_offer"))
            mis_ofertas = []

            with st.form(key=f"form_oferta_{ronda}"):
                for tech, info in sala["TECNOLOGIAS"].items():
                    clave_historial = f"{mi_equipo}_{tech}"
                    pot_anterior    = sala["potencia_asignada_anterior"].get(clave_historial, 0)

                    # Nombre de tecnología traducido en el formulario
                    st.markdown(f"**🔌 {tech_display(tech)}** ({t('previous_mw', mw=int(pot_anterior))})")
                    col1, col2 = st.columns(2)
                    with col1:
                        if ronda == 0:
                            min_sl, max_sl = 0, info["pot_max"]
                        else:
                            min_sl = int(max(0, pot_anterior - info["max_cambio"]))
                            max_sl = int(min(info["pot_max"], pot_anterior + info["max_cambio"]))

                        pot = st.slider(
                            f"MW – {tech_display(tech)}", min_sl, max_sl,
                            int(pot_anterior) if pot_anterior >= min_sl else min_sl,
                            step=10
                        )
                    with col2:
                        pre = st.number_input(
                            f"€/MWh – {tech_display(tech)}",
                            value=float(info["coste_op"]),
                            step=1.0
                        )

                    mis_ofertas.append({
                        "Equipo":                  mi_equipo,
                        "Tecnología":              tech,   # siempre interno para el motor
                        "Potencia Ofertada (MW)":  pot,
                        "Precio (€/MWh)":          pre,
                        "Coste Op (€/MWh)":        info["coste_op"],
                        "Coste Cambio (€/MW)":     info["coste_cambio"],
                        "Coste P/A Fijo (€)":      info["coste_pa"],
                        "Potencia Anterior (MW)":  pot_anterior,
                    })
                    st.divider()

                enviado = st.form_submit_button(
                    t("send_offer"), type="primary", use_container_width=True
                )
                if enviado:
                    sala["ofertas"][mi_equipo] = mis_ofertas
                    st.rerun()

    # ── FASE: RESULTADOS (JUGADOR) ────────────────────────────────────────────
    elif sala["fase"] == "resultados":
        if sala["hubo_apagon"]:
            st.error(t("blackout_player"))
            st_autorefresh(interval=2000, key="refresh_jugador_apagon")
        else:
            st.success(t("market_cleared"))

            df_res     = pd.DataFrame(sala["resultados_df"])
            datos_mios = df_res[df_res["Equipo"] == mi_equipo]
            saldo_actual = sala["dinero_acumulado"][mi_equipo]

            tecnologias_orden = ["Nuclear", "Carbón", "Ciclo Combinado", "Gas"]

            data_dict = {
                "Concepto": [
                    t("offer_power_mw"),
                    t("offer_price"),
                    t("sold_power_mw"),
                    t("clearing_price_row"),
                    t("income"),
                    t("op_costs"),
                    t("penalties"),
                    t("net_profit"),
                ]
            }

            for tech in tecnologias_orden:
                tech_disp = tech_display(tech)
                row_data  = datos_mios[datos_mios["Tecnología"] == tech]
                if not row_data.empty:
                    r = row_data.iloc[0]
                    penalizaciones = (
                        r["Penalización Cambio (€)"] + r["Penalización Parada/Arranque (€)"]
                    )
                    data_dict[tech_disp] = [
                        f"{r['Potencia Ofertada (MW)']:,.0f} MW",
                        f"{r['Precio (€/MWh)']:,.2f} €/MWh",
                        f"{r['Potencia Asignada (MW)']:,.0f} MW",
                        f"{sala['precio_marginal']:,.2f} €/MWh" if r["Potencia Asignada (MW)"] > 0 else "—",
                        f"{r['Ingresos (€)']:,.0f} €",
                        f"{r['Costes Op (€)']:,.0f} €",
                        f"{penalizaciones:,.0f} €",
                        f"{r['Beneficio Neto (€)']:,.0f} €",
                    ]
                else:
                    data_dict[tech_disp] = ["0 MW", "— €/MWh", "0 MW", "—", "0 €", "0 €", "0 €", "0 €"]

            df_display = pd.DataFrame(data_dict)

            def aplicar_colores(row):
                concepto = row["Concepto"]
                if t("offer_power_mw") in concepto or t("offer_price") in concepto:
                    est = "background-color:#dbeafe;color:#1e3a8a;"
                elif t("sold_power_mw") in concepto or t("income") in concepto:
                    est = "background-color:#dcfce7;color:#166534;"
                elif t("op_costs") in concepto or t("penalties") in concepto:
                    est = "background-color:#fee2e2;color:#991b1b;"
                elif t("net_profit") in concepto:
                    est = "background-color:#16a34a;color:white;font-weight:bold;"
                else:
                    est = ""
                estilos    = [est] * len(row)
                estilos[0] = (
                    (est + "font-weight:bold;border-right:2px solid gray;")
                    if est else "font-weight:bold;border-right:2px solid gray;"
                )
                return estilos

            styled_df = df_display.style.hide(axis="index").apply(aplicar_colores, axis=1)
            st.table(styled_df)

            st.markdown(
                f"<h3 style='text-align:right;color:#1e3a8a;'>"
                f"{t('total_balance')} {saldo_actual:,.0f} €</h3>",
                unsafe_allow_html=True,
            )
            st.info(t("waiting_host"))
            st_autorefresh(interval=2000, key="refresh_jugador_resultados")
