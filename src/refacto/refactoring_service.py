from typing import Callable

from pygls.lsp.types import CodeAction
from pygls.lsp.types import CodeActionKind
from pygls.lsp.types import CodeActionParams
from pygls.lsp.types.basic_structures import Range
from pygls.lsp.types.basic_structures import TextEdit
from pygls.lsp.types.basic_structures import WorkspaceEdit
from pygls.workspace import Document

from refacto.lsp_utilities import lsp_text_edits
from refacto.refactorings.extract_variable import extract_variable


class RefactoringService:
    def __init__(self) -> None:
        self.refactoring_methods_by_title: dict[str, Callable[[Range, str], str]] = {
            "Extract Variable": extract_variable,
        }

    def get_available_refactorings(self, document: Document, code_action_params: CodeActionParams) -> list[CodeAction]:
        code_actions: list[CodeAction] = []
        for title, refactoring_method in self.refactoring_methods_by_title.items():
            code_actions.append(
                self._get_workspace_edit(
                    document=document,
                    title=title,
                    new_code=refactoring_method(code_action_params.range, document.source),
                ),
            )

        return code_actions

    def _get_workspace_edit(self, document: Document, new_code: str, title: str) -> CodeAction:
        text_edits: list[TextEdit] = lsp_text_edits(old_code=document.source, new_code=new_code)
        edit = WorkspaceEdit(changes={document.uri: text_edits}, document_changes=None, change_annotations=None)
        return CodeAction(
            title=title,
            kind=CodeActionKind.RefactorExtract,
            edit=edit,
            diagnostics=None,
            is_preferred=None,
            disabled=None,
            command=None,
            data=None,
        )
