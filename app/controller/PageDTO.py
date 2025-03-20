from abc import ABC, abstractmethod
from datetime import datetime

import h5py
from PyQt6.QtWidgets import QWidget
from app.model.score.hdf5Util import hdf5File

class Page(ABC):
    def __init__(self, widget:QWidget, toolbar_shown:bool):
        self.widget = widget
        self.toolbar_shown = toolbar_shown
        self.hdf5_marker = hdf5File

    def start(self, controller):
        """
        This method is called only when the page is shown.
        Please initalize all connections that can be made before that in the constructor
        (otherwise we will have two connections, meaning that the functions is gonna be called twice!).
        Only actions that should be performed once the page is shown should be placed here.
        """
        pass

    def reset(self, controller):
        """
        Reset the page to its initial state e.g. when an error occurs or a new session is started.
        """
        pass

class StartPage(Page):
    def __init__(self, widget:QWidget, controller, next_page:str):
        super().__init__(widget, True)
        self.widget.user_input_entered.connect(lambda: controller.set_session_variables(self.widget.session_name, self.widget.jitsi_room_name))
        self.widget.user_input_entered.connect(lambda: controller.next_page(next_page))

    def start(self, controller):
        self.widget.session_input.clear()
        self.widget.jitsi_input.clear()

    def reset(self, controller):
        self.widget.session_input.clear()
        self.widget.jitsi_input.clear()

class BaselineStartPage(Page):
    def __init__(self, widget:QWidget, controller, next_page_baseline_button:str, next_page_skip_button:str):
        super().__init__(widget, True)
        self.widget.monitor_baseline_button.clicked.connect(lambda: controller.next_page(next_page_baseline_button))
        self.widget.dialog.yes_button.clicked.connect(lambda: controller.next_page(next_page_skip_button))

class SkipPage(Page):
    def __init__(self, widget: QWidget, controller, next_page: str, previous_page: str):
        super().__init__(widget, True)
        self.widget.back_button.clicked.connect(lambda: controller.next_page(previous_page))
        self.widget.sessionSelected.connect(lambda: controller.recorder.save_previous_min_max_values(self.widget.selected_file))
        self.widget.next_button.clicked.connect(lambda:  controller.next_page(next_page))

    def start(self, controller):
        self.widget.load_sessions()

class BaselinePage(Page):
    def __init__(self, widget:QWidget, controller, next_page:str):
        super().__init__(widget, False)

    def start(self, controller):
        controller.start_min()

class MaxtestPage(Page):
    def __init__(self, widget:QWidget, controller, next_page:str):
        super().__init__(widget, False)
        self.widget.correct_button.clicked.connect(controller.maxtest_correct_button_clicked)
        self.widget.skip_button.clicked.connect(controller.maxtest_incorrect_button_clicked)
        controller.test_model.showButton.connect(self.widget.show_correct_button) # TODO
        controller.test_model.charSubmiter.connect(self.widget.updateChar) # TODO

    def start(self, controller):
        controller.start_max()
        controller.test_model.startTest() # TODO
        self.widget.hide_correct_button()

class MaxtestStartPage(Page):
    def __init__(self, widget:QWidget, controller, next_page:str):
        super().__init__(widget, True)
        widget.startMaxtestButton.clicked.connect(lambda: controller.next_page(next_page))


class ResultPage(Page):
    def __init__(self, widget:QWidget, controller, next_page:str):
        super().__init__(widget, False)
        widget.next_button.clicked.connect(lambda: controller.next_page(next_page))

    def start(self, controller):
        self.widget.updateResult(controller.get_maxtest_result())

class JitsiPage(Page):
    def __init__(self, widget:QWidget, controller, next_page:str):
        super().__init__(widget, False)
        self.controller = controller
        self.widget.dialog.exit_button.clicked.connect(lambda : controller.next_page(next_page))
        self.widget.dialog.exit_button.clicked.connect(controller.stop_monitoring)
        self.widget.dialog.exit_button.clicked.connect(self.widget.toggle_video) # TODO ersetze toogle_video durch end_meeting nach Evaluation
        #controller.recorder.powers.connect(self.widget.plot_widget.update_plot) # TODO
        controller.recorder.powers.connect(lambda powers: self.widget.plot_widget.updateScore(powers["load_score"]))

        self.widget.commentSignal.connect(lambda: controller.recorder.save_comment(datetime.now().timestamp(), self.widget.comment))

    def start(self, controller):
        try:
            display_name = controller.settings_model.settings['display_name']
        except KeyError:
            display_name = None
        #self.widget.load_jitsi_meeting(controller.jitsi_room_name, display_name) TODO for evaluation
        controller.start_monitoring()


class RetrospectivePage(Page):
    def __init__(self, widget:QWidget, controller):
        super().__init__(widget, True)
        widget.back_button.clicked.connect(controller.new_session)

    def start(self, controller):
        self.widget.load_sessions()