=========
VALIDATOR
=========

Validator is an implementation of
`saltcheck <https://docs.saltstack.com/en/master/ref/modules/all/salt.modules.saltcheck.html>`_
written for `pop <https://gitlab.com/saltstack/pop/pop>`_ and
`idem <https://gitlab.com/saltstack/pop/idem>`_.

It is a test framework which enables running assertions on any
`idem execution modules <https://idem.readthedocs.io/en/latest/>`_. Like other
`pop projects <https://pop.readthedocs.io>`_, as additional capabilties are added or idem is
extended to additional execution modules, so is validator. Like saltcheck, this capabiltiy
can be used to validate idem states successfully ran, or to validate deployments, permissions,
or anything else for which there is an execution module.

Usage Example
=============

.. code-block:: shell

    # validator examples.tst
    {'TEST RESULTS': {'Execution Time': 0.0044,
                      'Failed': 0,
                      'Passed': 3,
                      'Skipped': 1},
     'multiple assertion test': {'assertion1': {'status': 'Pass'},
                                 'assertion2': {'status': 'Pass'},
                                 'assertion3': {'status': 'Pass'},
                                 'duration': 0.0019,
                                 'status': 'Pass'},
     'test execution module ping': {'duration': 0.0, 'status': 'Pass'},
     'test skip ping': {'duration': 0.0, 'status': 'Skip'},
     'test_jinja': {'duration': 0.0024, 'status': 'Pass'}}


tst Files
=========

An idem test is written in a any `rend <https://gitlab.com/saltstack/pop/rend>`_ supported syntax with a
``.tst`` extension. By default this is commonly used jinja and yaml.

Keywords
--------

:module_and_function:
    (str) The idem execution module to be run.

:args:
    (list) Optional arguments passed to the execution module.

:kwargs:
    (dict) Optional keyword arguments to be passed to the execution module.

:assertion:
    (str) One of the supported assertions. Failed tests cause validator to exit with a non-zero exit code.
    Multiple assertions can be run against the output of a single module_and_function call. The ``assertion``,
    ``expected_return``, ``assertion_section``, and ``assertion_section_delimiter`` keys can be placed in a
    list under an ``assertions`` key. See the multiple assertions example below.

:expected_return:
    (str) Required except by assertEmpty, assertNotEmpty, assertTrue, assertFalse. The return of
    module_and_function is compared to this value in the assertion.

:assertion_section:
    (str) Optional keyword used to parse the module_and_function return. If the execution module returns a
    list or dictionary as a result, the assertion_section value is used to lookup a specific value in that
    return for the assertion comparison.

:assertion_section_delimiter:
    (str) Optional delimiter to use when splitting a nested structure. Defaults to ``:``

:print_result:
    (bool) Optional toggle to show values in test failure results. Defaults to ``True``.

:skip:
    (bool) Optional toggle to skip running the individual test.

Supported Assertions
--------------------

* assertEqual
* assertNotEqual
* assertTrue
* assertFalse
* assertIn
* assertNotIn
* assertGreater
* assertGreaterEqual
* assertLess
* assertLessEqual
* assertEmpty
* assertNotEmpty

Examples
========

Basic Test
----------

.. code-block:: yaml

    test execution module ping:
      module_and_function: test.ping
      assertion: assertTrue

Jinja Example with assertion_section
------------------------------------

.. code-block:: yaml

    {% set expected_value = 5 %}
    test_jinja:
      module_and_function: cmd.run
      args:
        - echo
        - 6
      kwargs:
        shell: True
      assertion_section: stdout
      expected_return: {{ expected_value }}
      assertion: assertLessEqual

Multiple Assertions
-------------------

.. code-block:: yaml

    multiple assertion test:
      module_and_function: cmd.run
      args:
        - echo
        - something
      assertions:
        - assertion: assertNotEmpty
        - assertion: assertEqual
          assertion_section: "stdout"
          expected_return: "something\n"
        - expected_return: s
          assertion: assertIn
          assertion_section: stdout

Skip
----

.. code-block:: yaml

    test skip ping:
      module_and_function: test.ping
      assertion: assertTrue
      skip: True
