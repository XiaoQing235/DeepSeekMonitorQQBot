TARGET_COMMANDS = {"!dss", "!deepseekstatus", "!dsss", "!deepseekserverstatus", "!deepseekservicesstatus"}
VALID_LENGTHS = {len(cmd) for cmd in TARGET_COMMANDS}

def check_command(s: str) -> bool:
    s = s.lower()
    return len(s) in VALID_LENGTHS and s in TARGET_COMMANDS
