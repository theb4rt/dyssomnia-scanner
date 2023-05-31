import json
import subprocess
import asyncio
from typing import Optional, Tuple, Union, Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

from ms.helpers.schema_validator import is_valid
from ms.services.service import BaseService
from ..repositories.nikto_repository import NiktoRepository
from ..schema import NiktoSchema
from ...utils import nikto_logger


class NiktoService(BaseService):
    def __init__(self, data: dict = None):
        super().__init__()
        self.nikto_repo = NiktoRepository()
        self.target_url: str = ''
        self.timeout: int = 3
        self.extra_options: Any = None
        self.data: dict = data
        self._nikto_logger = nikto_logger

    async def run_nikto(self) -> Optional[str]:
        cmd = ['nikto', '-h', self.target_url, '-Tuning', '-x6', '-timeout', str(self.timeout)]

        process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE,
                                                       stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            print(f"Nikto exited with an error code: {process.returncode}")
            print(f"Error message: {stderr.decode()}")
            return None
        return stdout.decode()

    def req_nikto(self) -> dict:
        status, result = self._is_valid_data

        if not status:
            return self.response_error(data=result, code=400)
        self.target_url = self.data['host']
        result = asyncio.run(self.run_nikto())
        return self.response_ok(message="Nikto Running", code=200)

    @property
    def _is_valid_data(self) -> Tuple[bool, Union[str, dict]]:
        if self.data is None:
            return False, {"error": "Invalid Json"}
        schema = NiktoSchema()
        return is_valid(schema, self.data)

    def process_data(self):
        status, result = self._is_valid_data
        if not status:
            return self.response_error(data=result, code=400)
        self._info_logger.info(f"Processing data for {self.data['host']}")

        scan_details = result['niktoscan']['scandetails']
        niktoscan_general = result['niktoscan']['dollar']
        statistics = scan_details[0]['statistics'][0]

        scan_items_found = statistics['$']['itemsfound']
        end_time = statistics['$']['endtime']
        target_banner = scan_details[0]['dollar']['targetbanner']
        time_elapsed = statistics['$']["elapsed"]
        ip_address = scan_details[0]['dollar']["targetip"]
        target_url = scan_details[0]['dollar']["targethostname"]
        scan_date = scan_details[0]['dollar']["starttime"]
        scan_items_json = scan_details[0]['item']

        final_data = {
            "target_url": target_url,
            "ip_address": ip_address,
            "server_banner": target_banner,
            #"end_time": end_time,
            "scan_duration": time_elapsed,
            #"scan_date": scan_date,
            "items": scan_items_json,
            "scan_items_found": scan_items_found,
            "scan_full_report": result,

        }

        try:

            self.nikto_repo.add(final_data)

            return self.response_ok(data=final_data, code=200)
        except IntegrityError as e:
            self._error_logger.error(f"Error saving data: {e}")
            return self.response_error(message="Please contact an administrator")
        except FlushError as e:
            self._error_logger.error(f"Error saving data: {e}")
            return self.response_error(message="Please contact an administrator")

