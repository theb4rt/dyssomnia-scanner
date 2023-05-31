import subprocess
import asyncio

from ms.helpers.schema_validator import is_valid
from ms.services.service import BaseService
from ..repositories.nikto_repository import NiktoRepository
from ..schema import NiktoSchema
from ...helpers.response import response_ok, response_error


class NiktoService(BaseService):
    def __init__(self, data=None):
        self.nikto_repo = NiktoRepository()
        self.target_url = None
        self.timeout = 3
        self.extra_options = None
        self.data = None

    async def run_nikto(self):
        cmd = ['nikto', '-h', self.target_url, '-Tuning', '-x6', '-timeout', str(self.timeout)]

        process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE,
                                                       stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            print(f"Nikto exited with an error code: {process.returncode}")
            print(f"Error message: {stderr.decode()}")
            return None
        return stdout.decode()

    def req_nikto(self):
        status, result = self._is_valid_data

        if not status:
            return response_error(data=result, code=400)
        self.target_url = self.data['host']
        result = asyncio.run(self.run_nikto())
        return response_ok(message="Nikto Running", code=200)

    @property
    def _is_valid_data(self) -> tuple:
        if self.data is None:
            return False, {"error": "Invalid Json"}

        schema = NiktoSchema()
        return is_valid(schema, self.data)

