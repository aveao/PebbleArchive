import os
import httpx
import logging
import shutil
from typing import Any
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UA_SUFFIX = os.environ.get("PEBBLE_SCRAPER_UA_SUFFIX", "")
if not UA_SUFFIX:
    UA_SUFFIX = input("Please input your email for use in user agent: ")

USER_AGENT = "firmware scraping for archival {UA_SUFFIX}"

HARDWARE_MAP = {
    "v1_5": Path("OG/Pebble/"),
    "v2_0": Path("OG/PebbleSteel/"),
    "snowy_dvt": Path("Time/Time/"),
    "snowy_s3": Path("Time/TimeSteel/"),
    "spalding": Path("Time/TimeRound/"),
    "silk": Path("Two/"),
}

FALLBACK_DIR = Path("Extra/")

client = httpx.Client(headers={"User-Agent": USER_AGENT})


def get_cohorts_json() -> dict[str, Any]:
    response = client.get(
        "https://github.com/pebble-dev/rebble-cohorts/raw/refs/heads/master/config.json",
        follow_redirects=True,
    )
    response.raise_for_status()
    return response.json()


def download_file(url: str, output_path: Path) -> None:
    logger.info("Downloading %s to %s", url, output_path)
    with client.stream("GET", url) as r:
        with open(output_path, "wb") as f:
            for data in r.iter_bytes():
                f.write(data)


def main() -> None:
    cohorts_json = get_cohorts_json()
    for hardware, overall_release_data in cohorts_json["hardware"].items():
        for version_type, release_data in overall_release_data.items():
            url = f"https://binaries.rebble.io/fw/{hardware}/Pebble-{release_data['version']}-{hardware}.pbz"
            filename = (
                f"Pebble-{release_data['version']}-{hardware}.pbz"
                if version_type == "normal"
                else f"recovery_{release_data['version']}_{hardware}.pbz"
            )
            fallback_dir_path = FALLBACK_DIR / hardware / "rebble"
            fallback_dir_path.mkdir(parents=True, exist_ok=True)
            local_paths = [fallback_dir_path / filename]
            if hardware in HARDWARE_MAP:
                local_paths.append(HARDWARE_MAP[hardware] / filename)
            if local_paths[0].exists():
                logger.info("Skipping download of %s as we already have it.", filename)
            else:
                download_file(url, local_paths[0])

            for other_path in local_paths[1:]:
                shutil.copyfile(local_paths[0], other_path)


if __name__ == "__main__":
    main()
