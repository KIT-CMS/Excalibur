#!/bin/bash

# first do several checks - formatting below

# clang-format exists in version 3.6?
echo "Looking for clang-format"
which clang-format &&
clang-format -version ||
(echo "No clang-format installed!"; exit 1)

VERSION=$(clang-format -version)

if [ "$VERSION" != "clang-format version 3.6.0 " ]; then
  echo "This is not version 3.6: $VERSION"
  echo "Please use clang-format 3.6 from CMSSW_7_4_5_ROOT5!"
  exit 1
fi

# style file exists?
if [ ! -f "$EXCALIBURPATH/.clang-format" ]; then
  echo "There is no .clang-format file in $EXCALIBURPATH."
  exit 1
fi

# style is unchanged?
read -r -d '' VARIABLE << EOM
---
Language:        Cpp
AccessModifierOffset: -2
AlignEscapedNewlinesLeft: true
AlignTrailingComments: true
AllowAllParametersOfDeclarationOnNextLine: false
AllowShortBlocksOnASingleLine: false
AllowShortCaseLabelsOnASingleLine: false
AllowShortIfStatementsOnASingleLine: false
AllowShortLoopsOnASingleLine: false
AllowShortFunctionsOnASingleLine: All
AlwaysBreakAfterDefinitionReturnType: false
AlwaysBreakTemplateDeclarations: true
AlwaysBreakBeforeMultilineStrings: true
BreakBeforeBinaryOperators: None
BreakBeforeTernaryOperators: true
BreakConstructorInitializersBeforeComma: false
BinPackParameters: false
BinPackArguments: true
ColumnLimit:     100
ConstructorInitializerAllOnOneLineOrOnePerLine: true
ConstructorInitializerIndentWidth: 4
DerivePointerAlignment: false
ExperimentalAutoDetectBinPacking: false
IndentCaseLabels: true
IndentWrappedFunctionNames: false
IndentFunctionDeclarationAfterType: false
MaxEmptyLinesToKeep: 1
KeepEmptyLinesAtTheStartOfBlocks: false
NamespaceIndentation: None
ObjCBlockIndentWidth: 2
ObjCSpaceAfterProperty: false
ObjCSpaceBeforeProtocolList: false
PenaltyBreakBeforeFirstCallParameter: 1
PenaltyBreakComment: 300
PenaltyBreakString: 1000
PenaltyBreakFirstLessLess: 120
PenaltyExcessCharacter: 1000000
PenaltyReturnTypeOnItsOwnLine: 200
PointerAlignment: Left
SpacesBeforeTrailingComments: 2
Cpp11BracedListStyle: true
Standard:        Cpp11
IndentWidth:     4
TabWidth:        4
UseTab:          Never
BreakBeforeBraces: Linux
SpacesInParentheses: false
SpacesInSquareBrackets: false
SpacesInAngles:  false
SpaceInEmptyParentheses: false
SpacesInCStyleCastParentheses: false
SpaceAfterCStyleCast: false
SpacesInContainerLiterals: true
SpaceBeforeAssignmentOperators: true
ContinuationIndentWidth: 4
CommentPragmas:  '^ IWYU pragma:'
ForEachMacros:   [ foreach, Q_FOREACH, BOOST_FOREACH ]
SpaceBeforeParens: ControlStatements
DisableFormat:   false
...

EOM

if ! diff  <(echo -e "$VARIABLE\n") <(clang-format -style=file -dump-config); then
  echo "The clang-format style is not like expected."
  echo "Are there intended changes in .clang-format? Then please change the dump in this script."
  echo "Did the chromium style change? Then please consider following it."
  exit 1
fi

# this is ok, istall the pre-commit hook
test -f $EXCALIBURPATH/.git/hooks/pre-commit ||
read -p "Do you want to install the git commit hook? [y/N] " install
if [ "$install" == "y" -a "$EXCALIBURPATH" != "" ]; then
  ln -s ../../scripts/pre-commit-hook $EXCALIBURPATH/.git/hooks/pre-commit
fi

if [ "$#" -eq 0 ]; then  # no arguments? -> test only and exit
  exit 0
fi

# get file list from arguments (recursively for folders)
lst=""
for f in $@; do
  if [ -f "$f" ]; then
    lst+="$f "
  elif [ -d "$f" ]; then
    lst+=`find $f -name "*.h" -o -name "*.cc"`
  else
    echo "File $f does not exist!"
  fi
done

# possibility to exit
echo "Format these files:"
for i in $lst; do
  echo "  $i"
done
echo "Continue? [y/N] "
read go
if [ "$go" != "y" ]; then
  exit 0
fi

# format with clang-format
for i in $lst; do
  clang-format -style=file -i $i  # format
  sed -i 's/[[:blank:]]*$//' $i   # remove trailing whitespaces
done
