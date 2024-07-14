# Changes made,
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
"""
Multilspy logger module.
"""
import inspect
import logging
from datetime import datetime
from pydantic import BaseModel

class LogLine(BaseModel):
    """
    Represents a line in the Multilspy log
    """

    time: str
    level: str
    caller_file: str
    caller_name: str
    caller_line: int
    message: str

class MultilspyLogger:
    """
    Logger class
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger("multilspy")
        self.logger.setLevel(logging.DEBUG)

    def log(self, debug_message: str, level: int, sanitized_error_message: str = "") -> None:
        """
        Log the debug and santized messages using the logger
        """

        debug_message = debug_message.replace("'", '"').replace("\n", " ")
        sanitized_error_message = sanitized_error_message.replace("'", '"').replace("\n", " ")

        # Collect details about the callee
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        caller_file = calframe[1][1].split("/")[-1]
        caller_line = calframe[1][2]
        caller_name = calframe[1][3]

        # Construct the debug log line
        debug_log_line = LogLine(
            time=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            level=logging.getLevelName(level),
            caller_file=caller_file,
            caller_name=caller_name,
            caller_line=caller_line,
            message=debug_message,
        )
        #print("DEBUG",debug_log_line.json())
        self.logger.log(
            level=level,
            msg=debug_log_line.json(),
        )
