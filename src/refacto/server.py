from pygls.lsp.methods import CODE_ACTION
from pygls.lsp.types import CodeAction
from pygls.lsp.types import CodeActionKind
from pygls.lsp.types import CodeActionOptions
from pygls.lsp.types import CodeActionParams
from pygls.server import LanguageServer

from refacto.refactoring_service import RefactoringService


class RefactoLanguageServer(LanguageServer):
    def __init__(self) -> None:
        super().__init__()
        self.service = RefactoringService()


refacto_server = RefactoLanguageServer()


@refacto_server.feature(
    CODE_ACTION,
    CodeActionOptions(
        code_action_kinds=[CodeActionKind.RefactorExtract],
        work_done_progress=None,
        resolve_provider=True,
    ),
)
def code_action(server: RefactoLanguageServer, code_action_params: CodeActionParams) -> list[CodeAction]:
    document = server.workspace.get_document(code_action_params.text_document.uri)
    return server.service.get_available_refactorings(document=document, code_action_params=code_action_params)
