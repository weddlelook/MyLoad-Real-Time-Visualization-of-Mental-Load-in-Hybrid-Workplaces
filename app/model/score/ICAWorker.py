from PyQt6.QtCore import QObject, pyqtSignal
from sklearn.decomposition import FastICA

class ICAWorker(QObject):
    """Worker class to train ICA in a separate thread."""
    finished = pyqtSignal(object)

    def __init__(self, eeg_data):
        super().__init__()
        self.eeg_data = eeg_data

    def run(self):
        ica = FastICA(n_components=self.eeg_data.shape[0], max_iter=2000, tol=0.005, whiten='arbitrary-variance')
        ica.fit(self.eeg_data.T) 
        self.finished.emit(ica)