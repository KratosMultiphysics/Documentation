python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-avoid-bind' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-deprecated-headers' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-loop-convert' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-make-shared' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-make-unique' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-pass-by-value' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-raw-string-literal' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-redundant-void-arg' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-replace-auto-ptr' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-shrink-to-fit' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-use-auto' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-use-bool-literals' -fix
# python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-use-default-member-init' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-use-emplace' -fix
# python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-use-equals-default' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-use-equals-delete' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-use-nullptr' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-use-override' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-use-transparent-functors' -fix
python run-clang-tidy.py -header-filter='.*' -checks='-*,modernize-use-using' -fix

