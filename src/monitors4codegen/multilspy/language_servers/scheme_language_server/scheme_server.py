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

from contextlib import asynccontextmanager
from typing import AsyncIterator
import logging
from monitors4codegen.multilspy.language_server import LanguageServer
from monitors4codegen.multilspy.multilspy_logger import MultilspyLogger
from monitors4codegen.multilspy.lsp_protocol_handler.server import ProcessLaunchInfo
from monitors4codegen.multilspy.multilspy_config import MultilspyConfig
from monitors4codegen.multilspy.lsp_protocol_handler.lsp_types import InitializeParams
import os
import json
import pathlib
class SchemeServer(LanguageServer):
    def __init__(self, config: MultilspyConfig, logger: MultilspyLogger, repository_root_path: str):
        super().__init__(
            config,
            logger,
            repository_root_path,
            ProcessLaunchInfo(cmd="guile-lsp-server", cwd=repository_root_path),
            "scheme",
        )
    def _get_initialize_params(self, repository_absolute_path: str) -> InitializeParams:
        """
        Returns the initialize params for the Jedi Language Server.
        """
        with open(os.path.join(os.path.dirname(__file__), "initialize_params.json"), "r") as f:
            d = json.load(f)

        del d["_description"]

        d["processId"] = os.getpid()
        assert d["rootPath"] == "$rootPath"
        d["rootPath"] = repository_absolute_path

        assert d["rootUri"] == "$rootUri"
        d["rootUri"] = pathlib.Path(repository_absolute_path).as_uri()

        assert d["workspaceFolders"][0]["uri"] == "$uri"
        d["workspaceFolders"][0]["uri"] = pathlib.Path(repository_absolute_path).as_uri()

        assert d["workspaceFolders"][0]["name"] == "$name"
        d["workspaceFolders"][0]["name"] = os.path.basename(repository_absolute_path)

        return d

    @asynccontextmanager
    async def start_server(self) -> AsyncIterator["SchemeServero"]:
        """
         Usage:
        ```
        async with lsp.start_server():
            # LanguageServer has been initialized and ready to serve requests
            await lsp.request_definition(...)
            await lsp.request_references(...)
            # Shutdown the LanguageServer on exit from scope
        # LanguageServer has been shutdown
        ```
        """

        async def execute_client_command_handler(params):
            return []

        async def do_nothing(params):
            return

        async def check_experimental_status(params):
            if params["quiescent"] == True:
                self.completions_available.set()

        async def window_log_message(msg):
            self.logger.log(f"LSP: window/logMessage: {msg}", logging.INFO)

#        self.server.on_request("client/registerCapability", do_nothing)
#        self.server.on_notification("language/status", do_nothing)
        self.server.on_notification("window/logMessage", window_log_message)
        self.server.on_request("workspace/executeClientCommand", execute_client_command_handler)
#        self.server.on_notification("$/progress", do_nothing)
#        self.server.on_notification("textDocument/publishDiagnostics", do_nothing)
#        self.server.on_notification("language/actionableNotification", do_nothing)
#        self.server.on_notification("experimental/serverStatus", check_experimental_status)

        async with super().start_server():
            self.logger.log("Starting scheme server process", logging.INFO)
            await self.server.start()
            initialize_params = self._get_initialize_params(self.repository_root_path)

            self.logger.log(
                "Sending initialize request from LSP client to LSP server and awaiting response",
                logging.INFO,
            )
            init_response = await self.server.send.initialize(initialize_params)
            print(dict(init_response=init_response))
            #assert init_response["capabilities"]["textDocumentSync"]["change"] == 2
            #assert "completionProvider" in init_response["capabilities"]
            #assert init_response["capabilities"]["completionProvider"] == {
            #    "triggerCharacters": [".", "'", '"'],
            #    "resolveProvider": True,
            #}

            self.server.notify.initialized({})

            yield self

            await self.server.shutdown()
            await self.server.stop()
#{'init_response': {'capabilities': {'textDocumentSync': {'save': True, 'openClose': True, 'change': 2}, 'hoverProvider': True, 'completionProvider': {'resolveProvider': True}, 'signatureHelpProvider': {}, 'definitionProvider': {}, 'diagnosticsProvider': {'interFileDiagnostics': True, 'workspaceDiagnostics': True}}, 'serverInfo': {'name': 'Guile LSP server', 'version': '0.4.4'}}}
