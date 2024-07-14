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
Configuration parameters for Multilspy.
"""

from enum import Enum
from dataclasses import dataclass

class Language(str, Enum):
    """
    Possible languages with Multilspy.
    """

    CSHARP = "csharp"
    PYTHON = "python"
    SCHEME = "scheme"
    RUST = "rust"
    JAVA = "java"

    def __str__(self) -> str:
        return self.value

@dataclass
class MultilspyConfig:
    """
    Configuration parameters
    """
    code_language: Language
#    trace_lsp_communication: bool = True
    trace_lsp_communication: bool = False

    @classmethod
    def from_dict(cls, env: dict):
        """
        Create a MultilspyConfig instance from a dictionary
        """
        import inspect
        return cls(**{
            k: v for k, v in env.items() 
            if k in inspect.signature(cls).parameters
        })
