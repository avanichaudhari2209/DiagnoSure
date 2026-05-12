# Fix Yellow Underline Lint Warnings in Django API Files

## Steps:
1. [x] Edit api/models.py: Remove duplicate `from django.db import models`
2. [x] Edit api/serializers.py: Replace wildcard import with explicit model imports
3. [x] Edit api/admin.py: Replace wildcard import with explicit model imports
4. [x] Update TODO.md: Mark steps complete
5. [x] Test: Run pylint on files; reload VSCode Python Language Server (`Ctrl+Shift+P` > 'Python: Restart Language Server')

**pylint results (post-fix)**: No more undefined name/no-member warnings. Remaining are minor style (docstrings, newlines, __str__ returns, slicing). Yellow underlines from wildcard imports **gone**.

6. [x] attempt_completion

Current progress: Complete.

