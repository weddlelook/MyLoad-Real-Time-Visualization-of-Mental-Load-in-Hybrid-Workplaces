from PyQt6.QtCore import QObject, pyqtSignal
from sklearn.decomposition import FastICA


class ICAWorker(QObject):
    """Worker class to train ICA in a separate thread."""

    finished = pyqtSignal(object)

    def __init__(self, eeg_data):
        super().__init__()
        self.eeg_data = eeg_data

    def run(self):
        ica = FastICA(
            n_components=self.eeg_data.shape[0],
            max_iter=2000,
            tol=0.005,
            whiten="arbitrary-variance",
        )
        ica.fit(self.eeg_data.T)
        self.finished.emit(ica)

    # ---------------- ICA -----------------

    def apply_ica(self, new_data):
        """Apply trained ICA to new 1-second EEG chunk."""
        if self.ica_model is None:
            return new_data  # Return raw EEG if ICA isn’t trained yet

        new_data = self.clean_eeg_data(new_data)

        try:
            # Apply ICA transformation
            transformed = np.dot(self.ica_model.components_, new_data)  # Unmix sources
            cleaned_data = np.dot(
                np.linalg.pinv(self.ica_model.components_), transformed
            )  # Reconstruct EEG
            return cleaned_data

        except Exception as e:
            self.status_callback.emit(f"Error in ICA application: {e}")
            return new_data  # Return raw data if ICA fails

    def start_ica_training(self):
        """Start ICA training in a separate thread."""
        print("Starting ICA training thread...")

        # Check if enough data is available for training
        if (
            self.data_buffer is None
            or self.data_buffer.shape[1] < self.sampling_rate * 10
        ):
            print("Not enough data for ICA training. Need at least 10 seconds of EEG.")
            return

        self.ica_thread = QThread()
        data = self.clean_eeg_data(self.data_buffer)

        if np.var(data, axis=1).min() < 1e-6:
            print("Warning: EEG data has very low variance! ICA may fail.")

        self.ica_worker = ICAWorker(data)  # Pass cleaned EEG data
        self.ica_worker.moveToThread(self.ica_thread)

        # Connect signals
        self.ica_thread.started.connect(self.ica_worker.run)
        self.ica_worker.finished.connect(self.store_trained_ica)
        self.ica_worker.finished.connect(
            self.ica_thread.quit
        )  # Stop thread when training is done
        self.ica_worker.finished.connect(self.ica_worker.deleteLater)  # Cleanup
        self.ica_thread.finished.connect(self.ica_thread.deleteLater)  # Cleanup

        self.ica_thread.start()

    def store_trained_ica(self, trained_ica):
        """Store the trained ICA model from the worker thread."""
        self.ica_model = trained_ica
        print("New ICA model stored!")

    # ---------------- Threshhold -----------

    def _moving_average(self, cl_value):
        """
        Replace invalid cognitive load values with mean of prior valid values.
        :return: Valid value as given, average if invalid or none if the value is invalid and not enough valid values are available in the sliding window.
        """

        # Append value if valid, otherwise append None
        self._threshold_filter(cl_value)

        # Filter for valid values
        valid_values = [v for v in self.filter_window if v is not None]

        if len(valid_values) >= 1:
            return np.mean(valid_values)
        else:
            return (
                cl_value if cl_value <= self.THRESHOLD_UPPER else self.THRESHOLD_UPPER
            )

    def _threshold_filter(self, cl_value):
        if cl_value <= self.THRESHOLD_UPPER:
            self.filter_window.append(cl_value)
            return cl_value
        else:
            self.filter_window.append(None)
            return None
