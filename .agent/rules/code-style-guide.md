---
trigger: always_on
---

# General

- All code in English
- Add comments only when needed
- Add docstrings for every function
- Use type hints in all functions
- Use f-strings
- Follow PEP 8 and clean code principles
- Imports always at the top
- Avoid short variable names, abbreviations, or single-letter names
- Avoid the use of noqa unless strictly necessary

# Test

- Add tests following TDD practices
- Mirror the amazon_paapi structure in the tests directory
- Use unittest.TestCase with setUp() and tearDown()
- Use unittest assertions, not native assert
- Use @patch decorators for mocks (avoid context managers)

# References

- Documentation for the Product Advertising API here: https://webservices.amazon.com/paapi5/documentation/operations.html
