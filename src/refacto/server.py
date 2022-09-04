from devtools import debug
from pygls.lsp.methods import CODE_ACTION
from pygls.lsp.types import CodeAction
from pygls.lsp.types import CodeActionKind
from pygls.lsp.types import CodeActionOptions
from pygls.lsp.types import CodeActionParams
from pygls.lsp.types.basic_structures import Range
from pygls.server import LanguageServer

refacto_server = LanguageServer()


@refacto_server.feature(
    CODE_ACTION,
    CodeActionOptions(
        code_action_kinds=[CodeActionKind.RefactorExtract],
        work_done_progress=None,
        resolve_provider=True,
    ),
)
def extract_variable(server: LanguageServer, code_action_params: CodeActionParams) -> list[CodeAction]:
    server.show_message_log(message="Refacto: Code Action")
    document = server.workspace.get_document(code_action_params.text_document.uri)
    doc_path = document.uri.replace(r"file://", "")
    with open(file=doc_path, mode="r") as code:
        s = code.readlines()
    debug(get_chars_in_range(range=code_action_params.range, code=s))
    code_actions = []
    test = CodeAction(
        title="Testing",
        kind=CodeActionKind.RefactorExtract,
        edit=None,
        diagnostics=None,
        is_preferred=None,
        disabled=None,
        command=None,
        data=None,
    )
    code_actions.append(test)
    return code_actions


def get_chars_in_range(range: Range, code: list[str]) -> str:
    start = range.start
    end = range.end
    if start == end:
        return ""
    b = code[start.line : end.line + 1]
    if start.line == end.line:
        return "".join(b)[start.character : end.character]

    return ""
