from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
)
from PyQt6.QtGui import QPixmap
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
from datetime import datetime, timedelta

from app.util import HDF5_FOLDER_PATH, FILE_PATH_INFO_ICON, getAbsPath
from app.model.score.hdf5Util import hdf5File
import mplcursors


class RetrospectivePage(QWidget):
    def __init__(self):
        super().__init__()
        self.session_folder = getAbsPath(HDF5_FOLDER_PATH)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.page_explanation = QLabel(
            "Plot your past sessions to track cognitive load over time. "
            "Choose a single session for precise time values and comments or "
            "multiple for normalized times. "
            "In single-session plots, hover over the dots to view your comments."
        )
        self.page_explanation.setObjectName("text")
        self.page_explanation.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.page_explanation.setWordWrap(True)
        layout.addWidget(self.page_explanation)

        self.session_list = QListWidget()
        self.session_list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )
        layout.addWidget(self.session_list)

        # button for plotting
        self.plot_button = QPushButton("Plot Sessions")
        self.plot_button.clicked.connect(self._plot_sessions)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.plot_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self.delete_button = QPushButton("Delete Selected Sessions")
        self.delete_button.clicked.connect(self._delete_sessions)
        h_layout.addWidget(self.delete_button, alignment=Qt.AlignmentFlag.AlignLeft)

        h_layout.addItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )

        # Info Icon
        self.info_icon = QLabel(self)
        path_info_icon = getAbsPath(FILE_PATH_INFO_ICON)
        self.info_icon.setPixmap(
            QPixmap(str(path_info_icon)).scaled(
                32,
                32,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.info_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        self.info_icon.setToolTip(
            "The score displayed represents your Cognitive Load (CL) score."
            " It is calculated using various values recorded by the headphones"
            " and processed through a formula to standardize it, allowing for"
            " comparison with your previous sessions."
        )  # Tooltip for new icon
        self.info_icon.setAlignment(Qt.AlignmentFlag.AlignRight)
        h_layout.addWidget(self.info_icon, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(h_layout)

        # Matplotlib-Canvas for plotting
        self.figure = Figure(facecolor="#F8F8FF", edgecolor="#444444")
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.load_sessions()

        self.back_button = QPushButton("Back to Homepage")
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignRight)

    def load_sessions(self):
        """Loads the h5 files"""
        self.session_list.clear()
        if os.path.exists(self.session_folder):
            files = [f for f in os.listdir(self.session_folder) if f.endswith(".h5")]

            def extract_index(file_name):
                file_name = str(file_name)
                index = file_name.split("__")[0].strip()
                return int(index)

            files.sort(key=extract_index, reverse=True)
            for file in files:
                self.session_list.addItem(file)

    def _plot_sessions(self):
        """
        Plots the selected sessions. If you select only one session, you can see the session's time course with times
        on the x-axis.
        If you select multiple sessions, the times are normalized and all courses start at 0.
        """
        selected_files = [item.text() for item in self.session_list.selectedItems()]
        if not selected_files:
            self.show_popup(
                "No sessions selected", "Please select at least one session to plot."
            )
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        for file in selected_files:
            length = 0
            try:
                file_path = os.path.join(self.session_folder, file)
                (
                    modified_timestamps,
                    modified_load_score,
                    timestamps_marker,
                    y_marker,
                    descriptions,
                ) = hdf5File.plot_file(file_path)

                if len(selected_files) == 1:
                    ax.plot(
                        [
                            datetime.fromtimestamp(t).strftime("%H:%M:%S")
                            for t in modified_timestamps
                        ],
                        modified_load_score,
                        label=file,
                    )
                    length = len(modified_timestamps)

                    scatter = ax.scatter(
                        [
                            datetime.fromtimestamp(t).strftime("%H:%M:%S")
                            for t in timestamps_marker
                        ],
                        y_marker,
                        color="red",
                        label="comments",
                        marker="o",
                        s=50,
                    )
                    cursor = mplcursors.cursor(scatter, hover=True)

                    @cursor.connect("add")
                    def on_hover(sel):
                        sel.annotation.set_text(descriptions[sel.index].decode())
                        sel.annotation.get_bbox_patch().set_facecolor(
                            "lightblue"
                        )
                        sel.annotation.get_bbox_patch().set_edgecolor(
                            "black"
                        )

                else:
                    # Normalize the timeline
                    timestamps_rel = modified_timestamps - modified_timestamps[0]
                    length = (
                        len(timestamps_rel) if len(timestamps_rel) > length else length
                    )
                    formatted_rel_times = [
                        str(timedelta(seconds=int(t))) for t in timestamps_rel
                    ]
                    ax.plot(formatted_rel_times, modified_load_score, label=file)
            except Exception as e:
                print(f"Error while plotting {file}: {e}")

        if len(selected_files) == 1:
            session_name = file.split("__")[1]
            date = file.split("__")[2].split("_")[1].split(".")[0]
            ax.set_title(
                f"Session: {session_name} on {date}",
                fontsize=12,
                fontweight="semibold",
                pad=10,
            )

        ax.set_xlabel(
            (
                "Time (HH:MM:SS)"
                if len(selected_files) == 1
                else "Session Duration (HH:MM:SS)"
            ),
            fontsize=6,
            fontweight="bold",
        )
        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.set_ylabel("Cognitive Load", fontsize=12, fontweight="bold", labelpad=15)
        ax.tick_params(axis="both", labelsize=10)
        ax.legend(loc="upper left", bbox_to_anchor=(-0.16, 1.15), borderaxespad=0.0)
        ax.grid(True, linestyle="--", color="gray", linewidth=1, alpha=0.75)

        self.canvas.draw()

    def _delete_sessions(self):
        """Delete a session when user confirmes"""
        selected_files = [item.text() for item in self.session_list.selectedItems()]
        if not selected_files:
            self.show_popup(
                "No sessions selected", "Please select at least one session to delete."
            )
            return
        # Show confirmation popup
        confirmation = QMessageBox(self)
        confirmation.setIcon(QMessageBox.Icon.Warning)
        confirmation.setWindowTitle("Delete Confirmation")
        confirmation.setText(
            f"Are you sure you want to delete the selected sessions? You cannot recover the files afterwards: "
            f"{', '.join(selected_files)}"
        )
        confirmation.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        confirmation = confirmation.exec()

        if confirmation == QMessageBox.StandardButton.Yes:
            # Delete the selected sessions
            for file in selected_files:
                file_path = os.path.join(self.session_folder, file)
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Session {file} has been deleted.")
                    else:
                        print(f"Session {file} not found.")
                except Exception as e:
                    print(f"Error while deleting {file}: {e}")

            # Load the remaining sessions after deleting
            self.load_sessions()

    def show_popup(self, title, message):
        """Warn pop up before deleting a session. User needs to confirm it."""
        popup = QMessageBox(self)
        popup.setWindowTitle(title)
        popup.setText(message)
        popup.setIcon(QMessageBox.Icon.Warning)
        popup.setStandardButtons(QMessageBox.StandardButton.Ok)
        popup.exec()
