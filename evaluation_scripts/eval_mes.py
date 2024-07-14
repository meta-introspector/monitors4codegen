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

from monitors4codegen.multilspy import SyncLanguageServer
from monitors4codegen.multilspy.multilspy_config import MultilspyConfig
from monitors4codegen.multilspy.multilspy_logger import MultilspyLogger
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    )

config = MultilspyConfig.from_dict({"code_language": "scheme"}) # Also supports "python", "rust", "csharp"
logger = MultilspyLogger()
lsp = SyncLanguageServer.create(config, logger, "/time/2024/07/13/scheme-lsp-server/")
with lsp.start_server():
    result = lsp.request_definition(
        "lsp-server-impl.scm", # Filename of location where request is being made
        1, # line number of symbol for which request is being made
        1 # column number of symbol for which request is being made
    )
    print(result)
