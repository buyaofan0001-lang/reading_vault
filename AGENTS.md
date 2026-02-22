# Book QA to Obsidian Workflow

## Goal
Build a Codex-based flow where the user selects a book by name, Codex reads the book content from the matching folder, answers questions, and appends the Q&A to the Obsidian vault.

## Vault Location
`/Users/liuguan1/Documents/github/reading_vault`

## Book Folder Convention
- Each book has its own folder under the vault.
- Folder name equals the book title exactly.
- Example: `/Users/liuguan1/Documents/github/reading_vault/书名/`

## Source Files
- The book folder contains one or more `*.pdf` or `*.epub` files.
- If multiple files exist, prefer the most recently modified file unless the user specifies otherwise.
- If no supported file exists, ask the user to provide or place the file in the book folder.

## User Flow
- User first provides the book title.
- Agent sets this as the current book context.
- Agent loads the corresponding PDF/EPUB from the book folder.
- Agent prepares an index for answering questions (chunking + retrieval).
- User asks questions about the book.
- Agent answers using retrieved content and always provides chapter/page or section references.
- Agent appends the Q&A record into the book folder.

## Q&A Log Format
Append to a single file:
`/Users/liuguan1/Documents/github/reading_vault/<书名>/问答.md`

Use an Obsidian-friendly card format per entry:

```
## <章节名称>

> [!info] 记录时间
> `<YYYY-MM-DD HH:mm>`

> [!question] 问题
> <user question>

> [!note] 回答
> <agent answer>

> [!cite] 来源
> - 章节/页码/小节: <chapter/page or section reference>
> - 文件: `<source filename>`
```

If this entry is a follow-up question, add this block between `记录时间` and `问题`:

```
> [!abstract] 追问关系
> 追问 `<上一个相关问题的时间戳>`：<本次追问与上个问题的关系>
```

Styling rules:
- Use chapter name as the H2 title, not timestamp.
- Keep timestamp in the `记录时间` callout.
- Separate entries with `---`.

## Behavior Rules
- Keep the current book context until the user changes it.
- If the question does not match the current book, ask whether to switch books.
- If the answer cannot be supported by the book text, say so explicitly.
- Do not fetch web sources unless the user explicitly requests it.
- For follow-up questions, explicitly record the relation to the referenced prior question in `问答.md`.

## Edge Cases
- If the book folder name is ambiguous, ask the user to confirm the exact folder.
- If the file is large, build the index incrementally and cache results per book.
- If the vault path changes, prompt the user to update it before proceeding.
