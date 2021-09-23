import pytest
import __main__


def test_directory_path():
    assert __main__.generate_debt_report('~/Desktop/tinkin/python/you-owe-me/tests/repository-fixture/') == """
                                                                                                    Report Type      | Result
                                                                                                    -----------------|-----------
                                                                                                    Code Duplication | 40%
                                                                                                    """