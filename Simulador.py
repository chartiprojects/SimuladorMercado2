import streamlit as st
import pandas as pd
import qrcode
import random
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import matplotlib.ticker as ticker
import time

# streamlit run SimuladorEquipos.py

st.set_page_config(page_title="Electricity Market Simulator", layout="wide")

# ==========================================
# 🌐 SISTEMA DE TRADUCCIONES
# ==========================================
LANG_OPTIONS = {"🇬🇧 English": "en", "🇪🇸 Español": "es", "🇫🇷 Français": "fr", "🇩🇪 Deutsch": "de"}

TRADUCCIONES = {
    "es": {
        "page_title": "Simulador Mercado Eléctrico",
        "language_screen_title": "⚡ Electricity Market Simulator",
        "language_screen_subtitle": "Choose the game language / Elige el idioma / Choisissez la langue",
        "welcome_title": "⚡ ¡Bienvenido! ⚡ Eres el operador del mercado eléctrico",
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
        "concept_label": "",
        "final_merit_title": "📊 Curva Merit Order - Histórico",
        "final_hour": "Hora",
        # ── Temporizador ──
        "timer_setup": "⏱️ Duración de la fase de ofertas (minutos)",
        "timer_help": "Los jugadores verán la cuenta atrás. Al llegar a 0 el mercado NO se cierra solo: lo cierras tú.",
        "time_left": "⏳ TIEMPO RESTANTE",
        "time_up": "⏰ ¡TIEMPO AGOTADO!",
        "time_up_host": "⏰ El tiempo ha terminado. Cierra el mercado cuando lo veas oportuno.",
        "force_close": "🔒 Cerrar mercado ahora (forzar casación)",
        "force_close_help": "Casa el mercado aunque falten empresas por ofertar. Las que no hayan enviado oferta se contarán como 0 MW.",
        "force_close_warning": "⚠️ Se ha forzado el cierre. Empresas sin oferta (contadas como 0 MW): {equipos}",
        # ── Blackout sin info de precios ──
        "blackout_coverage": "COBERTURA DE LA DEMANDA",
        "blackout_missing": "FALTA POR CUBRIR",
        "blackout_offered": "Ofertado por el conjunto de empresas",
        # ── Apagar instalación ──
        "shutdown_label": "⛔ Apagar esta central (0 MW)",
        "shutdown_active": "⛔ Central APAGADA — ofertará 0 MW",
        "shutdown_help": "Apagar tiene coste de parada, pero te permite bajar a 0 MW saltándote el límite de rampa.",
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
        "welcome_title": "⚡ Welcome! ⚡ You are the electricity market operator",
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
        "concept_label": "",
        "final_merit_title": "📊 Merit Order Curve - History",
        "final_hour": "Hour",
        # ── Timer ──
        "timer_setup": "⏱️ Bidding phase duration (minutes)",
        "timer_help": "Players will see the countdown. When it reaches 0 the market does NOT close by itself: you close it.",
        "time_left": "⏳ TIME REMAINING",
        "time_up": "⏰ TIME IS UP!",
        "time_up_host": "⏰ Time is up. Close the market whenever you see fit.",
        "force_close": "🔒 Close market now (force clearing)",
        "force_close_help": "Clears the market even if some companies haven't submitted. Missing offers count as 0 MW.",
        "force_close_warning": "⚠️ Closing was forced. Companies without offers (counted as 0 MW): {equipos}",
        # ── Blackout without price info ──
        "blackout_coverage": "DEMAND COVERAGE",
        "blackout_missing": "STILL UNCOVERED",
        "blackout_offered": "Offered by all companies combined",
        # ── Shutdown ──
        "shutdown_label": "⛔ Shut down this plant (0 MW)",
        "shutdown_active": "⛔ Plant SHUT DOWN — will offer 0 MW",
        "shutdown_help": "Shutting down has a stop cost, but lets you go to 0 MW bypassing the ramp limit.",
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
        "welcome_title": "⚡ Bienvenue ! ⚡ Vous êtes l'opérateur du marché de l'électricité",
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
        "concept_label": "",
        "final_merit_title": "📊 Courbe Merit Order - Historique",
        "final_hour": "Heure",
        # ── Minuteur ──
        "timer_setup": "⏱️ Durée de la phase d'offres (minutes)",
        "timer_help": "Les joueurs verront le compte à rebours. À 0, le marché ne se ferme PAS tout seul : c'est vous qui le fermez.",
        "time_left": "⏳ TEMPS RESTANT",
        "time_up": "⏰ TEMPS ÉCOULÉ !",
        "time_up_host": "⏰ Le temps est écoulé. Fermez le marché quand vous le jugez opportun.",
        "force_close": "🔒 Fermer le marché maintenant (forcer)",
        "force_close_help": "Équilibre le marché même si des entreprises n'ont pas soumis. Les offres manquantes comptent comme 0 MW.",
        "force_close_warning": "⚠️ Fermeture forcée. Entreprises sans offre (comptées 0 MW) : {equipos}",
        # ── Coupure sans info de prix ──
        "blackout_coverage": "COUVERTURE DE LA DEMANDE",
        "blackout_missing": "RESTE À COUVRIR",
        "blackout_offered": "Offert par l'ensemble des entreprises",
        # ── Arrêt ──
        "shutdown_label": "⛔ Arrêter cette centrale (0 MW)",
        "shutdown_active": "⛔ Centrale ARRÊTÉE — offrira 0 MW",
        "shutdown_help": "L'arrêt a un coût, mais permet de descendre à 0 MW en contournant la limite de modulation.",
        # Noms des technologies
        "tech_Nuclear":         "Nucléaire ⚛️",
        "tech_Coal":            "Charbon ⚫",
        "tech_CombinedCycle":   "Cycle Combiné ☁️",
        "tech_Gas":             "Gaz ♨️",
    },
    "de": {
        "page_title": "Strommarkt-Simulator",
        "language_screen_title": "⚡ Electricity Market Simulator",
        "language_screen_subtitle": "Choose the game language / Elige el idioma / Choisissez la langue",
        "welcome_title": "⚡ Willkommen! ⚡ Sie sind der Betreiber des Strommarktes",
        "choose_language": "🌐 Spielsprache wählen:",
        "generate_room": "👥 Raum erstellen",
        "waiting_room": "⚡ Warteraum",
        "scan_to_join": "### 📲 Scannen zum Mitmachen!",
        "registered_companies": "Registrierte Unternehmen:",
        "waiting_connections": "Warte auf Verbindungen...",
        "start_game": "🚀 Spiel starten",
        "need_2_players": "Es werden mindestens 2 Unternehmen benötigt!",
        "operator_name": "ÜNB",
        "ree_control": "⚡ ÜNB - Zentrale Steuerung",
        "demand": "🏭 NACHFRAGE",
        "renewables": "🌱 ERNEUERN.",
        "to_cover": "⚡ ZU DECKEN",
        "plant_params": "**📋 Kraftwerksparameter**",
        "max_power": "Maximale Leistung (MW)",
        "op_cost": "Betriebskosten (€/MWh)",
        "ramp_cost": "Rampenkosten (€/MW)",
        "startup_cost": "An-/Abfahrkosten (€)",
        "companies_submitted": "Unternehmen, die Angebote eingereicht haben:",
        "clear_market": "⚖️ Markt räumen",
        "all_offers_required": "⏳ Warte auf alle Angebote… ({received} von {total})",
        "nobody_offered": "Noch niemand hat ein Angebot eingereicht.",
        "blackout_alert": "🚨 BLACKOUT-ALARM! 🚨",
        "blackout_msg": "Das Stromsystem steht kurz vor dem Zusammenbruch. Der Markt wurde annulliert.",
        "redo_offers": "🔄 Neueinreichung erzwingen",
        "market_price": "💰 Endgültiger Marktpreis:",
        "next_hour": "⏭️ Zur nächsten Stunde",
        "final_results": "🎉 Die Handelssitzung ist beendet! Hier sind die Endergebnisse.",
        "final_ranking": "🏆 ENDRANGLISTE 🏆",
        "medals": ["🥇 1. PLATZ", "🥈 2. PLATZ", "🥉 3. PLATZ", "🏅 4. PLATZ", "🏅 5. PLATZ"],
        "register_title": "🏢 Unternehmensregistrierung",
        "company_name": "Name Ihres Unternehmens:",
        "accept": "Akzeptieren",
        "invalid_name": "Ungültiger Name oder bereits vergeben.",
        "registered_ok": "✅ Ihr Unternehmen **{nombre}** wurde registriert! Das Spiel beginnt bald…",
        "late_arrival": "Sie sind zu spät, das Spiel hat bereits begonnen.",
        "market_closed": "🎉 Der Markt hat für heute geschlossen!",
        "check_screen": "Schauen Sie auf den Bildschirm des Lehrers für die Endrangliste.",
        "hour_label": "STUNDE",
        "demand_to_cover": "ZU DECKENDE NACHFRAGE (MW)",
        "current_balance": "AKTUELLER KONTOSTAND:",
        "prepare_offer": "📝 Angebot vorbereiten",
        "previous_mw": "Vorherige: {mw} MW",
        "offer_sent": "📤 Angebot an ÜNB übermittelt.",
        "waiting_others": "Warten auf andere Unternehmen und den ÜNB zum Marktabschluss…",
        "send_offer": "⚖️ Angebot einreichen",
        "blackout_player": "🚨 BLACKOUT! Nachfrage nicht gedeckt. Bitte Angebot erneut einreichen.",
        "market_cleared": "✅ Markt geräumt. Hier sind Ihre Ergebnisse:",
        "offer_power_mw": "Angebot - Leistung (MW)",
        "offer_price": "Angebot - Preis (€/MWh)",
        "sold_power_mw": "Zugeteilt - Leistung (MW)",
        "clearing_price_row": "Abrechnungspreis (€/MWh)",
        "income": "Einnahmen (€)",
        "op_costs": "Betriebskosten (€)",
        "penalties": "Strafen (€)",
        "net_profit": "Nettogewinn (€)",
        "total_balance": "💵 GESAMTKONTOSTAND:",
        "waiting_host": "Warten auf den Marktbetreiber für die nächste Stunde…",
        "room_not_found": "❌ Dieser Raum existiert nicht oder das Spiel ist beendet.",
        "reconnect_title": "🔄 Erneut verbinden",
        "reconnect_info": "Ihre Sitzung wurde beendet. Geben Sie Ihren Unternehmensnamen ein:",
        "reconnect_btn": "Erneut verbinden",
        "reconnect_error": "Kein Unternehmen mit diesem Namen in diesem Raum gefunden.",
        "merit_order_title": "Angebotskurve (Merit Order)",
        "merit_order_x": "% Nachfrage gedeckt",
        "merit_order_y": "Preis (€/MWh)",
        "table_company": "Unternehmen",
        "table_net_profit": "Nettogewinn (€)",
        "param_label": "Parameter",
        "concept_label": "",
        "final_merit_title": "📊 Merit-Order-Kurve - Verlauf",
        "final_hour": "Stunde",
        # ── Timer ──
        "timer_setup": "⏱️ Dauer der Angebotsphase (Minuten)",
        "timer_help": "Die Spieler sehen den Countdown. Bei 0 schließt der Markt NICHT automatisch: Sie schließen ihn.",
        "time_left": "⏳ VERBLEIBENDE ZEIT",
        "time_up": "⏰ ZEIT ABGELAUFEN!",
        "time_up_host": "⏰ Die Zeit ist abgelaufen. Schließen Sie den Markt, wann immer Sie möchten.",
        "force_close": "🔒 Markt jetzt schließen (erzwingen)",
        "force_close_help": "Räumt den Markt, auch wenn Angebote fehlen. Fehlende Angebote zählen als 0 MW.",
        "force_close_warning": "⚠️ Schließung erzwungen. Unternehmen ohne Angebot (als 0 MW gezählt): {equipos}",
        # ── Blackout ohne Preisinfo ──
        "blackout_coverage": "NACHFRAGEDECKUNG",
        "blackout_missing": "NOCH UNGEDECKT",
        "blackout_offered": "Von allen Unternehmen zusammen angeboten",
        # ── Abschalten ──
        "shutdown_label": "⛔ Dieses Kraftwerk abschalten (0 MW)",
        "shutdown_active": "⛔ Kraftwerk ABGESCHALTET — bietet 0 MW",
        "shutdown_help": "Abschalten kostet, erlaubt aber 0 MW unter Umgehung der Rampengrenze.",
        # Technologienamen
        "tech_Nuclear":         "Kernkraft ⚛️",
        "tech_Coal":            "Kohle ⚫",
        "tech_CombinedCycle":   "GuD-Kraftwerk ☁️",
        "tech_Gas":             "Gas ♨️",
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
    "de": {
        "Nuclear":         "☢️ Kernkraft",
        "Carbón":          "🪨 Kohle",
        "Ciclo Combinado": "💨 GuD-Kraftwerk",
        "Gas":             "🔥 Gas",
    },
}

def tech_display(tech_internal):
    lang = st.session_state.get("idioma", "en")
    return TECH_DISPLAY.get(lang, TECH_DISPLAY["en"]).get(tech_internal, tech_internal)
# ==========================================
# 📊 GRÁFICO BLACKOUT
# ==========================================
def grafico_blackout(df_resultado, demanda_residual):
    """Indicador visual de apagón: SÓLO el % de demanda cubierta.

    Sin precios, sin ejes y sin texto accesorio. Durante el apagón los
    jugadores rehacen sus ofertas, así que cualquier dato de precios de los
    rivales sería información indebida.
    """
    from matplotlib.patches import FancyBboxPatch

    total_ofertado = float(df_resultado["Potencia Ofertada (MW)"].sum())
    pct_cubierto   = (total_ofertado / demanda_residual) * 100 if demanda_residual else 0
    pct_cubierto   = max(0.0, pct_cubierto)
    pct_dibujado   = min(pct_cubierto, 100.0)

    # Color según lo lejos que se esté de cubrir la demanda
    if pct_cubierto >= 95:
        color_fill = "#f59e0b"
    elif pct_cubierto >= 60:
        color_fill = "#f97316"
    else:
        color_fill = "#dc2626"

    fig, ax = plt.subplots(figsize=(11, 2.4))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Sistema de coordenadas pensado para que las esquinas salgan redondas
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 13)
    ax.axis("off")

    Y0, ALTO, RAD = 1.2, 4.4, 2.2

    # Carril de fondo = 100 % de la demanda
    ax.add_patch(FancyBboxPatch(
        (RAD, Y0 + RAD), 100 - 2 * RAD, ALTO - 2 * RAD,
        boxstyle=f"round,pad={RAD}",
        facecolor="#f1f5f9", edgecolor="none", zorder=2,
    ))

    # Relleno = lo que el mercado ha conseguido ofertar
    if pct_dibujado > 0:
        ancho = max(pct_dibujado, 2 * RAD + 0.1)
        ax.add_patch(FancyBboxPatch(
            (RAD, Y0 + RAD), ancho - 2 * RAD, ALTO - 2 * RAD,
            boxstyle=f"round,pad={RAD}",
            facecolor=color_fill, edgecolor="none", zorder=3,
        ))

    # El gran número: único texto del gráfico
    ax.text(0, 7.2, f"{pct_cubierto:.1f}%",
            fontsize=42, fontweight="900", color=color_fill,
            ha="left", va="bottom", zorder=4)

    plt.tight_layout()
    return fig


