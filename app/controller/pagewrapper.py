from abc import ABC, abstractmethod
from datetime import datetime

from PyQt6.QtWidgets import QWidget

from app.model import Phase
from app.model.score.hdf5Util import hdf5File
from app.util import MAX_PHASE_LENGTH, MIN_PHASE_LENGTH


class Page(ABC):
    def __init__(self, widget: QWidget, toolbar_shown: bool):
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
    def __init__(self, widget: QWidget, controller, next_page: str):
        super().__init__(widget, True)
        self.widget.user_input_entered.connect(
            lambda: controller.set_session_variables(
                self.widget.session_name, self.widget.jitsi_room_name
            )
        )
        self.widget.user_input_entered.connect(lambda: controller.next_page(next_page))

    def start(self, controller):
        self.widget.session_input.clear()
        self.widget.jitsi_input.clear()

    def reset(self, controller):
        self.widget.session_input.clear()
        self.widget.jitsi_input.clear()


class BaselineStartPage(Page):
    def __init__(
        self,
        widget: QWidget,
        controller,
        next_page_baseline_button: str,
        next_page_skip_button: str,
    ):
        super().__init__(widget, True)
        self.widget.monitor_baseline_button.clicked.connect(
            lambda: controller.next_page(next_page_baseline_button)
        )
        self.widget.dialog.yes_button.clicked.connect(
            lambda: controller.next_page(next_page_skip_button)
        )
        controller.recorder.phase_complete.connect(self.beep)

    def beep(self, phase: int):
        if phase == Phase.MIN.value:
            self.widget.beep()


class SkipPage(Page):
    def __init__(self, widget: QWidget, controller, next_page: str, previous_page: str):
        super().__init__(widget, True)
        self.widget.back_button.clicked.connect(
            lambda: controller.next_page(previous_page)
        )
        self.widget.sessionSelected.connect(controller.recorder.skip_min_max_phases)
        self.widget.next_button.clicked.connect(lambda: controller.next_page(next_page))

    def start(self, controller):
        self.widget.load_sessions()


class BaselinePage(Page):
    def __init__(self, widget: QWidget, controller, next_page: str):
        super().__init__(widget, False)

    def start(self, controller):
        controller.phase_change(Phase.MIN.value, MIN_PHASE_LENGTH)


class MaxtestPage(Page):
    def __init__(self, widget: QWidget, controller, next_page: str):
        super().__init__(widget, False)
        self.widget.correct_button.clicked.connect(
            lambda: controller.test_model.submit_answer(True)
        )
        self.widget.skip_button.clicked.connect(
            lambda: controller.test_model.submit_answer(False)
        )
        controller.test_model.show_correct_button.connect(
            self.widget.show_correct_button
        )
        controller.test_model.generated_char.connect(self.widget.updateChar)

    def start(self, controller):
        controller.phase_change(Phase.MAX.value, MAX_PHASE_LENGTH)
        controller.test_model.start_test()
        self.widget.hide_correct_button()


class MaxtestStartPage(Page):
    def __init__(self, widget: QWidget, controller, next_page: str):
        super().__init__(widget, True)
        widget.startMaxtestButton.clicked.connect(
            lambda: controller.next_page(next_page)
        )


class ResultPage(Page):
    def __init__(self, widget: QWidget, controller, next_page: str):
        super().__init__(widget, False)
        widget.next_button.clicked.connect(lambda: controller.next_page(next_page))

    def start(self, controller):
        self.widget.updateResult(controller.test_model.calculate_result())


class JitsiPage(Page):
    def __init__(self, widget: QWidget, controller, next_page: str):
        super().__init__(widget, False)
        self.widget.dialog.exit_button.clicked.connect(
            lambda: controller.next_page(next_page)
        )
        self.widget.dialog.exit_button.clicked.connect(
            lambda: controller.phase_change(Phase.PAUSED.value)
        )
        self.widget.dialog.exit_button.clicked.connect(self.widget.end_meeting)

        self.widget.commentSignal.connect(
            lambda: controller.recorder.save_comment(
                datetime.now().timestamp(), self.widget.comment
            )
        )
        self.widget.break_button.clicked.connect(
            lambda: self.toggle_monitoring(controller)
        )

        # Observer view > model
        controller.recorder.powers.connect(
            lambda powers: self.widget.plot_widget.update_score(powers["load_score"])
        )

    def toggle_monitoring(self, controller):
        if self.widget.break_button.text() == "Resume":
            controller.phase_change(Phase.PAUSED.value)
        else:
            controller.phase_change(Phase.MONITOR.value)

    def start(self, controller):
        try:
            display_name = controller.settings_model.settings["displayName"]
        except KeyError:
            display_name = None
        self.widget.load_jitsi_meeting(controller.jitsi_room_name, display_name)
        controller.phase_change(Phase.MONITOR.value)


class RetrospectivePage(Page):
    def __init__(self, widget: QWidget, controller):
        super().__init__(widget, True)
        widget.back_button.clicked.connect(controller.new_session)

    def start(self, controller):
        controller.check_last_session()
        self.widget.load_sessions()
