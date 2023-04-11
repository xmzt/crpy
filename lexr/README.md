# Lexr

Code generator for lexical analysis (parsing bytes / characters into tokens a la lex/flex).

- Output code is generated from a state machine graph that is generated from a grammar.

- Output code in Python only currently. C code output imminent. Moving beyond proof-of-concept,
  output of optimized machine-level code might be the next step.

- Optimizations to reduce redundancy, minimize output code size and variable usage.

- Grammar is formed from a combo of Python code and an application-specific interpreter using a
  lispish parenthesized prefix notation.

Primary goals

- Maximum efficiency / performance of output code.

- Viewing a grammar should bring to mind phrases like "compact" "succinct" and "minimally
  redundant". Current reference grammar to fully parse C language tokens (clexgen.py) is about
  150 lines of meat plus 30 lines of Python boilerplate.
  
- Graph is indepdendent of output language. Graph retains and deduces enough information for
  optimization at graph level (e.g. reduce redundant code paths, remove no-op nodes) down to
  machine-code level (e.g. take advantage of potential CPU instructions for testing input
  against multiple values at once, for table lookups, for indirect goto/call).

- The dream is a system in which ast-level parsers for most any programming language can be
  generated consistently and compactly, to enable powerful pre-processors, integrated
  mixed-language support at the ast level, and something resembling the ability to decouple the
  front-end syntax of a language (all of them lame) from the actual language features provided
  (not lame). Not unlike dreams of gcc (at one time at least) and llvm.
  
## Usage

Reference parser for C tokens:
```
python clexmake.py clex_gen.py
python clextest.py t0 t1 t2 t3 t4 t5
```

## Grammar format

### Top-level grammar

The grammar is just Python code at the top-level (see clexmake.py). Header boilerplate code sets
up diagnostics for debugging, the initial graph is formed, the graph is compiled.

One could generate the graph in straight Python generating objects from funlib objlib nodelib,
but the code becomes annoyingly redundant and punctation-heavy, hence the lispish interpreter
(machlib.Mach.parse) to aid in generating the graph. The lispish syntax seems to provide for a
textually compact grammar that follows the state machine closely, at least to the eyes of the
author.

### machlib.Mach.parse grammar

- Input is broken into lines. Backslash-eol sequences may be used as in C to continue a logical
  line across multiple physical lines.

- Each line represents a 'chain' of objects. The objects in a chain are evaluated left to
  right. An object may:

  - Create a new node in the graph representing a run-time conditional or operation.

  - Create or follow a transititon from the previous object to this one, representing a branch
    to take based on run-time input.

  - Perform a compile time operation e.g. set a variable or obtain information on current state
    of graph, to affect subsequent processing.

  - Cause multiple subchains to be evaluated e.g. the same end-of-line operation is to be taken
    based on input of \n \r or \r\n.

### Compile-time and run-time environment

After an initial graph is formed, machlib.Mach.compilFromGram will post-process the grammar, optimize,
and generate output code.

The implicit run-time environment exposed to the grammar includes:

- src: pointer to current input.
- *src: the character value at 'src', specifically the value tested by the preceding conditional at node.off-1.

Each node has a compile-time property 'off' representing an offset from 'src' that this node is
processing. For the most part 'node.off' is automatically deduced, but the grammar must
explicitly update the 'src' pointer, e.g the grammar expression '(src+)' results in run-time
operation of 'src += node.off'. This enables run-time parsers that do not need to implicitly
update 'src' after every single byte of input, for better performance and to utilize a wider
range of evunderlying operations to test input in the run-time environment.

Transistions also have an 'off' property that is either 0 or 1 representing whether to increment
off in the 'to' node i.e. whether to consume the input or not. By default a transition
specifying an input character has off=1, and off=0 otherwise, but this can be modified.

Top-level graph node types:

- NodeCond: read value of src[node.off]. Dispatch-style branch based on value, else follow 'to' pointer.
- NodeIf: Evaluates an expression. Branch if true else follow 'to' pointer.
- NodeTo: Execute a run-time operation. No branching, always follow 'to' pointer.
- NodeTerm: Stop parsing, only type of node with no 'to' pointer.