# ==========================================
# 📊 GRÁFICO MERIT ORDER
# ==========================================
def grafico_merit_order(df_resultado, demanda_residual, precio_marginal):
    lang = st.session_state.get("idioma", "en")

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
        "de": {
            "Nuclear":         "Kernkraft ⚛️",
            "Carbón":          "Kohle ⚫",
            "Ciclo Combinado": "GuD-Kraftwerk ☁",
            "Gas":             "Gas ♨",
        },
    }
    DICT_TECH_LEGEND = TECH_LEGEND.get(lang, TECH_LEGEND["en"])

    COLORES_TECH = {
        "Nuclear ⚛️":       "#62ff3b",
        "Coal ⚫":           "#4e4859",
        "Carbón ⚫":         "#4e4859",
        "Charbon ⚫":        "#4e4859",
        "Kohle ⚫":          "#4e4859",
        "Comb. Cycle ☁":    "#322fc4",
        "Ciclo ☁":          "#322fc4",
        "Cycle Combiné ☁":  "#322fc4",
        "GuD-Kraftwerk ☁":  "#322fc4",
        "Nucléaire ⚛️":     "#62ff3b",
        "Kernkraft ⚛️":     "#62ff3b",
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

    # Opacidad de las ofertas NO casadas: mismo color de tecnología pero apagado,
    # para que se siga distinguiendo qué tecnología y qué empresa es cada bloque.
    ALPHA_CASADO    = 1.0
    ALPHA_NO_CASADO = 0.30

    for _, row in df_sorted.iterrows():
        tech_leg = row["_tech_legend"]
        mw       = row["Potencia Ofertada (MW)"]
        price    = row["Precio (€/MWh)"]
        equipo   = row["Equipo"]

        x_start = (cumulative / demanda_residual) * 100
        x_width = (mw / demanda_residual) * 100
        x_end   = x_start + x_width

        color = COLORES_TECH.get(tech_leg, "#F5B731")

        rect_bottom = min(0, price)
        rect_height = abs(price) if price != 0 else 0.5

        # Una misma oferta puede quedar parcialmente casada (prorrateo o corte
        # justo en el margen): se parte en dos tramos, uno vivo y otro apagado.
        tramos = []
        if x_end <= 100:
            tramos.append((x_start, x_width, ALPHA_CASADO))
        elif x_start >= 100:
            tramos.append((x_start, x_width, ALPHA_NO_CASADO))
        else:
            tramos.append((x_start, 100 - x_start, ALPHA_CASADO))
            tramos.append((100, x_end - 100, ALPHA_NO_CASADO))

        label_leyenda = tech_leg if tech_leg not in labels_agregadas else None
        labels_agregadas.add(tech_leg)

        for i, (tx, tw, talpha) in enumerate(tramos):
            if tw <= 0:
                continue
            rect = plt.Rectangle(
                (tx, rect_bottom), tw, rect_height,
                facecolor=color, edgecolor="white", linewidth=1,
                alpha=talpha, zorder=2,
                label=label_leyenda if i == 0 else None,
            )
            ax.add_patch(rect)

        # Etiqueta con el nombre de la empresa, también en las ofertas no casadas
        if x_width > 1.5:
            casado_mayoritario = (x_start + x_width / 2) < 100
            cx     = x_start + x_width / 2
            bar_h  = abs(price)

            if bar_h > y_range * 0.10:
                cy = rect_bottom + bar_h / 2
                ax.text(
                    cx, cy, equipo,
                    ha='center', va='center',
                    fontsize=6.5, fontweight='bold',
                    color='white' if casado_mayoritario else '#374151',
                    alpha=1.0 if casado_mayoritario else 0.75,
                    rotation=90, zorder=7, clip_on=True,
                )
            else:
                cy = max(price, 0) + y_range * 0.025
                ax.text(
                    cx, cy, equipo,
                    ha='center', va='bottom',
                    fontsize=6, fontweight='bold',
                    color='#1e3a8a' if casado_mayoritario else '#9ca3af',
                    rotation=90, zorder=7, clip_on=True,
                )

        cumulative += mw

    ax.fill_between([0, 100], y_min, precio_marginal, color="#FEFCE8", alpha=0.6, zorder=0)
    ax.hlines(precio_marginal, 0, 100, colors="#1E3A8A", linestyles="--", linewidth=1.5, zorder=4)
    ax.vlines(100, y_min, precio_marginal, colors="#1E3A8A", linestyles="--", linewidth=1.5, zorder=4)
    ax.plot(100, precio_marginal, "o", color="#fc0303", markersize=8, zorder=5)

    if y_min < 0:
        ax.hlines(0, 0, (total_ofertado / demanda_residual) * 100,
                  colors="#888888", linestyles="-", linewidth=0.8, zorder=3)

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
# ⏱️ TEMPORIZADOR DE LA FASE DE OFERTAS
# ==========================================
def iniciar_temporizador(sala):
    """Marca el instante en el que arranca una nueva fase de ofertas."""
    if sala.get("duracion_oferta_seg"):
        sala["inicio_oferta_ts"] = time.time()
    else:
        sala["inicio_oferta_ts"] = None


def segundos_restantes(sala):
    """Segundos que quedan de la fase de ofertas.

    Devuelve None si el host no configuró temporizador, y 0 si ya se agotó.
    El mercado NUNCA se cierra solo al llegar a 0: sólo lo cierra el host.
    """
    duracion = sala.get("duracion_oferta_seg")
    inicio   = sala.get("inicio_oferta_ts")
    if not duracion or not inicio:
        return None
    return max(0.0, duracion - (time.time() - inicio))


def rellenar_ofertas_faltantes(sala):
    """Al forzar el cierre, las empresas que no han ofertado entran con 0 MW.

    Devuelve la lista de nombres de esas empresas para poder avisar al host.
    """
    faltantes = []
    for eq in sala["equipos"]:
        if eq in sala["ofertas"]:
            continue
        faltantes.append(eq)
        ofertas_cero = []
        for tech, info in sala["TECNOLOGIAS"].items():
            pot_anterior = sala["potencia_asignada_anterior"].get(f"{eq}_{tech}", 0)
            ofertas_cero.append({
                "Equipo":                 eq,
                "Tecnología":             tech,
                "Potencia Ofertada (MW)": 0,
                "Precio (€/MWh)":         float(info["coste_op"]),
                "Coste Op (€/MWh)":       info["coste_op"],
                "Coste Cambio (€/MW)":    info["coste_cambio"],
                "Coste P/A Fijo (€)":     info["coste_pa"],
                "Potencia Anterior (MW)": pot_anterior,
            })
        sala["ofertas"][eq] = ofertas_cero
    return faltantes


# ==========================================
# ⚖️ CASACIÓN DEL MERCADO
# ==========================================
def casar_mercado(sala, demanda_residual, datos_hora):
    """Casa el mercado con precio marginal y PRORRATEO en el margen."""
    todas_las_ofertas = []
    for lista_equipo in sala["ofertas"].values():
        todas_las_ofertas.extend(lista_equipo)

    df = pd.DataFrame(todas_las_ofertas)
    df = df.sort_values(by="Precio (€/MWh)").reset_index(drop=True)
    df["Potencia Acumulada (MW)"] = df["Potencia Ofertada (MW)"].cumsum()

    total_ofertado = df["Potencia Ofertada (MW)"].sum()

    if total_ofertado <= 0:
        # Nadie oferta potencia > 0: no hay precio marginal definido.
        df["Potencia Asignada (MW)"] = 0.0
        precio_marginal = float(df["Precio (€/MWh)"].min()) if not df.empty else 0.0
    else:
        # Precio marginal: precio de la oferta en la que la potencia acumulada
        # alcanza (o supera) la demanda residual. Si no se llega a cubrir toda
        # la demanda, el precio marginal es el de la oferta más cara (habrá apagón).
        idx_marginales = df.index[df["Potencia Acumulada (MW)"] >= demanda_residual]
        if len(idx_marginales) > 0:
            precio_marginal = df.loc[idx_marginales[0], "Precio (€/MWh)"]
        else:
            precio_marginal = df["Precio (€/MWh)"].max()

        # Todo lo estrictamente más barato que el precio marginal entra al 100%.
        energia_mas_barata = df.loc[
            df["Precio (€/MWh)"] < precio_marginal, "Potencia Ofertada (MW)"
        ].sum()

        # Las ofertas empatadas EXACTAMENTE al precio marginal se reparten
        # por PRORRATEO proporcional a la cantidad ofertada por cada una
        # (igual que hace OMIE/EUPHEMIA con las ofertas casadas en el margen).
        mask_marginal      = df["Precio (€/MWh)"] == precio_marginal
        qty_marginal_total = df.loc[mask_marginal, "Potencia Ofertada (MW)"].sum()
        necesario_marginal = max(0.0, demanda_residual - energia_mas_barata)
        necesario_marginal = min(necesario_marginal, qty_marginal_total)

        factor_prorrateo = (
            necesario_marginal / qty_marginal_total
            if qty_marginal_total > 0 else 0.0
        )

        def calcular_asignacion(row):
            if row["Precio (€/MWh)"] < precio_marginal:
                return row["Potencia Ofertada (MW)"]
            elif row["Precio (€/MWh)"] == precio_marginal:
                return row["Potencia Ofertada (MW)"] * factor_prorrateo
            else:
                return 0.0

        df["Potencia Asignada (MW)"] = df.apply(calcular_asignacion, axis=1)

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
            eq    = row["Equipo"]
            tech  = row["Tecnología"]
            clave = f"{eq}_{tech}"
            sala["potencia_asignada_anterior"][clave] = row["Potencia Asignada (MW)"]
            sala["dinero_acumulado"][eq]  += row["Beneficio Neto (€)"]
            sala["energia_acumulada"][eq][tech] += row["Potencia Asignada (MW)"]

        sala["historico_resultados"].append({
            "hora":             datos_hora["hora"],
            "demanda_residual": demanda_residual,
            "precio_marginal":  float(precio_marginal),
            "df_records":       df.to_dict("records"),
        })

    sala["resultados_df"]   = df.to_dict("records")
    sala["precio_marginal"] = float(precio_marginal)
    sala["fase"]            = "resultados"
    sala["inicio_oferta_ts"] = None
    return df


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

    # ── PASO 0: ELEGIR IDIOMA ─────────────────────────────────────────────────
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

        col_en, col_es, col_fr, col_de = st.columns(4)
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
        with col_de:
            st.markdown(
                "<div style='text-align:center;font-size:4rem;line-height:1;'>🇩🇪</div>",
                unsafe_allow_html=True,
            )
            if st.button("Deutsch", use_container_width=True, type="primary"):
                st.session_state.idioma = "de"
                st.rerun()
        st.stop()

    # ── PASO 1: CREAR SALA ────────────────────────────────────────────────────
    # ── PASO 1: CREAR SALA ────────────────────────────────────────────────────
    if "sala_activa" not in st.session_state:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            _partes = t("welcome_title").split("⚡")
            _titulo = f"⚡{_partes[1]}⚡<br>{_partes[2].strip()}" if len(_partes) > 2 else t("welcome_title")
            st.markdown(
                f"<h1 style='text-align:center;font-size:2.3rem;line-height:1.35;"
                f"margin-top:40px;margin-bottom:40px;'>{_titulo}</h1>",
                unsafe_allow_html=True,
            )
            st.markdown("""
                <style>
                div[data-testid="stButton"] > button {
                    height: 70px;
                    border-radius: 14px;
                }
                div[data-testid="stButton"] > button p {
                    font-size: 1.6rem !important;
                    font-weight: 800;
                }
                </style>
            """, unsafe_allow_html=True)

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

        # CSS de esta pantalla: botón grande y textos más legibles
        st.markdown("""
            <style>
            div[data-testid="stButton"] > button {
                height: 80px;
                border-radius: 14px;
            }
            div[data-testid="stButton"] > button p {
                font-size: 1.5rem !important;
                font-weight: 800;
            }
            div[data-testid="stNumberInput"] label p {
                font-size: 1.15rem !important;
                font-weight: 700;
            }
            div[data-testid="stNumberInput"] input {
                font-size: 1.4rem !important;
                font-weight: 700;
                text-align: center;
            }
            </style>
        """, unsafe_allow_html=True)

        col_izq, col_der = st.columns([1, 1])
        with col_izq:
            st.markdown(t("scan_to_join"))
            st.code(url_invitacion)
            equipos_unidos = sala["equipos"]
            st.markdown(
                f"<p style='font-size:1.4rem;font-weight:800;margin:15px 0 10px 0;'>"
                f"{t('registered_companies')} {len(equipos_unidos)}</p>",
                unsafe_allow_html=True,
            )

            if len(equipos_unidos) > 0:
                nombres_html = " ".join([
                    f"<span style='background-color:#1e3a8a;color:white;padding:10px 18px;"
                    f"border-radius:10px;margin:5px;display:inline-block;font-size:1.3rem;"
                    f"font-weight:700;'>{eq}</span>"
                    for eq in equipos_unidos
                ])
                st.markdown(nombres_html, unsafe_allow_html=True)
            else:
                st.info(t("waiting_connections"))

            st_autorefresh(interval=2000, key="refresh_host_lobby")

        with col_der:
            qr = qrcode.make(url_invitacion)
            st.image(qr.get_image(), width=420)

        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

        # ── CONFIGURACIÓN DEL TEMPORIZADOR ────────────────────────────────────
        col_t1, col_t2 = st.columns([1, 2])
        with col_t1:
            minutos_oferta = st.number_input(
                t("timer_setup"),
                min_value=0.0, max_value=30.0, value=3.0, step=0.5,
                help=t("timer_help"),
            )

        st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)

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
                sala["duracion_oferta_seg"]        = int(minutos_oferta * 60)
                sala["aviso_forzado"]              = None
                iniciar_temporizador(sala)
                st.rerun()
            else:
                st.error(t("need_2_players"))

    # ── JUEGO ACTIVO (HOST) ───────────────────────────────────────────────────
    elif estado_sala == "jugando":

        with st.sidebar:
            st.markdown("### 🔌 Reconnection QRs")
            st.caption("Show this to a player who disconnected.")
            for eq in sala["equipos"]:
                url_eq = f"https://simuladormercado2-tf9xg2yjxcjjfs5dufe6jl.streamlit.app/?sala={sala_id}&equipo={eq}"
                with st.expander(f"📱 {eq}"):
                    qr_eq = qrcode.make(url_eq)
                    st.image(qr_eq.get_image(), width=180)
                    st.code(url_eq, language=None)

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

            # ── TEMPORIZADOR ──────────────────────────────────────────────────
            restante = segundos_restantes(sala)
            if restante is not None:
                if restante > 0:
                    mins, segs = divmod(int(restante), 60)
                    # Verde > 50 %, ámbar > 20 %, rojo por debajo
                    total_seg = max(1, sala.get("duracion_oferta_seg", 1))
                    frac      = restante / total_seg
                    if frac > 0.5:
                        col_bg, col_bd, col_tx = "#dcfce7", "#22c55e", "#166534"
                    elif frac > 0.2:
                        col_bg, col_bd, col_tx = "#fef3c7", "#f59e0b", "#b45309"
                    else:
                        col_bg, col_bd, col_tx = "#fee2e2", "#dc2626", "#991b1b"
                    st.markdown(
                        f"<div style='background-color:{col_bg};border:2px solid {col_bd};"
                        f"border-radius:10px;padding:10px;text-align:center;margin-bottom:10px;'>"
                        f"<span style='color:{col_tx};font-size:0.85rem;font-weight:bold;'>"
                        f"{t('time_left')}</span><br>"
                        f"<span style='color:{col_tx};font-size:2.6rem;font-weight:900;"
                        f"font-family:monospace;'>{mins:02d}:{segs:02d}</span></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<div style='background-color:#fee2e2;border:2px solid #dc2626;"
                        "border-radius:10px;padding:10px;text-align:center;margin-bottom:10px;'>"
                        f"<span style='color:#991b1b;font-size:2rem;font-weight:900;'>"
                        f"{t('time_up')}</span></div>",
                        unsafe_allow_html=True,
                    )
                    st.info(t("time_up_host"))

            st.metric(t("companies_submitted"), f"{ofertas_recibidas} de {total_equipos}")
            st.progress(ofertas_recibidas / total_equipos)

            # Refresco cada segundo mientras corre el reloj, cada 2 s si no hay reloj
            st_autorefresh(interval=1000 if restante is not None else 2000,
                           key="refresh_host_ofertando")

            if not todas_enviadas:
                st.warning(t("all_offers_required",
                             received=ofertas_recibidas, total=total_equipos))

            # Un único botón, SIEMPRE activo: el host decide cuándo cerrar.
            # Si falta alguna empresa por ofertar, entra con 0 MW.
            if st.button(
                t("clear_market"),
                type="primary",
                use_container_width=True,
                help=t("force_close_help"),
            ):
                faltantes = rellenar_ofertas_faltantes(sala)
                sala["aviso_forzado"] = (
                    t("force_close_warning", equipos=", ".join(faltantes))
                    if faltantes else None
                )
                casar_mercado(sala, demanda_residual, datos_hora)
                st.rerun()


        # ── FASE: RESULTADOS (HOST) ────────────────────────────────────────────
        elif sala["fase"] == "resultados":
            if sala.get("aviso_forzado"):
                st.warning(sala["aviso_forzado"])

            if sala["hubo_apagon"]:
                df_res    = pd.DataFrame(sala["resultados_df"])
                fig_merit = grafico_blackout(df_res, demanda_residual)

                st.markdown(
                    "<h1 style='text-align:center;color:#ff0000;font-size:4em;'>"
                    f"{t('blackout_alert')}</h1>",
                    unsafe_allow_html=True,
                )
                st.error(t("blackout_msg"))
                st.pyplot(fig_merit)
                plt.close(fig_merit)

                if st.button(t("redo_offers"), type="primary"):
                    sala["ofertas_apagon"] = sala.get("resultados_df", [])  # keep failed offers as seed
                    sala["fase"]        = "ofertando"
                    sala["ofertas"]     = {}
                    sala["hubo_apagon"] = False
                    iniciar_temporizador(sala)
                    st.rerun()
            else:
                st.success(
                    f"### {t('market_price')} **{sala['precio_marginal']:,.2f} €/MWh**"
                )

                if st.button(t("next_hour"), type="primary", use_container_width=True):
                    sala["ronda_actual"] += 1
                    sala["fase"]         = "ofertando"
                    sala["ofertas"]      = {}
                    sala["ofertas_apagon"] = {}
                    sala["aviso_forzado"]  = None
                    iniciar_temporizador(sala)
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
        st.title(t("reconnect_title"))
        st.info(t("reconnect_info"))

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

        # ── CUENTA ATRÁS (también visible en el móvil del jugador) ────────────
        restante_j = segundos_restantes(sala)
        if restante_j is not None:
            if restante_j > 0:
                mins_j, segs_j = divmod(int(restante_j), 60)
                total_seg_j = max(1, sala.get("duracion_oferta_seg", 1))
                frac_j = restante_j / total_seg_j
                if frac_j > 0.5:
                    bg_j, bd_j, tx_j = "#dcfce7", "#22c55e", "#166534"
                elif frac_j > 0.2:
                    bg_j, bd_j, tx_j = "#fef3c7", "#f59e0b", "#b45309"
                else:
                    bg_j, bd_j, tx_j = "#fee2e2", "#dc2626", "#991b1b"
                st.markdown(
                    f"<div style='background-color:{bg_j};border:2px solid {bd_j};"
                    f"border-radius:10px;padding:6px;text-align:center;margin-bottom:10px;'>"
                    f"<span style='color:{tx_j};font-size:0.75rem;font-weight:bold;'>"
                    f"{t('time_left')}</span><br>"
                    f"<span style='color:{tx_j};font-size:2rem;font-weight:900;"
                    f"font-family:monospace;'>{mins_j:02d}:{segs_j:02d}</span></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div style='background-color:#fee2e2;border:2px solid #dc2626;"
                    "border-radius:10px;padding:6px;text-align:center;margin-bottom:10px;'>"
                    f"<span style='color:#991b1b;font-size:1.5rem;font-weight:900;'>"
                    f"{t('time_up')}</span></div>",
                    unsafe_allow_html=True,
                )

        if mi_equipo in sala["ofertas"]:
            st.success(t("offer_sent"))
            st.info(t("waiting_others"))
            st_autorefresh(interval=2000, key="refresh_jugador_esperando")
        else:
            # Refresco del reloj mientras el jugador prepara su oferta.
            # Los widgets del formulario conservan su valor entre refrescos.
            if restante_j is not None and restante_j > 0:
                st_autorefresh(interval=1000, key="refresh_jugador_reloj")

            st.subheader(t("prepare_offer"))
            mis_ofertas = []

            # Build a lookup of the failed blackout offers for this player (if any)
            apagon_lookup = {}
            for row in sala.get("ofertas_apagon", []):
                if isinstance(row, dict) and row.get("Equipo") == mi_equipo:
                    apagon_lookup[row["Tecnología"]] = row

            with st.form(key=f"form_oferta_{ronda}"):
                for tech, info in sala["TECNOLOGIAS"].items():
                    clave_historial = f"{mi_equipo}_{tech}"
                    pot_anterior    = sala["potencia_asignada_anterior"].get(clave_historial, 0)

                    st.markdown(f"**🔌 {tech_display(tech)}** ({t('previous_mw', mw=int(pot_anterior))})")

                    # ── BOTÓN DE APAGADO ──────────────────────────────────────
                    # Permite bajar a 0 MW saltándose el límite de rampa
                    # (con su correspondiente coste de parada).
                    apagada = st.checkbox(
                        t("shutdown_label"),
                        key=f"apagar_{ronda}_{tech}",
                        help=t("shutdown_help"),
                    )
                    if apagada:
                        st.caption(t("shutdown_active"))

                    col1, col2 = st.columns(2)
                    with col1:
                        if ronda == 0:
                            min_sl, max_sl = 0, info["pot_max"]
                        else:
                            min_sl = int(max(0, pot_anterior - info["max_cambio"]))
                            max_sl = int(min(info["pot_max"], pot_anterior + info["max_cambio"]))

                        # Default: use the failed blackout offer if available, else pot_anterior
                        if tech in apagon_lookup:
                            pot_default = int(apagon_lookup[tech]["Potencia Ofertada (MW)"])
                            pot_default = max(min_sl, min(max_sl, pot_default))
                        else:
                            pot_default = int(pot_anterior) if pot_anterior >= min_sl else min_sl

                        pot = st.slider(
                            f"MW – {tech_display(tech)}", min_sl, max_sl,
                            pot_default,
                            step=1,
                            disabled=apagada,
                        )
                    with col2:
                        apagon_price = float(apagon_lookup[tech]["Precio (€/MWh)"]) if tech in apagon_lookup else float(info["coste_op"])
                        pre = st.number_input(
                            f"€/MWh – {tech_display(tech)}",
                            value=apagon_price,
                            step=1.0,
                            disabled=apagada,
                        )

                    # Si la central está apagada, la oferta es 0 MW pase lo que pase
                    pot_final = 0 if apagada else pot

                    mis_ofertas.append({
                        "Equipo":                  mi_equipo,
                        "Tecnología":              tech,
                        "Potencia Ofertada (MW)":  pot_final,
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

            # "concept_label" is an empty string → first column header will be blank
            data_dict = {
                t("concept_label"): [
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
                concepto = row[t("concept_label")]
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
