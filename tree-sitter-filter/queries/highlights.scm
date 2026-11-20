["and" "or" "not" "in" "contains"] @keyword
["=" "!=" ">" "<" ">=" "<="] @operator
(string) @string
(number) @number
; boolean memakai @type.builtin: di tema CLI @constant.builtin identik dengan @number (tebal #875f00)
(boolean) @type.builtin
(comparison field: (identifier) @property)
(in_expression field: (identifier) @property)
(contains_expression field: (identifier) @property)
["(" ")" ","] @punctuation.bracket
