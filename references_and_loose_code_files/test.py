
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PyQt6.QtCore import QUrl

class JitsiApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins, True)

        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        )

        self.browser.setUrl(QUrl("https://meet.jit.si/ThisIsATestMeeting")) # Hier Meetinglink einfügen

        self.setGeometry(100, 100, 1280, 720)
        self.setWindowTitle("Jitsi in PyQt6")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JitsiApp()
    window.show()
    sys.exit(app.exec())


"""
Nicht alle Einstellungen sind wahrscheinlich notwendig, aber ich habe sie mal hinzugefügt, damit ich nicht alles durchprobieren muss, wenn es nicht funktioniert.
Im Log sind auserdem noch einige Fehlermeldungen, die bearbeitet werden müssen. Vieles häbgt vermutlich mit dem nicht erlaubten Audio zusammen


Log:
js: 2025-01-31T18:31:26.696Z [features/base/sounds] PLAY_SOUND: no sound found for id: RECORDING_OFF_SOUND
js: 2025-01-31T18:31:26.700Z [features/base/sounds] PLAY_SOUND: no sound found for id: RECORDING_OFF_SOUND
js: The AudioContext was not allowed to start. It must be resumed (or created) after a user gesture on the page. https://goo.gl/7K7WLu
js: 2025-01-31T18:31:26.841Z [features/hid] <YV.sendDeviceReport>:  There are currently non-compliant conditions
js: 2025-01-31T18:31:27.157Z [modules/RTC/RTCUtils.js] Failed to get access to local media. NotFoundError: Requested device not found {"video":{"height":{"ideal":720,"max":720,"min":180},"width":{"ideal":1280,"max":1280,"min":320},"frameRate":{"max":30}},"audio":{"autoGainControl":true,"echoCancellation":true,"noiseSuppression":true}}
js: 2025-01-31T18:31:27.158Z [features/base/tracks] Failed to create local tracks audio,video [object Object]
js: 2025-01-31T18:32:27.171Z [features/base/tracks] Failed to create local tracks audio [object Object]
js: 2025-01-31T18:32:27.172Z [features/base/tracks] Failed to create local tracks video [object Object]
js: 2025-01-31T18:32:27.172Z [features/base/tracks] Audio track creation failed with error gum.timeout: Could not start media source. Timeout occurred!
js: 2025-01-31T18:32:27.172Z [features/base/tracks] Video track creation failed with error gum.timeout: Could not start media source. Timeout occurred!
js: 2025-01-31T18:32:27.534Z [features/base/conference] Error while requesting wake lock for screen: NotAllowedError: Wake Lock permission request denied
[20608:1600:0131/193227.619:ERROR:socket_manager.cc(141)] Failed to resolve address for meet-jit-si-turnrelay.jitsi.net., errorcode: -105
[20608:1600:0131/193227.655:ERROR:socket_manager.cc(141)] Failed to resolve address for meet-jit-si-turnrelay.jitsi.net., errorcode: -105
[20608:1600:0131/193227.656:ERROR:socket_manager.cc(141)] Failed to resolve address for meet-jit-si-turnrelay.jitsi.net., errorcode: -105
js: Platform browser has already been set. Overwriting the platform with [object Object].
js: The kernel '_FusedMatMul' for backend 'wasm' is already registered
js: The kernel 'Abs' for backend 'wasm' is already registered
js: The kernel 'Add' for backend 'wasm' is already registered
js: The kernel 'AddN' for backend 'wasm' is already registered
js: The kernel 'All' for backend 'wasm' is already registered
js: The kernel 'Any' for backend 'wasm' is already registered
js: The kernel 'ArgMax' for backend 'wasm' is already registered
js: The kernel 'AvgPool' for backend 'wasm' is already registered
js: The kernel 'BatchMatMul' for backend 'wasm' is already registered
js: The kernel 'BatchToSpaceND' for backend 'wasm' is already registered
js: The kernel 'Cast' for backend 'wasm' is already registered
js: The kernel 'Ceil' for backend 'wasm' is already registered
js: The kernel 'ClipByValue' for backend 'wasm' is already registered
js: The kernel 'Concat' for backend 'wasm' is already registered
js: The kernel 'Conv2D' for backend 'wasm' is already registered
js: The kernel 'Conv2DBackpropInput' for backend 'wasm' is already registered
js: The kernel 'Cos' for backend 'wasm' is already registered
js: The kernel 'Cosh' for backend 'wasm' is already registered
js: The kernel 'CropAndResize' for backend 'wasm' is already registered
js: The kernel 'Cumsum' for backend 'wasm' is already registered
js: The kernel 'DepthToSpace' for backend 'wasm' is already registered
js: The kernel 'DepthwiseConv2dNative' for backend 'wasm' is already registered
js: The kernel 'Elu' for backend 'wasm' is already registered
js: The kernel 'Equal' for backend 'wasm' is already registered
js: The kernel 'Exp' for backend 'wasm' is already registered
js: The kernel 'ExpandDims' for backend 'wasm' is already registered
js: The kernel 'Fill' for backend 'wasm' is already registered
js: The kernel 'FlipLeftRight' for backend 'wasm' is already registered
js: The kernel 'Floor' for backend 'wasm' is already registered
js: The kernel 'FloorDiv' for backend 'wasm' is already registered
js: The kernel 'FusedBatchNorm' for backend 'wasm' is already registered
js: The kernel 'FusedConv2D' for backend 'wasm' is already registered
js: The kernel 'FusedDepthwiseConv2D' for backend 'wasm' is already registered
js: The kernel 'GatherNd' for backend 'wasm' is already registered
js: The kernel 'GatherV2' for backend 'wasm' is already registered
js: The kernel 'Greater' for backend 'wasm' is already registered
js: The kernel 'GreaterEqual' for backend 'wasm' is already registered
js: The kernel 'Identity' for backend 'wasm' is already registered
js: The kernel 'LeakyRelu' for backend 'wasm' is already registered
js: The kernel 'Less' for backend 'wasm' is already registered
js: The kernel 'LessEqual' for backend 'wasm' is already registered
js: The kernel 'Log' for backend 'wasm' is already registered
js: The kernel 'LogicalAnd' for backend 'wasm' is already registered
js: The kernel 'Max' for backend 'wasm' is already registered
js: The kernel 'Maximum' for backend 'wasm' is already registered
js: The kernel 'MaxPool' for backend 'wasm' is already registered
js: The kernel 'Mean' for backend 'wasm' is already registered
js: The kernel 'Min' for backend 'wasm' is already registered
js: The kernel 'Minimum' for backend 'wasm' is already registered
js: The kernel 'MirrorPad' for backend 'wasm' is already registered
js: The kernel 'Multiply' for backend 'wasm' is already registered
js: The kernel 'Neg' for backend 'wasm' is already registered
js: The kernel 'NonMaxSuppressionV3' for backend 'wasm' is already registered
js: The kernel 'NonMaxSuppressionV4' for backend 'wasm' is already registered
js: The kernel 'NonMaxSuppressionV5' for backend 'wasm' is already registered
js: The kernel 'NotEqual' for backend 'wasm' is already registered
js: The kernel 'OneHot' for backend 'wasm' is already registered
js: The kernel 'OnesLike' for backend 'wasm' is already registered
js: The kernel 'Pack' for backend 'wasm' is already registered
js: The kernel 'PadV2' for backend 'wasm' is already registered
js: The kernel 'Pow' for backend 'wasm' is already registered
js: The kernel 'Prelu' for backend 'wasm' is already registered
js: The kernel 'Prod' for backend 'wasm' is already registered
js: The kernel 'Range' for backend 'wasm' is already registered
js: The kernel 'RealDiv' for backend 'wasm' is already registered
js: The kernel 'Relu' for backend 'wasm' is already registered
js: The kernel 'Relu6' for backend 'wasm' is already registered
js: The kernel 'Reshape' for backend 'wasm' is already registered
js: The kernel 'ResizeBilinear' for backend 'wasm' is already registered
js: The kernel 'Reverse' for backend 'wasm' is already registered
js: The kernel 'RotateWithOffset' for backend 'wasm' is already registered
js: The kernel 'Round' for backend 'wasm' is already registered
js: The kernel 'Rsqrt' for backend 'wasm' is already registered
js: The kernel 'ScatterNd' for backend 'wasm' is already registered
js: The kernel 'Select' for backend 'wasm' is already registered
js: The kernel 'Sigmoid' for backend 'wasm' is already registered
js: The kernel 'Sin' for backend 'wasm' is already registered
js: The kernel 'Slice' for backend 'wasm' is already registered
js: The kernel 'Softmax' for backend 'wasm' is already registered
js: The kernel 'SpaceToBatchND' for backend 'wasm' is already registered
js: The kernel 'SparseFillEmptyRows' for backend 'wasm' is already registered
js: The kernel 'SparseReshape' for backend 'wasm' is already registered
js: The kernel 'SparseSegmentMean' for backend 'wasm' is already registered
js: The kernel 'SparseSegmentSum' for backend 'wasm' is already registered
js: The kernel 'SplitV' for backend 'wasm' is already registered
js: The kernel 'Sqrt' for backend 'wasm' is already registered
js: The kernel 'Square' for backend 'wasm' is already registered
js: The kernel 'SquaredDifference' for backend 'wasm' is already registered
js: The kernel 'Step' for backend 'wasm' is already registered
js: The kernel 'StridedSlice' for backend 'wasm' is already registered
js: The kernel 'Sub' for backend 'wasm' is already registered
js: The kernel 'Sum' for backend 'wasm' is already registered
js: The kernel 'Tan' for backend 'wasm' is already registered
js: The kernel 'Tanh' for backend 'wasm' is already registered
js: The kernel 'Tile' for backend 'wasm' is already registered
js: The kernel 'TopK' for backend 'wasm' is already registered
js: The kernel 'Transform' for backend 'wasm' is already registered
js: The kernel 'Transpose' for backend 'wasm' is already registered
js: The kernel 'Unpack' for backend 'wasm' is already registered
js: The kernel 'ZerosLike' for backend 'wasm' is already registered
js: wasm backend was already registered. Reusing existing backend factory.
js: Failed to create WebGPU Context Provider
"""