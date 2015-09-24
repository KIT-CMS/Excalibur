#!/bin/bash
# a script that checks source code whether deprecated things happen
if [[ "$@" == "-h" || -z "$@" ]]; then
    echo -e "Usage: ${0/*\/} google or ${0/*\/} [grep options] file\nwith typical grep options: -r -n -o -c"
    exit 0
fi
GREPOPT="-I --include *.h --include *.cc --include *.cpp --include *.hxx --exclude=easylogging++.h $@"

# use the Google linter without these filters:
# - header_guard: we use pragma once
# - include_what_you_use: we have global includes for map, string, vector
# - legal: we have no copyright notice
# - braces/newline: we use a different brace style (Linux) than google (Attach)
# - indent: we do not use a 2 spaces indent
if [[ "$@" == "google" ]]; then
    find src -name "*cc" -or -name "*h" | xargs python own/cpplint.py --linelength=100 \
    --filter=-build/header_guard,-build/include_what_you_use,-legal,-readability/braces,-runtime/int,-whitespace/braces,-whitespace/indent,-whitespace/newline
    exit 0
fi

# checks with a regex pattern and an advice
# not every occurence is a real warning, just typical cases are listed

# std::abs
grep -E "[^:]abs\s*\(" $GREPOPT && echo "-> use std::abs here"

# cast

grep -E "(double|float|int|long|short|char)\*?\s*\(" $GREPOPT | \
grep -v "std::function" | \
grep -E "(double|float|int|long|short|char)\*?\s*\(" && echo "-> use static_cast if possible"
grep -E "\(\s*(double|float|int|long|short|char)\s*\*?\s*\)" $GREPOPT && echo "-> use static_cast if possible"

# using namespace
grep -E "using namespace" $GREPOPT && echo "-> don't use using namespace"

# postfix increment
grep -E "[a-zA-Z_0-9]+\+{2}" $GREPOPT && echo "-> use prefix increment if possible (in for loop!)"

# Non-C++11 NULL
grep -E "NULL" $GREPOPT && echo "-> use nullptr instead of NULL"

# assignment in if condition
grep -E "if\s*\(.* = " $GREPOPT && echo "-> should this be ==?"

# possible place for an iterator
grep -E "for\s*\(.*(int|long|short).*size\(\)" $GREPOPT && echo "-> seems like a loop over a vector by index. Could this be replaced by iterators?"

# no pragma once (only in header)
test $(grep -L --include *.h "#pragma once" $@ | wc -l) != "0" &&
grep -L --include *.h "#pragma once" $@ && echo "-> header without pragma once"

# single semi-colons
grep -E "^\s*;\s*$" $GREPOPT && echo "-> single ; on line"

# class etc. not at outer level
grep -E "^\s+class\s+" $GREPOPT && echo "-> class is indented"
grep -E "^\s+#" $GREPOPT && echo "-> macro is indented"
#grep -E "^(  \s+| ?)(public|private|protected)" $GREPOPT && echo "-> private/public wrongly indented"

# compare to bool
grep -E "[!=]= (true|false)" $GREPOPT && echo "-> comparison to true/false can mostly be expressed more easily"

# includes of standard headers (only once)
grep -E "#include\s\<(map|string|vector)" $GREPOPT && echo "-> map, string, vector should be included globally"

# float compare
grep -E "==\s*[0-9]+\.[0-9]+f?" $GREPOPT && echo "-> Possible float comparison"
