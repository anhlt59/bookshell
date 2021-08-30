
## [Pre commit](https://pre-commit.com/)
1. Setup pre commit
    ```sh
    $ pip install -r requirements.txt
    $ pre-commit install
    $ pre-commit install --hook-type commit-msg
    ```

    - config file: `.pre-commit-config.yaml`

2. Demo
    ```text
    $ git add . && git commit -m update
    Trim Trailing Whitespace.................................................Passed
    Fix End of Files.........................................................Passed
    Check Yaml...........................................(no files to check)Skipped
    black....................................................................Passed
    isort....................................................................Passed
    mypy.....................................................................Passed
    Xenon (Radon CI).........................................................Passed
    pytest...................................................................Passed
    - hook id: pytest
    - duration: 1.8s

    ============================= test session starts =============================
    platform win32 -- Python 3.8.3, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
    rootdir: D:\project\bookshell
    plugins: cov-2.11.1
    collected 1 item

    Tools\pre-commit\demo\test_sample.py .                                   [100%]

    ============================== 1 passed in 1.04s ==============================

    [master 03000d4] update
     1 file changed, 1 insertion(+), 1 deletion(-)

    ```
