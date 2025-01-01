## Node Sync Monitor

The **Node Sync Monitor** is a Python-based tool designed to monitor the synchronization status of your Solana node. It compares your node's current slot with that of a trusted reference node and sends a Telegram notification when the slot difference exceeds a predefined threshold, indicating that your node is out of sync.

---

### Features

- **Real-Time Monitoring**: Checks your node's current slot against a trusted reference node's slot.
- **Threshold-Based Alerts**: Sends a Telegram notification if the slot difference exceeds the defined threshold.
- **Configurable Settings**: Customize RPC URLs, Telegram bot credentials, check intervals, and sync thresholds using a `.env` file.
- **Error Handling**: Logs issues like network errors or unreachable nodes.

---

### Requirements

- Python 3.7 or higher
- `requests` library
- `python-dotenv` library

---

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kiennd/solana-rpc-monitor.git
   cd solana-rpc-monitor
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` File**:
   Create a `.env` file in the project directory with the following configuration:
   ```plaintext
      LOCAL_RPC_URL=http://localhost:8899
      REFERENCE_RPC_URL=https://api.mainnet-beta.solana.com
      TELEGRAM_BOT_TOKEN=
      TELEGRAM_CHAT_ID=
      CHECK_INTERVAL=10
      SYNC_THRESHOLD=100

   ```

   Replace the placeholders with:
   - `LOCAL_RPC_URL`: Your Solana node's RPC URL.
   - `REFERENCE_RPC_URL`: A stable reference node's RPC URL.
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
   - `TELEGRAM_CHAT_ID`: Your Telegram chat ID.
   - `CHECK_INTERVAL`: Time (in seconds) between checks.
   - `SYNC_THRESHOLD`: Maximum acceptable slot difference before alerting.

---

### Usage

1. **Run the Script**:
   ```bash
   python run.py
   ```

2. **Monitor Logs**:
   Logs will be saved in the `node_sync_monitor.log` file and printed to the console.

---

### Example Output

1. **Console Output**:
   ```
   2025-01-01 10:00:00 - INFO - Local slot: 311229354, Reference slot: 311229400, Difference: 46
   2025-01-01 10:00:10 - INFO - Node is in sync.
   ```

2. **Telegram Notification**:
   ```
   ⚠️ Node is out of sync!
   Local slot: 311228900
   Reference slot: 311229500
   Difference: 600 slots
   ```

---

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