Some nodes are used only during compilation and are removed before output code generation.

### Objects

int, float, single and double quoted strings are same as in Python.

**[...]**

Character set object created with similar syntax to a [] regular expression.

**\!** 

Previous transition off=0 e.g. to peek at the input but not consume it.

**\*** 

Previous transition off=1 e.g. to consume src when following the 'to' pointer of a NodeCond
when no other input matches.

**\?**

Stop processing chain if transisition has already been set (normally this would error).

**src**

Pointer to current input

**\*src**

Character value of 'src' tested by previous NodeCond 'cond' where 'cond.off == node.off-1'.

**(\@ arg arg...)**

Like Python 'exec'. The arguments following \@ are evaulated compile-time, the result is
ignored, no node is generated, chain processing continues.

**(= dst ... src)**

Evaluate right-most argument as src. Assign src to each subsequent dst argument, from right to
left, result src. This results in run-time operation if any operand is run-time, else it is
evaluated compile-time. 

**(BINOP a b ...)**

BINOP is one of `+ - * / | & ^ << >> < <= == != >= >`. Perform binary operation(s) and return
result. `(+ a b c d)` is equivalent to `(+ (+ (+ a b) c) d)`. Same compile-time / run-time
semantics as `=`.

**(BINOP_EQU a b ...)**

BINOP_EQU is one of `+= -= *= /= |= &= ^= <<= >>=`. Perform augmented assignment operation(s)
and return a. `(+= a b c d)` is equivalent to `(+= a b) (+= a c) (+= a d)`. Same compile-time /
run-time semantics as `=`.

**(list ...)**

Create a Python data list of subsequent arguments.

**(for dst srcV)**

For each element of srcV, set dst to element, and process subchain of dst with remainder of line.

**(insert)**

Subchain remainder of line, but do not create transisiton to prev now. Postpone this operation
until post-processing grammar.

**(if expr then ...)**

Create a NodeIf. At run-time expr is evaluated, and if true, branches to the 'then ...' subchain.

**(line+)**

Records position of 'src + node.off' in list of line offsets for line.column diagnostics.

**(off=)**

Sets 'node.off' for previous node. The entry point into the parser is normally set to 0.

**(off-)**

A NodeTo is added to the graph that causes the following node.off to be decremented from the
current node.off. Used in backtracking. 

**(sameTo node0)**

Set 'to' pointer of prev node to 'to' pointer of node0. Used in backtracking.

**(src<- sym)**

Set 'src' pointer to run-time variable sym. All preceding execution paths are searched for
assignments to sym from 'src', and node.off is set to off of the node with the preceding
assignments, if they are consistent. Used in backtracking.

**(src+)**

Increment 'src' by node.off. Subsequent node.off = 0. Consumes input processed so far.

**(src+ arg)**

Increment 'src' by arg. Subsequent node.off is reduced by arg. Consumes partial input.

**(src+from node0)**

Equivalent to '(src+ arg)' with arg = node.off - node0.off.

**(term)**

Boom! Parsing is complete.

## Example grammar (todo update this)

An example few lines of clexmake.py: 
```
START        (off= 0) (= tokWs Ws._0) WS
WS [ \t\v\f] (|= tokWs Ws.H) (src+) WS
WS *         (= tokSrc src) OTHER (acc *src) (= accTyp AccTyp._0) (= tokTyp TokTyp.Other) (tokAddAcc) (src+) START
```

Line 1: from START state, set tokWs to 0 and goto WS. Input not used. The (off= 0) sets the
        'offset' of START. The compile-time offset is added to src pointer to determine the
        input element to test.
	
Line 2: from WS, with input of any of these 4 whitespace chars, update tokWs, increment src
        pointer, go to WS.

Line 3: from WS, for any other input, set tokSrc, go to OTHER (auto-created upon first
        reference), from OTHER accumulate current input into token string, set type of token
        string, set token type, add token, increment src pointer, go to START.

For the C language, things are more or less straightforward until the end with lines like this:
```
WS (- (WS.to.chset) wsAll) (insert) (= tokSrc src)
(@ = condV (mach.condNemptyV))
(for node0 condV) bs (for eol eolV) (src+from node0) (line+) node0
(for node0 condV) bs ? (off- 1) (sameTo node0)
```

