class DetectorConfig:
    # -----------------------------------
    # ISOLATION FOREST
    # -----------------------------------

    ISOLATION_FOREST = {
        # Schwierigkeitsgrad: wie schwer ist es, anomal zu sein
        # Erwarteter Anteil an Anomalien im Datensatz
        # Jetzt 5% sind vermutlich ungewöhnlich
        "contamination": 0.05,
        # Wie viele Bäume wir brauchen - Anzahl der Entscheidungsbäume
        "n_estimators": 100,
        # Zufalls-Seed - damit bei jedem Lauf dieselben Zufallszahllen genutzt werden
        "random_state": 42,
    }

    # -----------------------------------
    # LOCAL OUTLIER FACTOR
    # -----------------------------------

    LOF = {
        # Schwierigkeitsgrad: wie schwer ist es, anomal zu sein
        # Gleiche Bedeutung wie bei Isolation Forest
        # Jetzt 5% sind vermutlich anomal
        "contamination": 0.05,
        # Wir wollen 20 Nachbarn betrachten
        "n_neighbors": 20,
        # Distanzmaß zur Berechnung der Nähe zwischen Punkten
        # Bei Audio-Samples misst das: wie ähnlich oder
        # unterschiedlich zwei Audio-Samples sind
        # Anomal bei LOF: Anomalien haben eine geringere lokale Dichte
        "metric": "euclidean",
    }
