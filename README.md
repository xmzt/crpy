# crpy

C reader in python. Parse C code into an AST.

Currently only partially works. The lexer should be fairly complete. The parser should handle
complete declarations but needs support for expressions and preprocessing directives in
particular. Currently pure python.

## Notes

- declaration
  - declaration-specifiers,1+ init-declarator,0+,comma_sep
  - static_assert-declaration
    
- static_assert-declaration:
  - **_Static_assert** **(** ... **)**

- declaration-specifiers: 1+ of
  - storage-class-specifier **typedef**
  - storage-class-specifier **extern**
  - storage-class-specifier **static**
  - storage-class-specifier **_Thread_local**
  - storage-class-specifier **auto**
  - storage-class-specifier **register**
  - type-specifier **void**
  - type-specifier **char**
  - type-specifier **short**
  - type-specifier **int**
  - type-specifier **long**
  - type-specifier **float**
  - type-specifier **double**
  - type-specifier **signed**
  - type-specifier **unsigned**
  - type-specifier **_Bool**
  - type-specifier **_Complex**
  - type-specifier **_Atomic** **(** ... **)**
  - type-specifier **struct**|**union**|**enum** iden
  - type-specifier **struct**|**union**|**enum** iden **{** ... **}**
  - type-specifier **struct**|**union**|**enum** **{** ... **}**
  - type-specifier typedef-name
  - type-qualifier **const**
  - type-qualifier **restrict**
  - type-qualifier **volatile**
  - type-qualifier **_Atomic**
  - function-specifier **inline**
  - function-specifier **_Noreturn**
  - alignment-specifier **_Alignas** **(** ... **)**

- init-declarator:
  - declarator
  - declarator **=** initializer
    
- declarator:
  - pointer,0+ direct-declarator

- direct-declarator:
  - iden
  - **(** declarator **)**
  - direct-declarator **[** ... ****
  - direct-declarator **(** ... **)**
