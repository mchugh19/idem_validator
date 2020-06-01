
#!yaml
test execution module ping:
  module_and_function: test.ping
  assertion: assertTrue

#!jinja|yaml
{% set expected_value = 5 %}
test_args:
  module_and_function: cmd.run
  args:
    - echo 6
  kwargs:
    shell: True
  assertion_section: stdout
  expected_return: {{ expected_value }}
  assertion: assertLessEqual

multiple assertion test:
  module_and_function: cmd.run
  args:
    - echo something
  assertions:
    - assertion: assertNotEmpty
    - assertion: assertEqual
      assertion_section: "stdout"
      expected_return: "something\n"
    - expected_return: some
      assertion: assertIn
      assertion_section: stdout

test skip ping:
  module_and_function: test.ping
  assertion: assertTrue
  skip: True

{#
test custom:
  module_and_function: test.custom
  assertion: assertEqual
  expected_return: "thing"
  assertion_section: some:complicated
#}

#!toml
["test ping toml"]
module_and_function = "test.ping"
assertion = "assertTrue"
skip = false
