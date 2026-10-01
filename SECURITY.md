# Security Policy

## Supported versions

Only the latest commit on the default branch is supported. Fixes are not backported.

## Reporting a vulnerability

Please **do not** open a public issue for a security problem.

Report it privately through GitHub instead:
**Security → Report a vulnerability** on
[this repository](https://github.com/OdeToTheWind/pro-python-mastery/security/advisories/new).

Please include:

* the affected day or file,
* how to reproduce the problem,
* what an attacker could achieve,
* a suggested fix, if you have one.

You can expect an acknowledgement within 7 days. Confirmed issues are fixed as quickly as
possible and credited in the release notes, unless you would rather stay anonymous.

## Scope

This is a teaching repository. Some days deliberately show unsafe code next to its safe
version, for example `unsafe_find_member` in Day 82 (SQL injection). Each one is clearly
named and its tests prove the safe version is safe. Those demonstrations are not
vulnerabilities, but a *safe* version that can actually be exploited is.
