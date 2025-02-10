::: mermaid
classDiagram
    namespace view {
        class RootWindow {
            + MainWidget main_window
            %% Base layer der App 
        }
        class MainWidget {
            + Dict pages 
            %% Alle registrierten Widgets sind hier gespeichert, zum einfacheren Zugang
            + QStackedLayout layout 
            %% Ein Stack mit Funktionen (Qt eigene Klasse) der alle Widgets enthält.
            %% Es wird immer das Widget angezeigt dessen Index der currentIndex ist
        }
        class PlotWidget {
            %% vorläufig
            %% wird zu einer Monitoring Page
            %% Die unter anderem aber nicht ausschließlich die Visualisierung des CL enthält
            + update_visualization(dict)
            %% Soll Daten entgegennehmen und die Visualisierung entsprechend anpassen
            %% Enthält auch Pause
        }
        class StartWidget {
            %% vorläufig 
            %% wird zur Landing Page
            %% Soll Infos enthalten
        }
        class BaselineWidget {
            %% trivial
        }
        class Test {
            %% n-Back mit zwei BUttons "stimmt überein" und "stimmt nicht überein" 
        }
        class Skip {
            %% Zeigt Liste alter Sessions aus denen eine gewählt werden kann
            %% deren MaxWert genommen wird
            %% und Info zu "Wann geskipped werden kann"
        }
        class Retro {
            %% trivial
        }
    }
    namespace controller {
        class Controller
    }
    namespace model {
        class EEGMonitoring
        class KeyboardListener
    }
:::