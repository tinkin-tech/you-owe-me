from src.__main__ import generate_debt_report


def test_directory_path():
    assert generate_debt_report('~/Desktop/tinkin/python/you-owe-me/tests/repository-fixture/') == """
                                                                                                    Report Type      | Result
                                                                                                    -----------------|-----------
                                                                                                    Code Duplication | 40%
                                                                                                    """
