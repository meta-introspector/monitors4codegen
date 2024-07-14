# scheme server python
# Copyright (C) 2024 by James Michael Dupont for the Meta-Introspector Project

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import logging



from monitors4codegen.multilspy.multilspy_config import MultilspyConfig
from monitors4codegen.multilspy.multilspy_logger import MultilspyLogger
from monitors4codegen.multilspy.language_servers.scheme_language_server.scheme_server import (
SchemeServer,
)

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    )

config = MultilspyConfig.from_dict({"code_language": "scheme"})
logger = MultilspyLogger()

requests_log = logging.getLogger("multilspy")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")

repository_root_path= "/time/2024/07/13/scheme-lsp-server/"
lsp =  SchemeServer(config, logger, repository_root_path)

async def foo():
#    import pdb
#    pdb.set_trace()
    async with lsp.start_server():

        document_symbols, b = await lsp.request_document_symbols("lsp-server-impl.scm")
        print(document_symbols, b)
#        for x in range(100):
#            result = await lsp.request_definition(
#                "lsp-server-impl.scm", # Filename of location where request is being made
#                x, # line number of symbol for which request is being made
#            1 # column number of symbol for which request is being made
#        )
#        print(result)

import asyncio

asyncio.run(foo())
