"""Source catalog for multilingual sensor entity + state translations.

Regenerate translation JSON via: python tools/build_entity_translations.py
"""

from __future__ import annotations

LANGS = ("en", "de", "fr", "it", "nl")

# name: {lang: label}  |  states: {portal_value: {lang: label}}
SENSORS: dict[str, dict] = {
    "integration_status": {
        "names": {
            "en": "Integration status",
            "de": "Integrationsstatus",
            "fr": "État de l'intégration",
            "it": "Stato integrazione",
            "nl": "Integratiestatus",
        },
        "states": {
            "starting": {
                "en": "Starting",
                "de": "Startet",
                "fr": "Démarrage",
                "it": "Avvio",
                "nl": "Opstarten",
            },
            "ok": {
                "en": "OK",
                "de": "OK",
                "fr": "OK",
                "it": "OK",
                "nl": "OK",
            },
            "waiting_for_portal_data": {
                "en": "Waiting for data",
                "de": "Warte auf Daten",
                "fr": "En attente de données",
                "it": "In attesa di dati",
                "nl": "Wachten op gegevens",
            },
            "empty_snapshots": {
                "en": "Empty snapshots only",
                "de": "Nur leere Schnappschüsse",
                "fr": "Instantanés vides uniquement",
                "it": "Solo snapshot vuoti",
                "nl": "Alleen lege momentopnames",
            },
            "delivery_not_ready": {
                "en": "Delivery not ready",
                "de": "Lieferung nicht bereit",
                "fr": "Livraison pas prête",
                "it": "Consegna non pronta",
                "nl": "Levering niet gereed",
            },
        },
    },
    "charge_state": {
        "names": {
            "en": "Charge state",
            "de": "Ladestatus",
            "fr": "État de charge",
            "it": "Stato di carica",
            "nl": "Laadstatus",
        },
        "states": {
            "CHARGE_STATE_READY_FOR_CHARGING": {
                "en": "Ready for charging",
                "de": "Ladebereit",
                "fr": "Prêt à charger",
                "it": "Pronto per la carica",
                "nl": "Klaar om te laden",
            },
            "CHARGE_STATE_NOT_READY_FOR_CHARGING": {
                "en": "Not ready",
                "de": "Nicht ladebereit",
                "fr": "Pas prêt",
                "it": "Non pronto",
                "nl": "Niet gereed",
            },
            "CHARGE_STATE_CHARGING_HV_BATTERY": {
                "en": "Charging HV battery",
                "de": "Lädt HV-Batterie",
                "fr": "Charge batterie HV",
                "it": "Carica batteria HV",
                "nl": "Laadt HV-accu",
            },
            "CHARGE_STATE_CONSERVATION_CHARGING": {
                "en": "Conservation charging",
                "de": "Erhaltungsladung",
                "fr": "Charge de conservation",
                "it": "Carica di conservazione",
                "nl": "Behoudlading",
            },
            "CHARGE_STATE_DISCHARGING": {
                "en": "Discharging",
                "de": "Entladen",
                "fr": "Décharge",
                "it": "Scarica",
                "nl": "Ontladen",
            },
            "CHARGE_STATE_CHARGING_ERROR": {
                "en": "Charging error",
                "de": "Ladefehler",
                "fr": "Erreur de charge",
                "it": "Errore di carica",
                "nl": "Laadfout",
            },
            "CHARGE_STATE_CHARGE_PURPOSE_REACHED_AND_CONSERVATION": {
                "en": "Target reached (conservation)",
                "de": "Ziel erreicht (Erhaltung)",
                "fr": "Objectif atteint (conservation)",
                "it": "Obiettivo raggiunto (conservazione)",
                "nl": "Doel bereikt (behoud)",
            },
            "CHARGE_STATE_CHARGE_PURPOSE_REACHED_AND_NOT_CONSERVATION_CHARGING": {
                "en": "Target reached",
                "de": "Ziel erreicht",
                "fr": "Objectif atteint",
                "it": "Obiettivo raggiunto",
                "nl": "Doel bereikt",
            },
        },
    },
    "charge_mode": {
        "names": {
            "en": "Charge mode",
            "de": "Lademodus",
            "fr": "Mode de charge",
            "it": "Modalità di carica",
            "nl": "Laadmodus",
        },
        "states": {
            "CHARGE_MODE_IMMEDIATELY_DEFAULT": {
                "en": "Immediate (default)",
                "de": "Sofort (Standard)",
                "fr": "Immédiat (défaut)",
                "it": "Immediata (predefinita)",
                "nl": "Direct (standaard)",
            },
            "CHARGE_MODE_IMMEDIATELY_PROFILE": {
                "en": "Immediate (profile)",
                "de": "Sofort (Profil)",
                "fr": "Immédiat (profil)",
                "it": "Immediata (profilo)",
                "nl": "Direct (profiel)",
            },
            "CHARGE_MODE_IMMEDIATELY_STOPPED": {
                "en": "Immediate stopped",
                "de": "Sofort gestoppt",
                "fr": "Immédiat arrêté",
                "it": "Immediata arrestata",
                "nl": "Direct gestopt",
            },
            "CHARGE_MODE_EXTENDED_PROFILE": {
                "en": "Extended (profile)",
                "de": "Verlängert (Profil)",
                "fr": "Prolongé (profil)",
                "it": "Estesa (profilo)",
                "nl": "Verlengd (profiel)",
            },
            "CHARGE_MODE_EXTENDED_STOPPED": {
                "en": "Extended stopped",
                "de": "Verlängert gestoppt",
                "fr": "Prolongé arrêté",
                "it": "Estesa arrestata",
                "nl": "Verlengd gestopt",
            },
            "CHARGE_MODE_INVALID": {
                "en": "Invalid",
                "de": "Ungültig",
                "fr": "Invalide",
                "it": "Non valido",
                "nl": "Ongeldig",
            },
        },
    },
    "charge_type": {
        "names": {
            "en": "Charge type",
            "de": "Ladeart",
            "fr": "Type de charge",
            "it": "Tipo di carica",
            "nl": "Laadtype",
        },
        "states": {
            "CHARGE_TYPE_AC": {
                "en": "AC",
                "de": "AC",
                "fr": "AC",
                "it": "AC",
                "nl": "AC",
            },
            "CHARGE_TYPE_DC": {
                "en": "DC",
                "de": "DC",
                "fr": "DC",
                "it": "DC",
                "nl": "DC",
            },
            "CHARGE_TYPE_OFF": {
                "en": "Off",
                "de": "Aus",
                "fr": "Arrêt",
                "it": "Spento",
                "nl": "Uit",
            },
        },
    },
    "charging_scenario": {
        "names": {
            "en": "Charging scenario",
            "de": "Ladeszenario",
            "fr": "Scénario de charge",
            "it": "Scenario di carica",
            "nl": "Laadscenario",
        },
        "states": {
            "CHARGING_SCENARIO_OFF": {
                "en": "Off",
                "de": "Aus",
                "fr": "Arrêt",
                "it": "Spento",
                "nl": "Uit",
            },
            "CHARGING_SCENARIO_IMMEDIATELY_CHARGING_ACTIVE": {
                "en": "Immediate charging",
                "de": "Sofortladen aktiv",
                "fr": "Charge immédiate active",
                "it": "Carica immediata attiva",
                "nl": "Direct laden actief",
            },
            "CHARGING_SCENARIO_IMMEDIATELY_CHARGING_FINISHED": {
                "en": "Immediate charging done",
                "de": "Sofortladen beendet",
                "fr": "Charge immédiate terminée",
                "it": "Carica immediata terminata",
                "nl": "Direct laden voltooid",
            },
            "CHARGING_SCENARIO_CHARGING_TO_DEPARTURE_TIME_ACTIVE": {
                "en": "Charging to departure",
                "de": "Laden bis Abfahrt",
                "fr": "Charge jusqu'au départ",
                "it": "Carica fino alla partenza",
                "nl": "Laden tot vertrek",
            },
            "CHARGING_SCENARIO_CHARGING_TO_DEPARTURE_TIME_FINISHED": {
                "en": "Departure charging done",
                "de": "Abfahrtsladen beendet",
                "fr": "Charge départ terminée",
                "it": "Carica partenza terminata",
                "nl": "Vertrekladen voltooid",
            },
            "CHARGING_SCENARIO_OPTIMISED_CHARGING_AC": {
                "en": "Optimised AC charging",
                "de": "Optimiertes AC-Laden",
                "fr": "Charge AC optimisée",
                "it": "Carica AC ottimizzata",
                "nl": "Geoptimaliseerd AC-laden",
            },
            "CHARGING_SCENARIO_OPTIMISED_CHARGING_FINISHED": {
                "en": "Optimised charging done",
                "de": "Optimiertes Laden beendet",
                "fr": "Charge optimisée terminée",
                "it": "Carica ottimizzata terminata",
                "nl": "Geoptimaliseerd laden voltooid",
            },
        },
    },
    "immediate_action_state": {
        "names": {
            "en": "Charging action state",
            "de": "Ladeaktionsstatus",
            "fr": "État action de charge",
            "it": "Stato azione di carica",
            "nl": "Laadactiestatus",
        },
        "states": {
            "IMMEDIATE_ACTION_STATE_INVALID": {
                "en": "Invalid",
                "de": "Ungültig",
                "fr": "Invalide",
                "it": "Non valido",
                "nl": "Ongeldig",
            },
            "IMMEDIATE_ACTION_STATE_IMMEDIATE_CHARGING": {
                "en": "Immediate charging",
                "de": "Sofortladen",
                "fr": "Charge immédiate",
                "it": "Carica immediata",
                "nl": "Direct laden",
            },
            "IMMEDIATE_ACTION_STATE_IMMEDIATE_ACTION_TIME": {
                "en": "Action: time",
                "de": "Aktion: Zeit",
                "fr": "Action : heure",
                "it": "Azione: orario",
                "nl": "Actie: tijd",
            },
            "IMMEDIATE_ACTION_STATE_IMMEDIATE_ACTION_STOPPED": {
                "en": "Action stopped",
                "de": "Aktion gestoppt",
                "fr": "Action arrêtée",
                "it": "Azione arrestata",
                "nl": "Actie gestopt",
            },
            "IMMEDIATE_ACTION_STATE_IMMEDIATE_ACTION_RANGE": {
                "en": "Action: range",
                "de": "Aktion: Reichweite",
                "fr": "Action : autonomie",
                "it": "Azione: autonomia",
                "nl": "Actie: bereik",
            },
            "IMMEDIATE_ACTION_STATE_IMMEDIATE_ACTION_SOC": {
                "en": "Action: SoC",
                "de": "Aktion: Ladestand",
                "fr": "Action : charge",
                "it": "Azione: carica",
                "nl": "Actie: laadstatus",
            },
            "IMMEDIATE_ACTION_STATE_CHARGE_MODE_SELECTION": {
                "en": "Mode selection",
                "de": "Moduswahl",
                "fr": "Sélection du mode",
                "it": "Selezione modalità",
                "nl": "Moduskeuze",
            },
        },
    },
    "charge_mode_selection": {
        "names": {
            "en": "Charge mode selection",
            "de": "Lademodus-Auswahl",
            "fr": "Sélection mode de charge",
            "it": "Selezione modalità carica",
            "nl": "Laadmodusselectie",
        },
        "states": {
            "CHARGE_MODE_SELECTION_INVALID": {
                "en": "Invalid",
                "de": "Ungültig",
                "fr": "Invalide",
                "it": "Non valido",
                "nl": "Ongeldig",
            },
            "CHARGE_MODE_SELECTION_IMMEDIATECHARGING": {
                "en": "Immediate charging",
                "de": "Sofortladen",
                "fr": "Charge immédiate",
                "it": "Carica immediata",
                "nl": "Direct laden",
            },
            "CHARGE_MODE_SELECTION_IMMEDIATE_DISCHARGING": {
                "en": "Immediate discharging",
                "de": "Sofort entladen",
                "fr": "Décharge immédiate",
                "it": "Scarica immediata",
                "nl": "Direct ontladen",
            },
            "CHARGE_MODE_SELECTION_TIMERCHARGING": {
                "en": "Timer charging",
                "de": "Timer-Laden",
                "fr": "Charge programmée",
                "it": "Carica a timer",
                "nl": "Timerladen",
            },
            "CHARGE_MODE_SELECTION_TIMER_CHARGING_CLIMATIZATION": {
                "en": "Timer + climate",
                "de": "Timer + Klima",
                "fr": "Minuteur + clim",
                "it": "Timer + clima",
                "nl": "Timer + klimaat",
            },
            "CHARGE_MODE_SELECTION_PREFERRED_CHARGING_TIMES": {
                "en": "Preferred times",
                "de": "Bevorzugte Zeiten",
                "fr": "Horaires préférés",
                "it": "Orari preferiti",
                "nl": "Voorkeurstijden",
            },
            "CHARGE_MODE_SELECTION_ONLY_OWN_CURRENT": {
                "en": "Own current only",
                "de": "Nur eigener Strom",
                "fr": "Courant propre uniquement",
                "it": "Solo corrente propria",
                "nl": "Alleen eigen stroom",
            },
            "CHARGE_MODE_SELECTION_HOME_STORAGE_CHARGING": {
                "en": "Home storage",
                "de": "Heimspeicher",
                "fr": "Stockage domestique",
                "it": "Accumulo domestico",
                "nl": "Thuisopslag",
            },
        },
    },
    "max_ac_charge_current": {
        "names": {
            "en": "Max AC charge current",
            "de": "Max. AC-Ladestrom",
            "fr": "Courant AC max",
            "it": "Corrente AC max",
            "nl": "Max. AC-laadstroom",
        },
        "states": {
            "MAX_CHARGE_CURRENT_INVALID": {
                "en": "Invalid",
                "de": "Ungültig",
                "fr": "Invalide",
                "it": "Non valido",
                "nl": "Ongeldig",
            },
            "MAX_CHARGE_CURRENT_MAXIMUM": {
                "en": "Maximum",
                "de": "Maximum",
                "fr": "Maximum",
                "it": "Massimo",
                "nl": "Maximum",
            },
            "MAX_CHARGE_CURRENT_REDUCED": {
                "en": "Reduced",
                "de": "Reduziert",
                "fr": "Réduit",
                "it": "Ridotto",
                "nl": "Verminderd",
            },
        },
    },
    "auto_unlock_ac": {
        "names": {
            "en": "Auto unlock AC",
            "de": "AC automatisch entriegeln",
            "fr": "Déverrouillage AC auto",
            "it": "Sblocco AC automatico",
            "nl": "AC automatisch ontgrendelen",
        },
        "states": {
            "AUTO_UNLOCK_AC_INVALID": {
                "en": "Invalid",
                "de": "Ungültig",
                "fr": "Invalide",
                "it": "Non valido",
                "nl": "Ongeldig",
            },
            "AUTO_UNLOCK_AC_OFF": {
                "en": "Off",
                "de": "Aus",
                "fr": "Arrêt",
                "it": "Spento",
                "nl": "Uit",
            },
            "AUTO_UNLOCK_AC_ONCE": {
                "en": "Once",
                "de": "Einmalig",
                "fr": "Une fois",
                "it": "Una volta",
                "nl": "Eenmalig",
            },
            "AUTO_UNLOCK_AC_PERMANENT": {
                "en": "Permanent",
                "de": "Dauerhaft",
                "fr": "Permanent",
                "it": "Permanente",
                "nl": "Permanent",
            },
        },
    },
    "bcam_activation": {
        "names": {
            "en": "BCAM activation",
            "de": "BCAM-Aktivierung",
            "fr": "Activation BCAM",
            "it": "Attivazione BCAM",
            "nl": "BCAM-activering",
        },
        "states": {
            "BCAM_ACTIVATION_ACTIVATED": {
                "en": "Activated",
                "de": "Aktiviert",
                "fr": "Activé",
                "it": "Attivato",
                "nl": "Geactiveerd",
            },
            "BCAM_ACTIVATION_DEACTIVATED": {
                "en": "Deactivated",
                "de": "Deaktiviert",
                "fr": "Désactivé",
                "it": "Disattivato",
                "nl": "Gedeactiveerd",
            },
        },
    },
    "charging_timer_reachability": {
        "names": {
            "en": "Charging timer reachability",
            "de": "Lade-Timer erreichbar",
            "fr": "Atteinte minuterie charge",
            "it": "Raggiungibilità timer carica",
            "nl": "Laadtimer haalbaarheid",
        },
        "states": {
            "TARGET_REACHABILITY_CALCULATING": {
                "en": "Calculating",
                "de": "Berechnet",
                "fr": "Calcul en cours",
                "it": "Calcolo in corso",
                "nl": "Berekenen",
            },
            "TARGET_REACHABILITY_REACHABLE": {
                "en": "Reachable",
                "de": "Erreichbar",
                "fr": "Atteignable",
                "it": "Raggiungibile",
                "nl": "Haalbaar",
            },
            "TARGET_REACHABILITY_NOT_REACHABLE": {
                "en": "Not reachable",
                "de": "Nicht erreichbar",
                "fr": "Non atteignable",
                "it": "Non raggiungibile",
                "nl": "Niet haalbaar",
            },
        },
    },
    "window_heating_state": {
        "names": {
            "en": "Window heating",
            "de": "Scheibenheizung",
            "fr": "Chauffage vitres",
            "it": "Riscaldamento vetri",
            "nl": "Ruitverwarming",
        },
        "states": {
            "WINDOW_HEATING_STATE_OFF": {
                "en": "Off",
                "de": "Aus",
                "fr": "Arrêt",
                "it": "Spento",
                "nl": "Uit",
            },
            "WINDOW_HEATING_STATE_ON": {
                "en": "On",
                "de": "An",
                "fr": "Marche",
                "it": "Acceso",
                "nl": "Aan",
            },
        },
    },
    "charging_state": {
        "names": {
            "en": "Charge state",
            "de": "Ladestatus",
            "fr": "État de charge",
            "it": "Stato di carica",
            "nl": "Laadstatus",
        },
        "states": {
            "off": {
                "en": "Off",
                "de": "Aus",
                "fr": "Arrêt",
                "it": "Spento",
                "nl": "Uit",
            },
            "charging": {
                "en": "Charging",
                "de": "Lädt",
                "fr": "En charge",
                "it": "In carica",
                "nl": "Laden",
            },
            "error": {
                "en": "Error",
                "de": "Fehler",
                "fr": "Erreur",
                "it": "Errore",
                "nl": "Fout",
            },
            "conserving": {
                "en": "Conserving",
                "de": "Erhaltung",
                "fr": "Conservation",
                "it": "Conservazione",
                "nl": "Behoud",
            },
        },
    },
    "charging_mode": {
        "names": {
            "en": "Charge mode",
            "de": "Lademodus",
            "fr": "Mode de charge",
            "it": "Modalità di carica",
            "nl": "Laadmodus",
        },
        "states": {
            "off": {
                "en": "Off",
                "de": "Aus",
                "fr": "Arrêt",
                "it": "Spento",
                "nl": "Uit",
            },
            "manual": {
                "en": "Manual",
                "de": "Manuell",
                "fr": "Manuel",
                "it": "Manuale",
                "nl": "Handmatig",
            },
            "timer1": {
                "en": "Timer 1",
                "de": "Timer 1",
                "fr": "Minuterie 1",
                "it": "Timer 1",
                "nl": "Timer 1",
            },
            "timer2": {
                "en": "Timer 2",
                "de": "Timer 2",
                "fr": "Minuterie 2",
                "it": "Timer 2",
                "nl": "Timer 2",
            },
            "invalid": {
                "en": "Invalid",
                "de": "Ungültig",
                "fr": "Invalide",
                "it": "Non valido",
                "nl": "Ongeldig",
            },
        },
    },
    "charging_reason_trigger": {
        "names": {
            "en": "Charging reason",
            "de": "Ladeauslöser",
            "fr": "Motif de charge",
            "it": "Motivo di carica",
            "nl": "Laadreden",
        },
        "states": {
            "timer1": {
                "en": "Timer 1",
                "de": "Timer 1",
                "fr": "Minuterie 1",
                "it": "Timer 1",
                "nl": "Timer 1",
            },
            "timer2": {
                "en": "Timer 2",
                "de": "Timer 2",
                "fr": "Minuterie 2",
                "it": "Timer 2",
                "nl": "Timer 2",
            },
            "immediate": {
                "en": "Immediate",
                "de": "Sofort",
                "fr": "Immédiat",
                "it": "Immediato",
                "nl": "Direct",
            },
        },
    },
    "last_battery_charger_update_trigger": {
        "names": {
            "en": "Charger update trigger",
            "de": "Ladegerät-Aktualisierung",
            "fr": "Déclencheur MAJ chargeur",
            "it": "Trigger aggiornamento caricatore",
            "nl": "Laadpaal-update trigger",
        },
        "states": {
            "clamp15Off": {
                "en": "Clamp 15 off",
                "de": "Klemme 15 aus",
                "fr": "Contact 15 coupé",
                "it": "Clamp 15 spento",
                "nl": "Klem 15 uit",
            },
        },
    },
}

