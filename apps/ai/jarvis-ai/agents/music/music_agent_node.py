# Music Agent Node
# Handles all music-related actions (play, pause, skip, volume, queue).

from pathlib import Path
import subprocess

from agents.orchestrator.orchestrator_schemas import OrchestratorState

def music_agent_node(state: OrchestratorState) -> dict:
    """
    LangGraph node: handles music commands by delegating to the existing
    Node.js Sonos play test script.
    """
    repo_root = Path(__file__).resolve().parents[5]
    sonos_script = repo_root / "apps/server/app/api/sonos/test.js"

    if not sonos_script.exists():
        return {
            "content": f"[music] Sonos script not found: {sonos_script}",
        }

    try:
        completed = subprocess.run(
            ["node", str(sonos_script)],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except FileNotFoundError:
        return {
            "content": "[music] Node.js is not installed or not on PATH.",
        }
    except subprocess.TimeoutExpired:
        return {
            "content": "[music] Sonos play command timed out.",
        }

    output = (completed.stdout or completed.stderr or "").strip()
    if completed.returncode == 0:
        result = output or "[music] Sonos command completed."
    else:
        result = (
            f"[music] Sonos command failed (exit {completed.returncode}). "
            f"{output}"
        )

    return {
        "content": result,
    }
