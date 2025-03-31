# TES_MyLoad

## Requirements

Before you can run this code, you will need to install our dependency manager [Poetry](https://python-poetry.org/docs/).

### Installation

#### Windows
1. Run the following command in Powershell 
   ```powershell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   ```
3. Close and reopen your terminal (PowerShell or Command Prompt) to ensure changes take effect.
4. Verify the installation by running:
   ```sh
   poetry --version
   ```
5. Navigate to the root of the project and install dependencies:
   ```sh
   poetry install
   ```

#### Linux & macOS
1. Open a terminal and install Poetry with the following command:
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```
2. Ensure Poetry is available in your shell by adding it to your PATH:
   ```sh
   export PATH="$HOME/.local/bin:$PATH"
   ```
3. Verify the installation by running:
   ```sh
   poetry --version
   ```
4. Navigate to the root of the project and install dependencies:
   ```sh
   poetry install
   ```

If this does not work for you, here is a link to the [offical tutorials](https://python-poetry.org/docs/)

## Run Application

Navigate into the root of this directory, then run the project using:
```sh
poetry run python -m app
```

This will start the application with synthetic data. 

### Running with EEG-Headphones
To use the application with EEG-Headphones, start it with the following arguments:
```sh
poetry run python -m app --board_id 0 --port <your_usb_port>
```

If you don't specify the port, `COM3` is chosen by default. If this is not your serial-port you need to find and specify it.

#### Finding Your USB Port

- **Windows:** Open Command Prompt and run:
  ```sh
  wmic path Win32_SerialPort get DeviceID,Name
  ```
- **Linux:** Run the following command:
  ```sh
  ls /dev/tty*
  ```
  Your USB port will be listed as `/dev/ttyUSBX` or `/dev/ttySX`.
- **macOS:** Run:
  ```sh
  ls /dev/tty.*
  ```
  Your port will appear as `/dev/tty.usbmodemXXXX` or `/dev/tty.usbserial-XXXXX`.

Now, replace `<your_usb_port>` with the correct port and start the application.

## Jitsi

For demonstration, the current host is [meet.jit.si](https://meet.jit.si), which now has a 5-minute limit and is only recommended for testing purposes. 
You can use **Jitsi as a Service (JAAS)** by signing up for a JAAS account at [Jitsi as a Service](https://jaas.8x8.vc/).
Alternatively, to host your own Jitsi instance follow the official Jitsi self-hosting guide: [Self-Hosting Jitsi Meet](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-start).
If you are modifying the host, update the file: `app/res/styles/jitsi.html` accordingly.