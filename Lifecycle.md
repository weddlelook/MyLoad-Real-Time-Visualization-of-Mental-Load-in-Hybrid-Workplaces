```mermaid
graph TD;
    * --> Landing_Page

    Landing_Page --> Baseline
    Landing_Page --> Retrospektive/Alte_Sessions

    Baseline --> Test
    Baseline --> Auswahl_alte_Werte

    Auswahl_alte_Werte --> Monitoring

    Test --> Monitoring

    Monitoring --> Pause
    Monitoring --> Retrospektive/Alte_Sessions

    Pause --> Retrospektive/Alte_Sessions
    Pause --> Monitoring


    Retrospektive/Alte_Sessions --> [*]
    Retrospektive/Alte_Sessions --> Landing_Page

```