# field_name -> translation_key (curated enum sensors)
FIELD_TRANSLATION_KEYS: dict[str, str] = {
    "charging_state_report.current_charge_state": "charge_state",
    "charging_state_report.charge_mode": "charge_mode",
    "charging_state_report.charge_type": "charge_type",
    "charging_state_report.charging_scenario": "charging_scenario",
    "charging_state_report.immediate_action_state": "immediate_action_state",
    "settings.charge_mode_selection": "charge_mode_selection",
    "settings.max_charge_current_ac": "max_ac_charge_current",
    "settings.auto_unlock_ac": "auto_unlock_ac",
    "setting.bcam_activation": "bcam_activation",
    "profile_state_report.next_charging_timer_information.target_reachability": (
        "charging_timer_reachability"
    ),
    "window_heating_state": "window_heating_state",
    "charging_state": "charging_state",
    "charging_mode": "charging_mode",
    "charging_reason_trigger": "charging_reason_trigger",
    "last_battery_charger_update_trigger": "last_battery_charger_update_trigger",
}


def build_entity_block(lang: str) -> dict:
    """Build HA ``entity.sensor`` and ``entity.binary_sensor`` blocks for one language."""
    from binary_name_labels import NAME_LABELS as BINARY_NAME_LABELS
    from sensor_name_labels import NAME_LABELS

    sensors: dict[str, dict] = {}
    for key, spec in NAME_LABELS.items():
        sensors[key] = {"name": spec["names"][lang]}
    for key, spec in SENSORS.items():
        entry: dict = {"name": spec["names"][lang]}
        if spec.get("states"):
            entry["state"] = {
                state_key: labels[lang] for state_key, labels in spec["states"].items()
            }
        sensors[key] = entry

    binary_sensors: dict[str, dict] = {}
    for key, spec in BINARY_NAME_LABELS.items():
        binary_sensors[key] = {"name": spec["names"][lang]}

    return {"sensor": sensors, "binary_sensor": binary_sensors}
