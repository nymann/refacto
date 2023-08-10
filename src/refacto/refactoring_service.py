from lsprotocol.types import CodeAction
from lsprotocol.types import CodeActionKind
from lsprotocol.types import CodeActionParams
from lsprotocol.types import TextEdit
from lsprotocol.types import WorkspaceEdit
from pygls.workspace import Document

from refacto.lsp_utilities import lsp_text_edits
from refacto.refactorings.extract_variable.refactor import RefactorExtractVariable
from refacto.refactorings.inline_variable.refactor import RefactorInlineVariable
from refacto.refactorings.refactor import Refactor


class RefactoringService:
    def __init__(self) -> None:
        self.refactoring_methods_by_title: dict[str, Refactor] = {
            "Extract Variable": RefactorExtractVariable(),
            "Inline Variable": RefactorInlineVariable(),
        }

    def get_available_refactorings(self, document: Document, code_action_params: CodeActionParams) -> list[CodeAction]:
        code_actions: list[CodeAction] = []
        for title, klass in self.refactoring_methods_by_title.items():
            try:
                new_code = klass.refactor(code_action_params.range, document.source)
            except RuntimeError:
                continue
            if new_code == document.source:
                continue
            code_actions.append(
                self._get_workspace_edit(
                    document=document,
                    title=title,
                    new_code=new_code,
                ),
            )

        return code_actions

    def _get_workspace_edit(self, document: Document, new_code: str, title: str) -> CodeAction:
        text_edits: list[TextEdit] = lsp_text_edits(old_code=document.source, new_code=new_code)
        edit = WorkspaceEdit(changes={document.uri: text_edits}, document_changes=None, change_annotations=None)
        return CodeAction(
            title=title,
            kind=CodeActionKind.Refactor,
            edit=edit,
            diagnostics=None,
            is_preferred=None,
            disabled=None,
            command=None,
            data=None,
        )
