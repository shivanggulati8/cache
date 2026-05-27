# Location: QA/KompriseTestAutomationSuite/Library/CHAI/Features/DeepAnalytics/CustomActionUtil.py
# Use-Case: Match preaction, action and postaction logs in designated time interval
# Function:

# Below is TIMESTAMP_RE_2 which is a custom regex for function search_customaction_log_messages
import re

TIMESTAMP_RE_2 = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}", re.MULTILINE)

@staticmethod
    def search_customaction_log_messages(client, expected_output: str, start_time, end_time) -> list[str]:
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time.strip(), "%Y-%m-%d %H:%M:%S.%f")
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time.strip(), "%Y-%m-%d %H:%M:%S.%f")

        cmd = f"cat {CUSTOM_ACTION_LOG_PATH}"
        cmd_op = client.machine.execute_command(cmd, wait=True)

        if isinstance(cmd_op, dict):
            stdout = cmd_op.get("stdout")
        else:
            stdout = cmd_op[0]

        if hasattr(stdout, "read"):
            raw_log = stdout.read()
        else:
            raw_log = stdout

        raw_log = six.ensure_str(raw_log)

        # Strip SSH host prefix e.g. "[10.250.27.94] - " at the very start
        raw_log = re.sub(r'^\[\S+\] - ', '', raw_log)

        logging.info("raw_log first 300 chars (debugging): %r", raw_log[:300])
        logging.info("Timestamp RegEx match count: %d", len(TIMESTAMP_RE_2.findall(raw_log)))

        parts = TIMESTAMP_RE_2.split(raw_log)
        timestamps = TIMESTAMP_RE_2.findall(raw_log)

        logging.info("parts count: %d, timestamps count: %d", len(parts), len(timestamps))

        def parse_time(entry):
            try:
                return datetime.strptime(entry[:23], "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                return None

        all_entries = [(ts + body).strip() for ts, body in zip(timestamps, parts[1:])]
        entries = [e for e in all_entries if (t := parse_time(e)) and start_time <= t <= end_time]

        logging.info("=== Search Custom Action Log Messages ===")
        logging.info("Expected output  : %s", expected_output)
        logging.info("Time window      : %s  -->  %s", start_time, end_time)
        logging.info("Total entries in window: %d", len(entries))

        expected_lines = expected_output.strip().splitlines()
        n = len(expected_lines)
        results = []

        for i in range(len(entries) - n + 1):
            window = entries[i:i + n]

            window_messages = []
            for entry in window:
                match = MESSAGE_RE.search(entry)
                if match:
                    window_messages.append(match.group(1).strip())

            if len(window_messages) == n and all(exp in actual for exp, actual in zip(expected_lines, window_messages)):
                results.append("\n".join(window_messages))

        logging.info("Matches found: %d", len(results))
        for i, r in enumerate(results):
            logging.info("  Match[%d]: %s", i, r)
        logging.info("=========================================")
        return results

# Personal SVM for sdw

SDW_DND:
  autoDiscovery: false
  model: "NetApp 9 Cluster Mode"
  ipaddress: "10.250.50.58"
  cluster_ip: "10.1.10.116"
  hostname: "sdw_dnd"
  username: "vsadmin"
  password: "Komprise123"
  default_nfs_share: "/sdw_dnd_nfs"