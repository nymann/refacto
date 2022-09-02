from typing import Optional

from pygls.lsp.methods import CODE_ACTION
from pygls.lsp.methods import COMPLETION
from pygls.lsp.types import CodeAction
from pygls.lsp.types import CodeActionKind
from pygls.lsp.types import CodeActionOptions
from pygls.lsp.types import CodeActionParams
from pygls.lsp.types import CompletionItem
from pygls.lsp.types import CompletionList
from pygls.lsp.types import CompletionOptions
from pygls.lsp.types import CompletionParams
from pygls.lsp.types import InsertTextMode
from pygls.server import LanguageServer

refacto_server = LanguageServer()


@refacto_server.feature(
    COMPLETION,
    CompletionOptions(
        trigger_characters=[","],
        work_done_progress=None,
        all_commit_characters=None,
        resolve_provider=None,
    ),
)
def completions(server: LanguageServer, completion_params: CompletionParams) -> CompletionList:
    server.show_message_log(message="Refacto: Completion")
    return CompletionList(
        is_incomplete=False,
        items=[
            CompletionItem(
                additional_text_edits=None,
                insert_text_mode=InsertTextMode(1),
                commit_characters=None,
                data=None,
                command=None,
                text_edit=None,
                insert_text_format=None,
                insert_text=None,
                sort_text=None,
                filter_text=None,
                label="Item 1",
                kind=None,
                documentation=None,
                deprecated=False,
                preselect=True,
                tags=None,
                detail=None,
            ),
        ],
    )


@refacto_server.feature(
    CODE_ACTION,
    CodeActionOptions(
        code_action_kinds=[CodeActionKind.Refactor],
        work_done_progress=None,
        resolve_provider=True,
    ),
)
def code_action(server: LanguageServer, code_action_params: CodeActionParams) -> Optional[list[CodeAction]]:
    server.show_message_log(message="Refacto: Code Action")
    document = server.workspace.get_document(code_action_params.text_document.uri)
    server.show_message(document)
    code_actions = []
    test = CodeAction(
        title="Testing",
        kind=CodeActionKind.RefactorInline,
        edit=None,
        diagnostics=None,
        is_preferred=None,
        disabled=None,
        command=None,
        data=None,
    )
    code_actions.append(test)
    return code_actions