Line 1: generate a character set consisting of all characters in WS so far excluding those in
        wsAll (all whitespace). for each of these (non-whitespace) characters, insert an action
        in graph to copy current input pointer to tokSrc, representing the start of the token.

Line 2: compile-time set condV to the list of all NodeConds so far that are not empty.

Line 3: for each node in condV, add bs-eol sequences that increment src pointer by the length of
        input processed since that node (e.g. bs-nl increments src by 2, bs-cr-nl increments src
        by 3), record the position of the new line (for line.column diagnostics), and go back to
        that node.

Line 4: for each node in condV, if the grammar has not specified a default action to take upon a
        bs (i.e. not followed by the eol of previous line), then set it to the same default
        action of that node.

This generates a run-time lexr that processes bs-eol sequences at every character of input as if
it were a previous stage of processing, as described in the C spec section 'Translation Phases
5.1.1.2'. Implementing an actual previous stage of processing would be easy and straightforward,
but is inefficient, as these sequences are relatively rare in real code, and this previous stage
would get little work done relative to updating loop counters.

## Todo

Output C code, or even machine-level code to potentially take advantage of new CPU instructions
that may aid in lookup tables. A byte-by-byte parser is pretty much operating at machine-level
anyway.

Currently optimized to generate smallest output code - add functionality to generate faster
code by selectively duplicating some code paths to reduce number of branches.

Another way to maybe eek out 1% or so of performance is to analyze huge amounts of existing
code, and from each state, keep track of how often each transition occurs for each input. If
code for that state tests the input sequentially against various values, as in a sequence of if
and elseif statements, reorder the tests so that the most frequent branches are tested for
first. Or, potentially one could generate a custom parser for code that gets repeatedly
processed (e.g. a project being actively developed).

Parse trigraphs in C for completeness bragging rights even though they are an extinct feature.

## Opinion section

My instinct is to utilize functionality of the Python interpreter directly, rather than write
more code implementing a custom interpreter, but I found the resulting grammars in straight
Python overly verbose and cluttered with punctuation. Memories of perl.

One idea was to use Python's ast parser for expressions and translate that into different output
targets, rather than write my own parser / ast. However, the node graph system would still be
outside this and I would need to deal with Python discouraging multiple statements per line, or
suffer a grammar that is 600 lines long and 18 columns wide. Both of these issues would require
significant amounts of ugly, clunky code.

The lispish interpreter is easy to implement, and seems a good fit for this application, as
these state machine grammars tend to lack the deep nesting that can result in annoying monotone
parentheses soup.

Just to elaborate on the FACT that all language syntaxes are lame, they are lame when applied
generally. Some are not so lame in specific sitations. What I dream of here is that the lexical
syntax processing is completely handled by the editor, which operates on and stores user code in
a structure much closer to an ast than a text file, and the editor takes care of passing the ast
to the compiler, or even better, has deeper integration with the compiler. The editor
understands multiple syntaxes and can switch between them at user request. It becomes a bit less
text editor and a bit more GUI-based CAD software now that code is objects and we've evolved
beyond developing on 80x25 text terminals.

## Files

- clexmake.py: specific parser generator for C code
- clex_gen.py: generated code for C parser
- clex.py: C parser top-level
- clextest.py: test suite for clex.py (todo check output against known values)

- machlib: main 'machine' structure to manage generating the parser
- objlib: base objects / ast elements used to parse and process grammar
- funlib.py: objects / ast elements for basic functions (e.g. arithmetic)
- actlib.py: objects / ast elements for compile-time actions
- nodelib.py: nodes and transisitions for state machine graph
- codepylib.py: Python output code generation
- scanlib.py: lexical scanner for lispy expressions
- logclib.py: diagnostic logging helpers for debugging
- util.py: helper functions, stateless stuff
- cbase.py: enums and such for C language that may be used by both grammar and generated Python output code
- chtab.py: character lookup tables and character sets 
- other.py: scrapyard of abandoned code that I want to keep around
