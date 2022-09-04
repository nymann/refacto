from devtools import debug
from pygls.lsp.methods import CODE_ACTION
from pygls.lsp.types import CodeAction
from pygls.lsp.types import CodeActionKind
from pygls.lsp.types import CodeActionOptions
from pygls.lsp.types import CodeActionParams
from pygls.lsp.types import List
from pygls.lsp.types import Optional
from pygls.lsp.types import Union
from pygls.lsp.types.basic_structures import RenameFile
from pygls.lsp.types.basic_structures import TextEdit
from pygls.lsp.types.basic_structures import WorkspaceEdit
from pygls.server import LanguageServer

from refacto.refactorings.extract_variable import extract_variable
from refacto.refactorings.extract_variable import lsp_text_edits

refacto_server = LanguageServer()


@refacto_server.feature(
    CODE_ACTION,
    CodeActionOptions(
        code_action_kinds=[CodeActionKind.RefactorExtract],
        work_done_progress=None,
        resolve_provider=True,
    ),
)
def code_action(server: LanguageServer, code_action_params: CodeActionParams) -> list[CodeAction]:
    server.show_message_log(message="Refacto: Code Action")
    document = server.workspace.get_document(code_action_params.text_document.uri)
    doc_path = document.uri.replace(r"file://", "")
    with open(file=doc_path, mode="r") as source_file:
        source = source_file.read()
    new_code = extract_variable(range=code_action_params.range, source=source)
    text_edits: list[TextEdit] = lsp_text_edits(old_code=source, new_code=new_code)
    debug(text_edits)
    edit = WorkspaceEdit(changes={document.uri: text_edits}, document_changes=None, change_annotations=None)
    test = CodeAction(
        title="Extract Variable",
        kind=CodeActionKind.RefactorExtract,
        edit=edit,
        diagnostics=None,
        is_preferred=None,
        disabled=None,
        command=None,
        data=None,
    )
    return [test]
