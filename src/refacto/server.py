from lsprotocol.types import CodeAction
from lsprotocol.types import CodeActionKind
from lsprotocol.types import CodeActionOptions
from lsprotocol.types import CodeActionParams
from lsprotocol.types import TEXT_DOCUMENT_CODE_ACTION
from pygls.server import LanguageServer

from refacto.refactoring_service import RefactoringService


class RefactoLanguageServer(LanguageServer):
    def __init__(self) -> None:
        super().__init__("Refacto", "1.0.0")
        self.service = RefactoringService()


refacto_server = RefactoLanguageServer()


@refacto_server.feature(
    TEXT_DOCUMENT_CODE_ACTION,
    CodeActionOptions(
        code_action_kinds=[CodeActionKind.Refactor],
        work_done_progress=None,
        resolve_provider=True,
    ),
)
def code_action(server: RefactoLanguageServer, code_action_params: CodeActionParams) -> list[CodeAction]:
    document = server.workspace.get_document(code_action_params.text_document.uri)
    return server.service.get_available_refactorings(document=document, code_action_params=code_action_params)
